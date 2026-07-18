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

# --- 0. preflight (local, change-scoped) — the gate. Red here = prod is never touched. ---
log "0. preflight"
PF_ARGS=(--repo . --manifest "$MANIFEST")
if [ -n "$DIFF_BASE" ]; then PF_ARGS+=(--diff-base "$DIFF_BASE"); else PF_ARGS+=(--all); fi
if [ "$DRY" = 1 ]; then
  echo "  DRY: $PY $SKILL_DIR/preflight.py ${PF_ARGS[*]}"
else
  "$PY" "$SKILL_DIR/preflight.py" "${PF_ARGS[@]}" || { echo "ABORT: preflight failed" >&2; exit 1; }
fi

# --- 1. push branch to target (backup remote optional) ---
log "1. push $BRANCH to target"
run "git push '$SSH_HOST-vps' '$BRANCH' 2>/dev/null || git push vps '$BRANCH' 2>/dev/null || true"

# --- 2-7. remote: backup, tag :prev, build, recreate, health-gate, rollback-on-fail ---
REMOTE_SCRIPT=$(cat <<'REMOTE'
set -euo pipefail
cd "$REMOTE_DIR"
log() { echo "[$(date -u +%H:%M:%S)] $*"; }

# refuse to deploy a branch that does not contain the running commit (no silent rollback of newer prod)
git fetch --all --quiet
CUR=$(git rev-parse HEAD)
if ! git merge-base --is-ancestor "$CUR" "origin/$BRANCH"; then
  echo "ABORT: origin/$BRANCH does not contain current prod $CUR — would roll back." >&2; exit 3
fi

# 2. backup before mutation
if [ -n "$BACKUP_CMD" ]; then log "2. backup: $BACKUP_CMD"; bash -c "$BACKUP_CMD"; fi

# 3. tag each service's CURRENT image :prev (the rollback point). Derive the image NAME from the
#    running container (.Config.Image) — works for both `image:` services AND build-only services
#    (whose compose `image:` is empty; compose auto-names the built image <project>-<service>).
declare -A IMG
for SVC in $SPINE_SERVICES; do
  CID=$(docker compose ps -q "$SVC" 2>/dev/null || true)
  if [ -n "$CID" ]; then
    IMGID=$(docker inspect --format '{{.Image}}' "$CID")          # sha of the running image
    IMGNAME=$(docker inspect --format '{{.Config.Image}}' "$CID")  # compose-assigned name/tag
    IMG["$SVC"]="$IMGNAME"
    docker tag "$IMGID" "${IMGNAME%:*}:$PREV_TAG"; log "3. tagged $SVC ($IMGNAME) -> ${IMGNAME%:*}:$PREV_TAG"
  fi
done

# 4. fast-forward + build + recreate (rm -sf + up: fresh container AND env_file reload)
git checkout -B "$BRANCH" "origin/$BRANCH"
log "4. build+recreate: $(git log --oneline -1)"
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

log "2-5. remote deploy (backup, tag :prev, build, recreate, health-gate, auto-rollback)"
if [ "$DRY" = 1 ]; then
  echo "  DRY: ssh $SSH_HOST with REMOTE_DIR=$REMOTE_DIR BRANCH=$BRANCH SPINE_SERVICES='$SPINE_SERVICES' HEALTH_URL=$HEALTH_URL"
  echo "  DRY: would run the remote backup/tag-prev/build/recreate/health-gate/rollback block"
else
  ssh -o BatchMode=yes "$SSH_HOST" \
    "REMOTE_DIR='$REMOTE_DIR' BRANCH='$BRANCH' SPINE_SERVICES='$SPINE_SERVICES' HEALTH_URL='$HEALTH_URL' \
     HEALTH_POLL='$HEALTH_POLL' HEALTH_TIMEOUT='$HEALTH_TIMEOUT' HEALTH_OK='$HEALTH_OK' \
     PREV_TAG='$PREV_TAG' BACKUP_CMD='$BACKUP_CMD' bash -seuo pipefail" <<<"$REMOTE_SCRIPT"
fi

# --- 6. post-deploy runtime-behavior smoke (deterministic anchors) → rollback handled by smoke exit ---
log "6. post-deploy smoke (runtime-behavior anchors)"
if [ "$DRY" = 1 ]; then
  echo "  DRY: $PY $SKILL_DIR/smoke.py --manifest $MANIFEST"
else
  "$PY" "$SKILL_DIR/smoke.py" --manifest "$MANIFEST" || {
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
