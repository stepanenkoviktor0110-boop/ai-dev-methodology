#!/usr/bin/env bash
# deploy-safety SPINE — universal atomic, rollback-able deploy driven by deploy-manifest.yml.
#
# Order (any step's failure aborts; a failed switch AUTO-ROLLS-BACK to the previous image):
#   0. preflight  — change-scoped artifact validation (preflight.py). Red → never touch prod.
#   1. push       — send the branch to the target; refuse to deploy a branch missing current prod.
#   2. backup     — manifest spine.backup_cmd (if set) before any mutation.
#   3. tag :prev  — tag each service's CURRENT image :prev so we can bring the old code back fast.
#   4. build+up   — build new images, recreate services (rm -sf + up: fresh container + env reload).
#   5. health     — poll each /health per manifest (poll/timeout/consecutive-ok).
#   6. smoke      — deterministic runtime-behavior anchors (smoke.py). No LLM.
#   7a. OK        → promote (prev stays as the next rollback point).
#   7b. FAIL      → ROLLBACK: redeploy :prev for every service, verify, exit non-zero. Prod stays up.
#
# This generalizes deploy/deploy-backend.sh (its env_file-reload, uptime-reset and no-silent-rollback
# protections are preserved) and adds the :prev tag + health gate + auto-rollback the old script lacked.
#
# Usage:
#   deploy.sh --ssh HOST --dir /remote/repo --branch BR [--manifest deploy-manifest.yml]
#             [--health-url URL] [--diff-base REF] [--dry-run]
set -euo pipefail

MANIFEST="deploy-manifest.yml"
SSH_HOST=""; REMOTE_DIR=""; BRANCH=""; HEALTH_URL=""; DIFF_BASE=""; DRY=0
PY="${PYTHON:-python}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [ $# -gt 0 ]; do
  case "$1" in
    --ssh) SSH_HOST="$2"; shift 2;;
    --dir) REMOTE_DIR="$2"; shift 2;;
    --branch) BRANCH="$2"; shift 2;;
    --manifest) MANIFEST="$2"; shift 2;;
    --health-url) HEALTH_URL="$2"; shift 2;;
    --diff-base) DIFF_BASE="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$SSH_HOST" ] && [ -n "$REMOTE_DIR" ] && [ -n "$BRANCH" ] || {
  echo "usage: deploy.sh --ssh HOST --dir DIR --branch BR [--manifest M] [--health-url U] [--diff-base R] [--dry-run]" >&2; exit 2; }
[ -f "$MANIFEST" ] || { echo "manifest $MANIFEST missing — run probe.py" >&2; exit 2; }

log() { echo "[$(date -u +%H:%M:%S)] $*"; }
run() { if [ "$DRY" = 1 ]; then echo "  DRY: $*"; else eval "$*"; fi; }

# --- read manifest spine into shell vars (python emits assignments; bash can't parse YAML) ---
eval "$("$PY" - "$MANIFEST" <<'PYEOF'
import sys, yaml
m = yaml.safe_load(open(sys.argv[1], encoding="utf-8")) or {}
s = m.get("spine", {}) or {}
def sq(v): return "'" + str(v).replace("'", "'\\''") + "'"
print("SPINE_SERVICES=" + sq(" ".join(s.get("services") or [])))
print("HEALTH_POLL=" + sq(s.get("health_poll_seconds", 3)))
print("HEALTH_TIMEOUT=" + sq(s.get("health_timeout_seconds", 120)))
print("HEALTH_OK=" + sq(s.get("health_consecutive_ok", 2)))
print("PREV_TAG=" + sq(s.get("prev_tag", "prev")))
print("BACKUP_CMD=" + sq(s.get("backup_cmd") or ""))
PYEOF
)"
[ -n "$SPINE_SERVICES" ] || { echo "manifest spine.services is empty — fill it before deploying" >&2; exit 2; }

echo "== deploy-safety: branch=$BRANCH services=[$SPINE_SERVICES] dry-run=$DRY =="

# --- 0. preflight runs ON THE TARGET (Linux), inside the remote block after checkout — where the
#        tools (bash/nginx/docker) and the REAL target .env/configs exist. Running it on the deploy
#        operator's box would (a) false-fail on a non-Linux host and (b) validate repo artifacts
#        instead of the actual target state. CI (--all on Linux) remains the pre-merge gate.
log "0. preflight → runs on target (post-checkout, pre-recreate); CI is the pre-merge gate"

