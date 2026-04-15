# Codex-First Routing

> Loaded by feature-execution orchestrator in Phase 2 ONLY when `codex_mode: true` in checkpoint.yml.

For each task, determine executor before spawning:

**Claude-only** (auto-override):
- Task has `skills:` containing `deploy-pipeline` or `infrastructure-setup` (needs SSH/MCP)
- Fix after review, diff < 30 lines
- Codex returned 403 / rate limit / auth failure for this session

**Codex-eligible** — everything else. For Codex-eligible tasks:

a. **Select triads** from cached triad-index.md:
   - Filter by: `skill` column matches any of task's `skills`, OR keyword overlap between task "What to do" and triad `trigger`
   - Take top 5 by relevance. If 0 matches — skip `<pitfalls>` block.

b. **Build Codex prompt** (XML structure per `gpt-5-4-prompting` skill):

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

c. **Send to Codex** via companion runtime (foreground, Bash timeout 600000ms):
   ```
   node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" task --write "{prompt}"
   ```
   No polling, no background. Single blocking call — 0 tokens on monitoring.
   On Bash timeout (10 min) → fall through to Claude (step 3).

e. **On Codex completion:**
   - Run tests locally (`npm test` or project equivalent)
   - Quick grep: `password|secret|api_key` in new files (exclude test fixtures)
   - Tests pass + grep clean → commit: `feat: task {N} — {brief} [codex]`, proceed to review (step 2.f)
   - Tests fail → send failure to Codex (`--resume-last`), max 2 retries
   - After 2 retries still failing → fall through to Claude (step 3)

f. **Codex review** (lighter than full Claude review):
   - Codex already did self-review (prompted in `<action_safety>`)
   - Lead runs grep for anti-patterns: missing timeouts in fetch/axios, secrets in logs, SQL without parameterization
   - Full reviewer spawning (`code-reviewer`, `security-auditor`) only on **last task of the wave** — reviews cumulative wave diff, not per-task
   - If task has `reviewers: none` — grep check only, no reviewer spawning

g. **Fallback to Claude:** On Codex 403/rate-limit/timeout/repeated test failure:
   - Log: `"Codex failed: {reason}. Falling back to Claude for task {N}."`
   - Codex-written files remain on disk — Claude teammate starts from current state
   - Execute standard step 3 below (spawn Claude teammate)
