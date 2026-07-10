---
name: parallel-tracks
description: |
  Run 2-3 features in parallel across independent sessions without breaking the
  live platform: isolate each feature (branch + git worktree), coordinate through
  shared repo files (never session memory), and converge via a serialized
  integration train (rebase -> migration merge -> PR/CI -> ephemeral staging smoke
  -> merge -> per-service deploy). One session = one feature = one track.

  Use when: "веди фичи параллельно", "изолируй фичу", "изолируй трек",
  "собери фичу", "влей фичу", "собери X", "параллельная разработка",
  "integrate feature", "parallel development", "merge feature into dev".

  Auto-invoked by feature-execution at feature start (track isolation + registration)
  and at feature end (integration train). Also callable directly ("собери <feature>").
---

# Parallel Tracks

Cross-feature layer above the single-feature pipeline (user-spec -> tech-spec ->
decompose -> do-feature -> done). Lets 2-3 features run in **independent sessions**
in parallel and converge into `dev` **one at a time** through a gate, so the live
platform (and any live bot/service) is never interrupted during integration.

**Golden rule:** parallelize development, isolate the runtime used for integration,
serialize the point of convergence.

## Core model

- **Track** = one feature going through the standard pipeline, isolated on its own
  branch `feature/<slice>` in its own **git worktree**. One session works one track
  to result.
- **Integration train** = the serialized convergence. Only one track merges into
  `dev` at a time, through a gate. Development stays parallel; only the merge is
  ordered.
- **Coordination lives in files, not session memory.** Independent sessions share
  nothing except the repo. Two small files carry all cross-session state:
  - `work/_train/tracks.json` — the track map (who does what, danger zones, merge order).
  - `work/_train/train.lock.d/` — the integration lock (who is merging right now).

  Both are managed by `scripts/train.py` (stdlib-only, PowerShell+Bash). `work/_train/`
  is gitignored and resolved via the git common dir, so it is ONE shared dir seen by
  every worktree/session on this machine. Sessions never rely on remembering each other —
  they read these files.

## Danger zones (shared seams)

A track declares which shared seams it touches. A collision on any of these forces
merge ordering (the later track integrates after the earlier one):

- `schema` — DB migrations / table changes
- `auth` — tenant scope, RLS, login, access control
- `prompt-core` — shared bot behavioral prompt / core answer logic
- `deploy-config` — compose files, shared `.env`, container topology
- `rag` — vector collection schema, indexing, sources (also selects staging depth)

Non-overlapping tracks integrate in finish order, no waiting.

---

## Part A — Track start (isolation + registration)

Runs at the **start** of a feature (invoked by feature-execution Phase 1, or manually
before planning). Zero extra action required from the owner beyond naming the feature.

Infer which danger zones the feature will touch from its tech-spec / task files
(migrations => `schema`, tenant_scope/RLS/login => `auth`, shared prompt => `prompt-core`,
compose/.env => `deploy-config`, RAG/sources/indexing => `rag`), then run:

```
python scripts/train.py start <slice> --touches schema,auth
```

This single command: fetches `origin`, creates branch `feature/<slice>` + git worktree
`../wt-<slice>` from fresh `origin/dev` (reuses if they exist), registers the track in
`work/_train/tracks.json`, and runs the **collision check** — if this track shares a hard
zone (`schema`/`auth`/`prompt-core`/`deploy-config`) with another live track it prints a
`COLLISION:` line and records `depends_on` so this feature integrates **after** the other.

When a collision is printed, relay it to the owner once, in plain language:
> «Фича Y трогает ту же базу, что и X, которую ты уже делаешь в другой сессии.
> Соберём Y после X, чтобы не столкнулись.»
The order is now in the file — do not re-ask in later sessions.

Then `cd ../wt-<slice>` and run the normal pipeline there. **Never commit feature work
directly to `dev`** — only to `feature/<slice>`.

---

## Part B — Integration train ("собери <feature>")

Runs when the feature is done (`do-feature` green incl. Audit Wave), **before** `/done`.
Serialized: one track at a time.

1. **Preconditions.** On `feature/<slice>` in its worktree; do-feature completed clean.
   Check `python scripts/train.py status` — if this track has `depends_on` tracks not yet
   `merged`, tell the owner it waits for them, stop.
2. **Acquire the lock:** `python scripts/train.py lock <slice>`. On `BUSY:` another track
   is integrating → relay «сейчас собирается <holder>, <slice> встанет следом», stop, let
   the owner re-run when free. Never integrate two at once. (A stale/abandoned lock is
   auto-cleared by the tool.)
3. **Rebase on fresh `dev`:** `git fetch origin && git rebase origin/dev`. Resolve
   conflicts (technical — resolve autonomously; escalate only genuinely ambiguous product
   logic). A rebase that cannot proceed → `git rebase --abort`, fix, re-run.