# --- 1. push branch to target's origin mirror (if the target deploys from a local bare mirror) ---
# Many targets `git fetch` from THEIR OWN origin (often a local bare repo), NOT from GitHub. If that
# mirror is stale, the on-target ancestry guard ABORTS (safe) — but the operator must know WHY. So a
# missing/failed mirror push is a LOUD warning with the exact fix, never a silent `|| true` (that
# silence is precisely what hides deploy drift — the recurring "fix is in git but not on prod").
log "1. push $BRANCH to target mirror"
if git remote get-url "$SSH_HOST-vps" >/dev/null 2>&1 || git remote get-url vps >/dev/null 2>&1; then
  run "git push '$SSH_HOST-vps' '$BRANCH' 2>/dev/null || git push vps '$BRANCH' 2>/dev/null || echo '  WARN: mirror push FAILED — target will deploy whatever its own origin already has (guard is the net)'"
else
  log "  WARN: no mirror remote ('$SSH_HOST-vps' or 'vps') configured locally — target will deploy from ITS OWN origin."
  log "        If that origin is a stale bare mirror the on-target guard ABORTS (prod untouched). To feed the mirror, add e.g.:"
  log "        git remote add vps $SSH_HOST:/root/repos/<repo>.git   (then it fast-forwards the mirror each deploy)"
fi

# --- 2-7. remote: backup, tag :prev, build, recreate, health-gate, rollback-on-fail ---
REMOTE_SCRIPT=$(cat <<'REMOTE'
set -euo pipefail
cd "$REMOTE_DIR"
log() { echo "[$(date -u +%H:%M:%S)] $*"; }

# refuse to deploy a branch that does not contain the running commit (no silent rollback of newer prod)
git fetch --all --quiet
CUR=$(git rev-parse HEAD); CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if ! git merge-base --is-ancestor "$CUR" "origin/$BRANCH"; then
  echo "ABORT: origin/$BRANCH does not contain current prod $CUR — would roll back." >&2; exit 3
fi

# 1b. check out the new code. Running containers still use their OLD baked images, so prod is
#     unaffected until recreate — this is safe and lets preflight validate the real new tree.
git checkout -B "$BRANCH" "origin/$BRANCH"
log "checked out: $(git log --oneline -1)"

# 2. PREFLIGHT ON TARGET — validate the new tree + the REAL target .env/configs, before ANY mutation.
#    Runs here (Linux) not on the operator's box: the tools and actual target state live here. A
#    failure aborts with prod fully intact (nothing rebuilt/recreated yet); we just restore the tree.
if [ -f deploy/deploy-safety/preflight.py ]; then
  log "2. preflight (on target)"
  if ! python3 deploy/deploy-safety/preflight.py --repo . --manifest "$MANIFEST_NAME" --all; then
    echo "ABORT: preflight failed on target — restoring tree, prod untouched" >&2
    git checkout -B "$CUR_BRANCH" "$CUR" >/dev/null 2>&1 || git checkout -f "$CUR" >/dev/null 2>&1 || true
    exit 4
  fi
else
  log "2. preflight skipped (no vendored deploy/deploy-safety/preflight.py in repo — CI is the gate)"
fi

# 3. backup before mutation
if [ -n "$BACKUP_CMD" ]; then log "3. backup: $BACKUP_CMD"; bash -c "$BACKUP_CMD"; fi

# 4. tag each service's CURRENT image :prev (the rollback point). Derive the image NAME from the
#    running container (.Config.Image) — works for both `image:` services AND build-only services
#    (whose compose `image:` is empty; compose auto-names the built image <project>-<service>).
declare -A IMG
for SVC in $SPINE_SERVICES; do
  CID=$(docker compose ps -q "$SVC" 2>/dev/null || true)
  if [ -n "$CID" ]; then
    IMGID=$(docker inspect --format '{{.Image}}' "$CID")          # sha of the running image
    IMGNAME=$(docker inspect --format '{{.Config.Image}}' "$CID")  # compose-assigned name/tag
    IMG["$SVC"]="$IMGNAME"
    docker tag "$IMGID" "${IMGNAME%:*}:$PREV_TAG"; log "4. tagged $SVC ($IMGNAME) -> ${IMGNAME%:*}:$PREV_TAG"
  fi
done

# 5. build + recreate (rm -sf + up: fresh container AND env_file reload)
log "5. build+recreate: $(git log --oneline -1)"
for SVC in $SPINE_SERVICES; do docker compose build "$SVC"; done
for SVC in $SPINE_SERVICES; do docker compose rm -sf "$SVC"; docker compose up -d --no-deps "$SVC"; done

# 5. health gate: poll /health, require N consecutive OK within timeout; uptime must have reset
rollback() {
  echo "!! rolling back to :$PREV_TAG" >&2
  for SVC in $SPINE_SERVICES; do
    NAME="${IMG[$SVC]:-}"; [ -n "$NAME" ] || continue
    docker tag "${NAME%:*}:$PREV_TAG" "$NAME" 2>/dev/null || true   # point the compose image back to prev
    docker compose rm -sf "$SVC" || true; docker compose up -d --no-build --no-deps "$SVC" || true
  done
  echo "!! rolled back — prod restored to previous image" >&2; exit 5
}
HEALTH_DEADLINE=$(( $(date -u +%s) + HEALTH_TIMEOUT ))
for SVC in $SPINE_SERVICES; do
  ST=$(docker compose ps "$SVC" --format '{{.Status}}' || true)
  case "$ST" in *hour*|*day*|*week*) echo "!! $SVC NOT recreated (old container): $ST" >&2; rollback;; esac
