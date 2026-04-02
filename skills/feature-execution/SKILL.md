---
name: feature-execution
description: |
  Orchestrate feature delivery as team lead: spawn agents by wave,
  manage review cycles (max 3 rounds), commit per wave.

  Use when: "выполни фичу", "do feature", "execute feature", "запусти фичу",
  "выполни все задачи", "execute all tasks"
---

# Feature Execution

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Team lead orchestrates feature delivery. You are a dispatcher: spawn agents, track progress, commit code, escalate issues. Delegate all code reading, diff analysis, and report review to spawned agents. Your only inputs are status messages from teammates ("Task complete") and escalation requests.

Before starting, read [quick-ref-feature-execution.md](../quick-learning/references/quick-ref-feature-execution.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Initialization

0. Check `work/{feature}/logs/checkpoint.yml`:
   - `last_completed_wave > 0` → this is a resume after context compaction.
     Read checkpoint, then read `work/{feature}/decisions.md` to confirm what was actually completed.
     For tasks in the resumed wave: if a task has a decisions.md entry, it completed — update its
     frontmatter to `done` and skip it. Only re-execute tasks without a decisions.md entry.
     Check if `~/.claude/teams/{team_name}/config.json` exists: if yes, team is alive; if no,
     recreate via TeamCreate. Skip to Phase 2 starting from `next_wave`.
     Read session-plan.md to determine which session the next_wave belongs to. Update current_session accordingly.
     Report to user: "Resuming from wave {N} (session {S}). Waves 1-{N-1} completed."
   - `last_completed_wave: 0` → fresh start, proceed below.

1. Read `work/{feature}/tech-spec.md` and `work/{feature}/user-spec.md`
1.5. Read `work/{feature}/logs/session-plan.md` if it exists. Parse session boundaries: which waves belong to which session. If file does not exist — treat all waves as one session (backward compatibility).
2. Read frontmatter of all task files in `work/{feature}/tasks/` — extract fields:

   | Field | Purpose |
   |-------|---------|
   | `status` | planned → in_progress → done |
   | `wave` | Parallel execution group number |
   | `depends_on` | Task numbers that must be done first |
   | `skills` | Skills the teammate loads |
   | `reviewers` | Reviewer agents to spawn (source of truth) |
   | `teammate_name` | Agent name for team spawning (optional) |
   | `verify` | Verification types: [smoke], [user], [smoke, user], or [] (optional) |

   Build waves: group tasks by `wave` field. Within a wave, all tasks run in parallel.

3. Build execution plan following template at `~/.claude/shared/work-templates/execution-plan.md.template`
4. Save to `work/{feature}/logs/execution-plan.md`
5. Show plan to user, wait for approval
6. Create team via TeamCreate
7. Update `work/{feature}/logs/checkpoint.yml`: set `total_waves` from the execution plan.
8. If session-plan.md was found (step 1.5): write `current_session` and `total_sessions` to checkpoint.yml.

**Checkpoint:** execution plan approved, team created, checkpoint initialized.

## Phase 2: Execute Wave

1. Find tasks for current wave: `status: planned`, all `depends_on` tasks are `done`
2. Update frontmatter: `status: planned` → `status: in_progress`
3. For each task, spawn **teammate + reviewers** (if task has reviewers):

   Use `teammate_name` from task frontmatter as the agent name. If not set — pick a descriptive name based on the task.

   **Teammate** — `subagent_type: "general-purpose"`, `model: "opus"`, `team_name: "{team}"`

   Prompt template:

   ```
   You are "{name}" executing task {N}.

   Read task: {feature_dir}/tasks/{N}.md
   Load skills listed in task frontmatter. Follow the loaded skill workflow.

   If the task requires user actions — send the instruction to team lead via SendMessage.
   Team lead will forward to user and return confirmation.

   {reviewers_block}

   After task complete:
   - Write entry to {feature_dir}/decisions.md (follow template at ~/.claude/shared/work-templates/decisions.md.template).
     Use Planned/Actual/Deviation structure. If you have concerns (performance, edge case, tech debt) — set status "Done with concerns" and fill the Concerns field.
   - Message team lead: "Task {N} complete. decisions.md updated." (add "with concerns: {brief}" if applicable)

   Feature dir: {feature_dir}
   ```

   **{reviewers_block}** — include only when task has reviewers (not `reviewers: none`):

   ```
   Your reviewers: {reviewer_names} (list of teammate names).

   Review process — after task is complete, follow this review process (overrides review steps from loaded skills):
   1. Run `git diff -- <your files>` and collect the list of changed files + full diff output.
   2. Send each reviewer via SendMessage: list of changed files + full diff output.
   3. Reviewers will perform review, write JSON report to `{feature_dir}/logs/working/task-{N}/{reviewer_name}-round{round}.json`, and send report path back to you.
   4. Read reports, fix findings. After fixes: send updated diff to reviewers for next round.
   5. Max 3 review rounds. Reason: diminishing returns — if 3 rounds cannot resolve findings, the issue requires human judgment. If unresolved after 3 → message team lead to escalate.

   Commit flow:
   1. After implementation complete (tests pass): git commit `feat|fix: task {N} — {brief description}`
   2. Send diff to reviewers for review.
   3. After each round of fixes (tests pass): git commit `fix: address review round {M} for task {N}`
   4. After all reviews pass (or max 3 rounds): git commit review reports with message `chore: review reports for task {N}`
   ```

   If task has `reviewers: none` — skip reviewer spawning. The teammate works independently, commits code with message `feat|fix: task {N} — {brief description}` (tests pass), and reports completion directly to team lead.

   **Each reviewer** (when present) — `subagent_type: "{reviewer_agent}"`, `model: "sonnet"`, `team_name: "{team}"`

   Prompt template:

   ```
   You are reviewer "{name}" for task {N}.

   Read specs: {feature_dir}/user-spec.md, {feature_dir}/tech-spec.md
   Read task: {feature_dir}/tasks/{N}.md

   Wait for a message from teammate "{teammate_name}" with git diff of changes.

   When you receive it:
   1. Perform your review based on the changed files list and diff provided
   2. Write JSON report to: {feature_dir}/logs/working/task-{N}/{reviewer_name}-round{round}.json
   3. Send report path to teammate "{teammate_name}" via SendMessage

   The teammate may send updated diffs for subsequent rounds (max 3).
   Review each round the same way. After the final round, shut down.
   ```

4. All agents work in parallel. Lead waits for teammates to report "Task complete."

### Audit Wave tasks

Audit Wave tasks (Code Audit, Security Audit, Test Audit) have `reviewers: none` — each auditor teammate IS the review. Spawn them as standard teammates (general-purpose, opus), each loads its methodology skill.

Each auditor:
- Reads decisions.md to understand what was done in each task
- Reads all source files listed in tech-spec "Files to modify" across all implementation tasks
- Reviews the final state of code holistically (full files, not diffs)
- Writes report to `{feature_dir}/logs/working/audit/{auditor-name}.json`
- Writes decisions.md entry, reports to lead

After all 3 reports:
- All clean → proceed to Final Wave
- Issues found → spawn a fixer teammate (ad-hoc, code-writing skill), assign the auditors who found issues as reviewers, standard review protocol (max 3 rounds). After approval → proceed to Final Wave. If unresolved after 3 rounds → escalate (see Escalation).

### Ad-hoc agents

When lead spawns an agent outside the original execution plan (to fix audit findings, handle escalations, complete missing work):

1. Lead assigns a skill and reviewers matching the type of work:
   - Code changes → skill: `code-writing`, reviewers: code-reviewer, security-auditor, test-reviewer
   - Prompt changes → skill: `prompt-master`, reviewers: prompt-reviewer
   - Skill changes → skill: `skill-master`, reviewers: skill-checker
   - Deploy/CI changes → skill: `deploy-pipeline`, reviewers: deploy-reviewer
   - Infrastructure changes → skill: `infrastructure-setup`, reviewers: infrastructure-reviewer, security-auditor
   - Other tasks (research, config, manual steps) → no skill, no reviewers. Agent follows lead's instructions directly.
2. The ad-hoc agent writes a decisions.md entry (same template as planned tasks)
3. Standard review protocol: agent commits → sends diff to reviewers → fix → max 3 rounds
4. Lead verifies decisions.md entry exists before considering ad-hoc work complete

**Checkpoint:** all teammates reported "Task complete", decisions.md entries written.

## Phase 3: Wave Transition

0. **Build check (mandatory).** Run full production build (`npm run build` or equivalent) after each wave completes. Unit tests don't catch server/client boundary violations, callback type mismatches, or runtime-only import errors — only build does. If build fails, fix before proceeding.
1. Verify decisions.md entries exist and match template (`~/.claude/shared/work-templates/decisions.md.template`)
2. If task had Smoke/User verification steps — confirm decisions.md Verification section includes results. Missing results without explanation → ask user whether to proceed.
3. Update task frontmatter: `status: in_progress` → `status: done` (or `done_with_concerns` if teammate reported concerns — preserve the `concerns:` field from decisions.md entry into task frontmatter)
4. Git commit: `chore: complete wave {N} — update task statuses and decisions`. Code is already committed by teammates.
5. Update `work/{feature}/logs/checkpoint.yml`: set `last_completed_wave`, update task statuses, set `next_wave`.
   At session boundary: explicitly commit checkpoint.yml even if no code changed in the last wave — next session must start with accurate state.
6. **Session boundary check** (skip if session-plan.md does not exist):
   Read session-plan.md. If current wave is the **last wave of current_session**:
   a0. **Quick Learning (subagent, background).** Spawn a subagent to run [quick-learning](../quick-learning/SKILL.md). Pass it: feature path, current session number, path to decisions.md. The subagent runs in the **background** while you proceed with the session report. When it finishes, show the user its one-line summary. Do NOT read the quick-learning SKILL.md yourself — the subagent loads it independently in its own context.
   a. Increment `current_session` in checkpoint.yml.
   b. Generate next-session prompt from template `~/.claude/shared/work-templates/session-prompt.md.template`:
      - Fill: feature name, description (first line of tech-spec Description), completed sessions/waves, next session's waves and tasks, context files from session-plan.md.
      - Apply prompt-master principles to the generated prompt before saving: make it concrete (specific files, wave numbers, task names), remove filler phrases, lead with the goal, not the context.
   c. Save prompt to `work/{feature}/logs/next-session-prompt.md` (overwrite each time).
   d. Present to user:
      ```
      Сессия {N} из {total} завершена.

      Рекомендую начать новую сессию Claude Code и вставить этот промт:

      ---
      {generated prompt content}
      ---
      ```
   e. **STOP execution.** Do not proceed to next wave. End the session here.

   If current wave is NOT a session boundary → proceed to Phase 2 for next wave.
7. Next wave → Phase 2

**Checkpoint:** all wave tasks done, committed, checkpoint updated.

## Phase 4: User Review

All waves done including Final Wave (QA, deploy if applicable, post-deploy verification if applicable).

1. Show results: what was built, key decisions, QA report summary
2. Describe what to check manually (from execution plan "user checks" section)
3. Issues found → fix → review → commit (max 3 rounds). If unresolved → escalate (see Escalation).
4. All ok → finalize, shutdown team, delete `work/{feature}/logs/checkpoint.yml`

## Escalation

Call user when:
- 3 review/fix iterations exhausted with remaining findings
- Teammate reports blocker or ambiguous requirement
- Task depends on unavailable MCP tool or external service

When escalating:
1. Stop all work on the blocked task/wave
2. Report to user: what failed, what was tried (all 3 attempts), what remains unresolved
3. Write decisions.md entry: summary of attempts + unresolved findings
4. Git commit: `chore: escalate task {N} — unresolved after 3 fix rounds`
5. Wait for user decision before continuing

## Promoted Patterns

- **Спорные решения ДО генерации:** Перед генерацией артефакта > 200 строк — выписать список решений с неоднозначностью, предложить варианты с пояснением последствий, генерировать ПОСЛЕ утверждения. Один раунд обсуждения вместо серии переделок.
- **Субагент не завершил задачу — выполни напрямую:** Если субагент прерван (rejection, блокировка, ошибка записи) — lead немедленно выполняет задачу сам через Write/Edit, не ретраит субагент. Повторный spawn не поможет если причина — внешняя (права, permission-блок).
- **Новый sentinel/marker в промте — описать во всех секциях:** При добавлении нового маркера в агентный промт — перечислить все секции и таблицы где маркер может появиться, прописать обработку в каждой. Частичное описание гарантирует major review findings.

- **False-positive test finding — немедленный fix** (Seen: 2): Если audit wave нашла major finding с false-positive risk (тест зелёный, но покрытие иллюзорно) — создать ad-hoc fix task немедленно, не откладывать в deferred. Тест с false-positive risk ломает доверие ко всему test suite.
- **Флаг-файл run-once — путь от якоря, не от CWD** (Seen: 2): Если задача создаёт state-файл (флаг, lock, checkpoint), привязывай его путь к стабильному anchor: `db_path.parent`, `Path(__file__).parent` или `settings.BASE_DIR`. Относительный `Path("data/...")` разрешается от CWD — а CWD у cron-процесса и dev-окружения разные. Перед approving AC задачи с флаг-файлом — проверь anchor.
- **Верифицируй результат, а не только изменение** (Seen: 3): После любого деплоя или изменения — проверь что результат работает в реальной среде, не только что изменение применено. Для cron-деплоев: проверь лог через 5 минут после первого срабатывания. Объявлять "работает" без проверки реального лога — ошибка.
- **Off-by-one в позиционном форматировании — верифицируй на конкретном примере** (Seen: 2): При вычислении 1-based row/column индексов из динамически строящихся структур — подставить конкретные числа и проверить вручную до записи. Off-by-one смещает форматирование на соседнюю строку, визуально неотличимо от правильного.

## Self-Verification

- [ ] Execution plan created and approved
- [ ] All tasks executed, reviewed where applicable (max 3 iterations each), decisions.md filled
- [ ] All waves committed (including Final Wave)
- [ ] User reviewed and approved

## Learned Patterns

- When spawning reviewer agents -> spawn AFTER the teammate's diff is ready, passing the diff directly in the prompt; spawning before diff exists causes reviewers to complete before there is anything to review
- When entering post-deploy user review -> plan 2-4 UX correction iterations as the norm; UX adjustments are not process failures
- When code review identifies an error pattern (not a one-off bug) -> add an explicit warning to the next teammate's prompt to prevent recurrence in subsequent tasks
- When running code/security audit in a multi-task feature -> maintain a known-issues.md that auditors read before reviewing, to avoid re-reporting already-known issues
- When discussing architectural decisions with a non-technical user -> use the user's own language and decode each technical term, to accelerate decision-making
- When writing smoke verification for a markdown artifact -> check structural elements (phases, links, guards present), not keywords, to confirm the artifact is complete rather than a stub
- When writing smoke commands that check file size -> use [ $(wc -l < FILE) -lt N ] instead of awk conditions, to prevent a false-passing size guard
- When a QA criterion requires a live call to a service unavailable in the test environment -> mark as deferred with an explicit condition, not as failed, to get a clean QA pass without blocking
- When a non-technical user is executing server commands -> give one command at a time and wait for the result before proceeding, to prevent pasting a block into the wrong context
- When deploying a new backend service on VPS -> run `ss -tlnp` before first start to see all listening ports, to avoid EADDRINUSE from an unexpected port conflict
- When Claude Code needs to run SSH commands on a VPS -> first ask the user to confirm SSH works manually (`ssh user@host echo ok`), only then attempt from Claude Code; rapid failed attempts can trigger fail2ban and block the IP
- When two fix variants are both correct -> apply TRIZ-ideality: choose the variant with zero maintenance cost and lower coupling, to avoid creating tech debt while fixing
- When an agent writes files to multiple directories before committing -> enumerate all write locations from the skill body before running git add, to avoid losing files outside the main tree
- When writing agent files for multi-context use (inline + spawn_agent) -> use a neutral completion signal, not a back-reference to the parent step, so the artifact works in both execution environments
- When writing grep-based smoke checks for markdown content -> verify the actual case of the target string in the file; add -i if case is unpredictable, to prevent false-negative AVP checks
- When Edit tool returns File-has-been-unexpectedly-modified on a shared file -> switch to atomic read-modify-write via script instead of retrying Edit, to avoid accumulating partial writes
- When two process steps are semantically linked (A must complete before B is shown) -> run A synchronously and wait for completion before executing B; background launch of A does not guarantee A completes first
- When production behavior does not match current code -> verify timestamp of deployed file against server process start time, to avoid debugging code that is already correct
- When executing deploy commands in a client project -> clarify server ownership and agree on deploy process BEFORE executing, to avoid unauthorized production changes
- When asked to update a single system component -> invoke only that component in isolation through a minimal script, to avoid triggering side effects from the full pipeline
- When pre-deploy QA is complete and the user is in local-first or sketch mode -> clarify the desired deploy environment BEFORE launching deploy wave, to avoid preparing VPS deploy for a user who is not ready for it
- When UI demonstration is blocked by a non-working infrastructure dependency -> mock the dependency locally in the component, to unblock UX evaluation
- When SSH key auth fails despite correct authorized_keys -> check ls -la ~ to verify home directory ownership belongs to the user, to resolve auth blocker without touching sshd_config
- When browser shows not-loading without an error -> check server access log before diagnosing the network layer, to avoid diagnosing the wrong layer
- When diagnosing nginx external inaccessibility -> run nginx -T | grep server_name to detect conflicting server blocks in one step
- When a service is accessible via curl but mobile browser hangs -> clarify domain-or-IP before network diagnostics, to avoid diagnosing the wrong layer
- When a subagent reports a blocker as the reason for an incomplete task -> run the same command independently before accepting the agent's diagnosis as fact
- When a subagent completes a task -> explicitly update status: done in the task file frontmatter to avoid accumulating planned tasks that require manual batch updates
- When user asks to change a schedule from-tomorrow and a run is imminent -> check the next scheduled run time and apply the change AFTER it, to preserve the planned run
- When QA wave includes integration/E2E tests requiring a DB -> verify DB connection with a single ping query BEFORE launching test suites, to avoid wasting the QA wave on an infrastructure blocker
- When an ad-hoc fix task is needed but agent spawning tools are unavailable -> perform inline review by the lead using the reviewer checklist instead of skipping review
- When a metric shows a logically impossible value (A < B where A should be >= B) -> establish the semantic definition of each metric BEFORE tracing code, to find the structural bug instead of masking the symptom
- When a DB field contains a value in the wrong format -> find ALL write paths to that field including legacy code and schema defaults before creating cleanup scripts
- When formulating residual problems in the session-end prompt -> verify each problem against what the user sees in UI/output, not against internal code state, to avoid directing the next session at a misidentified problem
- When deploying to VPS for the first time or after changing domain/secrets -> run SSH smoke (ssh -i deploy_key user@host echo ok) locally BEFORE pushing to main, to avoid cycling through multiple redeploy triggers for sequential infrastructure blockers
- When a feature writes files to disk in a directory that may not exist -> explicitly include mkdir for that directory in the deploy checklist, to avoid ENOENT on the first upload after deploy
- When user says a name/value looks wrong without specifying the field or expected output -> ask "what exactly do you expect to see and where" before diagnosing, to avoid wasting an iteration on the wrong version of the problem
- When a skill assumes interactive data collection but the task already contains all required fields -> skip interview phases and go directly to showing the extracted structure for confirmation, to minimize turns without losing verification
- When an audit wave finds an open security risk in a product handling sensitive data -> create an ad-hoc fix task and resolve it BEFORE launching the QA wave, to avoid deploying with a known data leak and wasting QA on a fixable failure (triad #136)
- When a user executes a multi-step process and their current branch or external state is unknown -> ask one clarifying question about the state BEFORE giving instructions, then give one step at a time and wait for the result (triad #40)
