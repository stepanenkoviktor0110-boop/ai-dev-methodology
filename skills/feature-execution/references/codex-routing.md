# Codex-First Routing

> Loaded by feature-execution orchestrator in Phase 2 ONLY when `codex_mode: true` in checkpoint.yml.

For each task, determine executor before delegating:

**Claude-only** (auto-override):
- Task has `skills:` containing `deploy-pipeline` or `infrastructure-setup` (needs SSH/MCP)
- Fix after review, diff < 30 lines
- Codex returned 403 / rate limit / auth failure for this session

**Codex-eligible** — everything else. For Codex-eligible tasks, follow steps (a)–(g) below.

---

## Pre-delegation size check (gate — run before step a)

Check both conditions:
- **≤ 3 files** — count files listed under "Files to modify" in the task.
- **Single intent** — the task has one coherent goal (add a handler, rewrite a module, etc.), not a bundle of unrelated changes.

If either condition fails → **require split**. Tell the orchestrator: "Task exceeds delegation scope (files: N / intent: multiple). Split into smaller tasks before delegating to Codex." Do NOT proceed to step (a) until the task is split.

---

## Steps for Codex-eligible tasks

### (a) Select triads from cached triad-index.md

- Filter by: `skill` column matches any of task's `skills`, OR keyword overlap between task "What to do" and triad `trigger`.
- Take top 5 by relevance. If 0 matches — skip `<pitfalls>` block.

### (b) Build Codex prompt (XML structure)

```xml
<task>
{task "What to do" section, verbatim}
Context files: {task Context Files list}
Acceptance criteria: {task acceptance criteria, verbatim}
</task>

<pitfalls>
{selected triads as: "When {trigger} → {action}"}
</pitfalls>

<project_patterns>
{cached patterns.md contents, if available}
</project_patterns>

<completeness_contract>
Write files one at a time. After each file, verify syntax.
Do not batch all files into one response.
</completeness_contract>

<action_safety>
Scope changes to listed files only. No unrelated refactors.
Self-review before finishing: no hardcoded secrets, no unused imports, no missing error handling at boundaries.
</action_safety>
```

### (c) Deliver prompt via tmp-file

XML prompt contains quotes, backticks, `$`, and newlines. **Never pass it inline** (`--write "{prompt}"`) — shell interpolation will break or silently corrupt the content.

Write to a temp file and pass the path:

```bash
PROMPT_FILE="$(mktemp -t codex-prompt-XXXXXX.xml)"
cat > "$PROMPT_FILE" <<'EOF'
<task>...</task>
...
EOF
```

### (d) Launch Codex in background

```bash
LAUNCH_JSON=$(node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" \
  task --background --write --json --prompt-file "$PROMPT_FILE")
JOB_ID=$(echo "$LAUNCH_JSON" | jq -r '.jobId // empty')
[ -z "$JOB_ID" ] && { echo "Codex launch failed: $LAUNCH_JSON"; exit 1; }
[[ "$JOB_ID" =~ ^[a-zA-Z0-9_-]+$ ]] || { echo "Codex launch returned invalid JOB_ID format: $JOB_ID"; exit 1; }
```

If `JOB_ID` is empty or has unexpected format → stop with error message; do NOT proceed to step (e), do NOT call ScheduleWakeup.

### (e) Initialize codex-jobs.yml

Before calling ScheduleWakeup, write an entry to `work/{feature}/codex-jobs.yml`.

> **Note:** Add `codex-jobs.yml` to `.gitignore` for the feature directory — the `description` field is copied from the task and may contain internal URLs or sensitive context. Do not commit this file.

Keep `description` short and human-readable (e.g. "Task 3: add webhook handler") — do not paste the full task context.

```yaml
jobs:
  - job_id: "{JOB_ID}"
    description: "{task description — first line of task Description field}"
    started_at: "{ISO-8601 UTC timestamp}"   # e.g. 2026-04-19T10:00:00Z
    status: in_progress
    resume_count: 0
```

If the file already exists (from a previous job in this feature), append to the `jobs` list.

### (f) Schedule polling

Call `ScheduleWakeup(delaySeconds=270)` immediately after writing codex-jobs.yml. Bash is now unblocked — orchestrator continues with other work.

### (g) On wake-up — polling loop

Check job status:

```bash
STATUS=$(node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" \
  status "$JOB_ID" --json | jq -r '.status')
```

Branch on `STATUS`:

- **`running`** → log `"Codex: {elapsed} min, still running"` + call `ScheduleWakeup(270)` again. Do NOT cancel — if the job is long, the orchestrator failed the size check. Cancel only on explicit user request.
- **`done`** → get output and run tests:
  ```bash
  OUTPUT=$(node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" \
    result "$JOB_ID" --json | jq -r '.output')
  ```
  Run local tests (`npm test` or project equivalent). Quick grep: `password|secret|api_key` in new files (exclude test fixtures).
  Tests pass + grep clean → commit `feat: task {N} — {brief} [codex]`, proceed to review (step h).
  Tests fail → report to user; do NOT auto-retry.
  Update yml: `status: completed`.
- **`error`** → write plain-text diagnosis in chat (what Codex reported). Update yml: `status: cancelled`. STOP — do NOT call a new ScheduleWakeup. No automatic retry, no fallback to Claude.

### (h) Codex review (on done path)

- Codex already did self-review (prompted in `<action_safety>`).
- Lead runs grep for anti-patterns: missing timeouts in fetch/axios, secrets in logs, SQL without parameterization.
- Full reviewer spawning (`code-reviewer`, `security-auditor`) only on **last task of the wave** — reviews cumulative wave diff, not per-task.
- If task has `reviewers: none` — grep check only, no reviewer spawning.

---

## Auto-recover on session start

On every session start, check `work/{feature}/codex-jobs.yml`:

- **File absent** → skip silently. No error.
- **File present, entry has `status: in_progress`**:
  - If `resume_count` field is absent → treat as 0 (backward compatibility with old yml entries).
  - `resume_count == 0` → check current Codex status via `status <job-id> --json`:
    - `running` → increment `resume_count` to 1 in yml, resume polling loop (call ScheduleWakeup(270)).
    - `done` → retrieve result, run tests, update `status: completed`.
    - `error` → plain-text diagnosis in chat, update `status: cancelled`.
  - `resume_count == 1` → report to user: "Job {job_id} is still in_progress after one auto-recovery attempt. Manual check required." Do NOT auto-resume.
- **Entry has `status: completed` or `cancelled`** → no action needed.

---

## Edge cases

| Situation | Behavior |
|-----------|----------|
| `codex-jobs.yml` absent at session start | Skip silently — not an error |
| `resume_count` field absent in entry | Treat as 0 (backward compat) |
| `JOB_ID` empty after `task --background` | Stop with error message; no polling |
| Codex error during polling | Diagnosis in chat + `status: cancelled` in yml + STOP; no new ScheduleWakeup |
| Job running longer than expected | Do NOT cancel automatically; orchestrator is responsible for task size via pre-delegation size check |
| User wants to cancel a running job | Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" cancel "$JOB_ID"` manually; update yml `status: cancelled` |