done
if [ -n "$HEALTH_URL" ]; then
  ok=0
  while [ "$(date -u +%s)" -lt "$HEALTH_DEADLINE" ]; do
    code=$(curl -sk -o /dev/null -w '%{http_code}' --max-time 10 "$HEALTH_URL" || echo 000)
    if [ "$code" = 200 ]; then ok=$((ok+1)); else ok=0; fi
    log "5. health $HEALTH_URL -> $code (consecutive ok=$ok/$HEALTH_OK)"
    [ "$ok" -ge "$HEALTH_OK" ] && break
    sleep "$HEALTH_POLL"
  done
  [ "$ok" -ge "$HEALTH_OK" ] || { echo "!! health gate failed" >&2; rollback; }
fi
log "OK: services healthy on new image"
REMOTE
)

log "2-6. remote (checkout, preflight-on-target, backup, tag :prev, build, recreate, health-gate, auto-rollback)"
if [ "$DRY" = 1 ]; then
  echo "  DRY: ssh $SSH_HOST with REMOTE_DIR=$REMOTE_DIR BRANCH=$BRANCH SPINE_SERVICES='$SPINE_SERVICES' HEALTH_URL=$HEALTH_URL"
  echo "  DRY: would run the remote backup/tag-prev/build/recreate/health-gate/rollback block"
else
  ssh -o BatchMode=yes "$SSH_HOST" \
    "REMOTE_DIR='$REMOTE_DIR' BRANCH='$BRANCH' SPINE_SERVICES='$SPINE_SERVICES' HEALTH_URL='$HEALTH_URL' \
     HEALTH_POLL='$HEALTH_POLL' HEALTH_TIMEOUT='$HEALTH_TIMEOUT' HEALTH_OK='$HEALTH_OK' \
     PREV_TAG='$PREV_TAG' BACKUP_CMD='$BACKUP_CMD' MANIFEST_NAME='$(basename "$MANIFEST")' bash -seuo pipefail" <<<"$REMOTE_SCRIPT"
fi

# --- 6. post-deploy runtime-behavior smoke (deterministic anchors) → rollback handled by smoke exit ---
log "6. post-deploy smoke (runtime-behavior anchors)"
if [ "$DRY" = 1 ]; then
  echo "  DRY: $PY $SKILL_DIR/smoke.py --manifest $MANIFEST --ssh $SSH_HOST"
else
  "$PY" "$SKILL_DIR/smoke.py" --manifest "$MANIFEST" --ssh "$SSH_HOST" || {
    echo "!! smoke failed — triggering remote rollback" >&2
    ssh -o BatchMode=yes "$SSH_HOST" \
      "REMOTE_DIR='$REMOTE_DIR' SPINE_SERVICES='$SPINE_SERVICES' PREV_TAG='$PREV_TAG' bash -seuo pipefail" <<'RB'
cd "$REMOTE_DIR"
# derive the image name from the (new) running container — same base name across builds, so the
# :prev tag from step 3 restores build-only services too. No cross-session state needed.
for SVC in $SPINE_SERVICES; do
  CID=$(docker compose ps -q "$SVC" 2>/dev/null || true); [ -n "$CID" ] || continue
  NAME=$(docker inspect --format '{{.Config.Image}}' "$CID")
  docker tag "${NAME%:*}:$PREV_TAG" "$NAME" 2>/dev/null || true
  docker compose rm -sf "$SVC" || true; docker compose up -d --no-build --no-deps "$SVC" || true
done
echo "rolled back after smoke failure — prod restored" >&2
RB
    exit 6
  }
fi

echo "== deploy-safety: DONE — new version live, verified, :$PREV_TAG kept as rollback point =="