4. **Reconcile + prove migrations:** `python scripts/train.py migration-check`. Auto-creates
   an `alembic merge heads` revision if the chain forked, then proves `upgrade head` +
   `downgrade base` + re-`upgrade` all run clean on a FRESH throwaway DB
   (`docker-compose.local.yml`, port 5440 — never dev/prod). This is the guard against the
   #1 integration breakage (two migration heads crash prod's `alembic upgrade head`).
5. **PR + CI gate.** Push the branch (`gh auth switch --user viktors-byt` first — see
   deployment.md) and open a PR `feature/<slice>` -> `dev` (`gh pr create`). GitHub Actions
   (`test.yml`) runs the full suite + cross-tenant security tests and **must pass** —
   enforced by branch protection on `dev`. Red CI → fix on the branch, do not merge.
   Watch: `gh pr checks --watch`.
6. **Merge** the PR into `dev` (`gh pr merge --squash`). This is the only write to `dev`.
7. Set the track `merged` and **release the lock:** `python scripts/train.py unlock <slice>`.
8. Proceed to Part C (deploy).

> On CI: the GitHub Actions suite already runs on ephemeral postgres+redis, so it IS the
> integration smoke for schema/auth/app logic. A full RAG (ml+qdrant) end-to-end smoke is
> only meaningful on the VPS (the ml image carries ~4.5 GB baked weights, not runnable on
> the dev box) — for `touches: rag` tracks, defer that check to the post-deploy verify on
> prod rather than a local full stack.

If the next track had `depends_on: [<this>]`, it can now integrate — its session
re-runs "собери" and finds the lock free.

---

## Part C — Deploy (per-service, no platform interruption)

1. **Env-contract check (mandatory).** Before any rebuild, verify the VPS `.env` carries
   every required (no-default) `Settings` field:
   `python scripts/check-deploy-env.py --ssh aiplatform --env /root/ai-platform/.env`
   (and the fizika env file if fizika is in the diff). A missing key here is exactly what
   crash-loops an unrelated live service on rebuild. Missing → stop, list them, fix the VPS
   env first. (Checks by NAME only, never reads a value.)
2. **Deploy only changed services.** Use the project runbook `deploy/deploy-backend.sh dev`
   — it pushes `dev`, rebuilds+recreates only the listed services (fizika first, then app),
   refuses a branch that would roll back prod, and verifies health. For a change that does
   NOT touch a live service, that service is not rebuilt and keeps running.
3. **Verify (built into the runbook).** `deploy-backend.sh` already asserts each recreated
   container is healthy AND that untouched containers still read "Up N hours" (not seconds)
   — proof the live bot was not restarted. For a build that changes the served widget, pass
   its embed.js marker as arg 2.
4. Then run `/done` for the feature (updates project-knowledge, archives, syncs the board).

---

## Cross-session coordination (why independent sessions stay in sync)

- All shared state is on disk in the repo (`work/_train/tracks.yml`, `train.lock`),
  committed and pushed — so a session that knows nothing about the others still sees
  the current map and lock.
- The **lock file** gives mutual exclusion on integration across sessions that don't
  share memory: create-if-absent = acquire, delete = release.
- The **track map** carries merge order (`depends_on`) so a collision decided once in
  one session is honored by every later session without re-asking the owner.
- If a session dies mid-integration, the lock can be stale — a lock older than a safe
  window (or naming a track already `merged`) is treated as abandoned and cleared with
  a one-line note to the owner.

## Owner-facing surface (keep it this small)

- Start of a session: **nothing new** — the track self-registers.
- Once per batch, only on a real collision: one plain-language «соберём Y после X» → «ок».
- End of a session, at result: one word — **«собери»**.

Everything else (isolation, rebase, migration merge, CI, staging, per-service deploy,
verification) is automatic and decided technically without bothering the owner.

## Project-specific pieces (supplied by the repo, not this skill)

This skill is stack-agnostic. On the AI-platform repo the concrete implementation reuses
existing tooling — do NOT recreate it:
- `scripts/train.py` — track map + lock + migration-check (the only new coordination tool).
- `docker-compose.local.yml` — the throwaway fresh-DB stack used by `migration-check`.
- `scripts/check-deploy-env.py` — the env-contract guard (Part C step 1).
- `deploy/deploy-backend.sh` — per-service deploy + health/uptime/marker verify (Part C).
- GitHub Actions `test.yml` — the PR CI gate; branch protection on `dev` enforces it.

On another project, supply equivalents for these five roles.

## Self-verification

- [ ] Feature worked on `feature/<slice>` in its own worktree, never committed to `dev` directly
- [ ] Track registered via `train.py start`; collisions ordered via `depends_on`
- [ ] Integration held the `train.py` lock (one track at a time); rebase done
- [ ] `train.py migration-check` green (single head, reversible on fresh DB)
- [ ] PR CI green before merge (branch protection on `dev`)
- [ ] Deploy via `deploy-backend.sh`: only changed services rebuilt; untouched live services still "Up N hours"
- [ ] Lock released (`train.py unlock`); `/done` run
