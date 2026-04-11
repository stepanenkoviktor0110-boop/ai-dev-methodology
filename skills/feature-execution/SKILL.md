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
1.6. **Codex mode** (opt-in, skip if `codex_mode` absent or false in checkpoint.yml):
   - Set at feature start via `--codex` flag → writes `codex_mode: true` to checkpoint.yml
   - Read and cache `~/.claude/skills/quick-learning/references/triad-index.md` for prompt injection
   - Read and cache `.claude/skills/project-knowledge/references/patterns.md` if file exists and < 2KB
   - If `codex_mode: false` or absent → standard Claude-only flow, skip all "Codex mode" blocks below
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

### Codex-First Routing (skip if `codex_mode: false`)

   For each task, determine executor before spawning:

   **Claude-only** (auto-override):
   - Task has `verify: [smoke]` or `verify: [user]` (needs dev-server/browser)
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
   a00. **Update project-knowledge** (before generating the next-session prompt): check if roles, architecture, or business rules changed during this session — update the relevant `.claude/skills/project-knowledge/` docs so the next session does not re-ask what was already discussed.
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
5. Prompt user: "Фича завершена. Запусти `/done` для архивации и обновления документации."

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

- **Спорные решения ДО генерации:** Артефакт > 200 строк → сначала список решений с вариантами → утверждение → генерация. Один раунд вместо серии переделок.
- **Субагент не завершил → выполни напрямую:** Не ретраить субагент при внешней блокировке (права, permission). Lead делает сам через Write/Edit.
- **Верифицируй результат в реальной среде** (Seen: 4): После деплоя — curl/лог/проверка. Не объявлять "готово" без подтверждения работы. Для cron — лог через 5 мин.
- **Codex: один файл за раз** (Seen: 1): Codex зависает при генерации множества файлов одним ответом. Промт должен содержать `<completeness_contract>` с инструкцией писать файлы по одному.
- **Codex: тесты прогоняет Claude** (Seen: 1): Codex sandbox не может запускать vitest/vite (spawn EPERM на Windows). Тесты всегда запускать локально после получения результата от Codex.

## Self-Verification

- [ ] Execution plan created and approved
- [ ] All tasks executed, reviewed where applicable (max 3 iterations each), decisions.md filled
- [ ] All waves committed (including Final Wave)
- [ ] User reviewed and approved

## Learned Patterns

Мета-правила, обобщённые из опыта. Детали в quick-learning triad-index.

**1. Серверные операции — проверяй preconditions:**
Перед deploy/restart/подключением → verify: занятость целевого порта, push state (`git log origin..HEAD`), ручная проверка подключения до автоматических попыток, количество процессов на порту. Серверные проблемы имеют физические причины (порт занят, ISP-блок, hung process) — проверяй их до дебага логики. Сервис недоступен с нескольких независимых сетей при открытом порте = проблема провайдера → туннель или смена IP. В deploy script — явно завершать зависшие процессы перед перезапуском сервиса, чтобы orphan-процессы не блокировали порт. Аутентификация по ключу падает при корректных ключах — проверить права на домашнюю директорию пользователя.

**2. Пользовательские инструкции — уточняй scope:**
"Не нужен" → уточни: UI или вся функциональность (API, DB)? "X здесь, а не там" → добавь в новое место, убери только из названного. Неоднозначное название → покажи варианты, спроси. Диагностический вопрос ≠ запрос на действие. Task file > prompt для значений.

**3. Любое изменение — проверяй радиус поражения:**
Изменён элемент из группы → примени к каждому sibling. Синхронизация файлов → проверь index-файлы. Hotfix вне плана → добавь в audit wave. Новый marker в промте → опиши во всех секциях. DRY-нарушение в N задачах → extraction-задача в audit. Validation добавлена в route → немедленно grep по имени поля во всех route-файлах, убедиться что structurally-similar endpoints имеют ту же validation. Смена домена → grep hardcoded CORS/CSRF/allowed_origins в кодовой базе и обновить ВСЕ до деплоя, иначе молчаливый 403 после переключения.

**4. Не подтверждай без проверки реальности:**
"Это работает?" → grep в коде до ответа. Pipeline ok но экспорт упал → алерт на N consecutive 0. Тесты зелёные но покрытие иллюзорно → ad-hoc fix немедленно. Pre-existing failures → проверь working tree (git stash).

**5. Планирование задач — валидируй зависимости:**
depends_on=[N] в той же wave → проверить wave(dep) < wave(task). Фильтр ко всем колонкам → таблица тип→поведение до кода. Endpoint с resource_id без user_id → проверка роли target-user. Off-by-one в индексах → подставить числа вручную. State-файл → путь от якоря (db_path.parent), не от CWD.

**6. Порядок вызовов — лог после накопления:**
When функция log_*() вызывается до стадии-накопителя метрики → перенести вызов в конец всех накопительных стадий, to гарантировать полноту записи в лог.

**7. Non-ASCII в HTTP-ответах:**
When файл с non-ASCII именем отдаётся через HTTP Content-Disposition → использовать RFC 5987 encoding (filename*=UTF-8''...) + ASCII fallback, to предотвратить ByteString crash и некорректное имя при скачивании.

**8. Shared state для UI табов:**
When общий state объект для нескольких UI табов с разными типами данных → защищать доступ к type-specific полям optional chaining или разделять state по табам, to предотвратить runtime crash при переключении табов из-за stale данных чужого типа.

**9. Tunnel URL после перезапуска:**
When сервис с free tunnel перезапустился → считать новый tunnel URL и немедленно передать клиенту, to не оставлять клиента со старым нерабочим URL.

**10. Проверка запретов из спека перед коммитом:**
When task-файл содержит явный запрет ("NEVER X"), реализация нарушает запрет → grep по запрещённому паттерну в изменённых файлах ДО коммита, to не тратить review round на нарушение явного запрета из спека.

**11. Async агент без прогресса — kill threshold:**
When мониторинг async AI-агента без нового прогресса → установить порог "5 мин без записи в лог = убить и перезапустить", to не тратить 15+ мин на polling заведомо зависшей задачи.

**12. Визуальная фича — по одному экрану:**
When визуальная фича с несколькими экранами/блоками → показать один экран/блок полностью → дождаться одобрения → следующий, to получить ранний фидбэк на каждый экран до следующего.

**13. Баг после деплоя — upstream сначала:**
When фикс задеплоен → баг воспроизводится → проверить upstream-инфраструктуру до повторного анализа кода, to не тратить ещё один цикл деплоя на не тот слой.

**14. Внешний агент (Codex) — полный diff:**
When делегирование точечных правок внешнему агенту (Codex) → проверить полный git diff после завершения, не только целевые файлы, to поймать непрошеные изменения до коммита.

**15. DNS-миграция — .env после propagation:**
When DNS-миграция: .env содержит домен который ещё не пропагировался → менять .env и пересобирать ПОСЛЕ подтверждения dig A → новый IP, не параллельно с nginx, to не ломать работающий сайт на период пропагации DNS.

**16. Агрегация ресурса из параллельных прогонов:**
When агрегация расхода ресурса из параллельных запусков → использовать pool_start − pool_end вместо SUM(individual_spent), to получить корректный совокупный показатель без двойного счёта.

**17. Стоимость многошагового API — верифицируй математику:**
When объяснение стоимости многошагового API-процесса клиенту → посчитать каждый шаг отдельно и сверить сумму с фактом до отправки, to не давать клиенту математически противоречивую картину расходов.

**18. «Сколько X» при 1→N разворачивании:**
When пользователь спрашивает «сколько X» когда пайплайн делает 1→N разворачивание → найти код трансформации и считать на выходной стороне, to дать метрику совпадающую с тем что пользователь видит.

**19. «Вчера/сегодня запускалось» — ориентируйся по датам:**
When пользователь говорит «вчера/сегодня запускалось» в контексте диагностики → сначала SELECT DISTINCT run_date ORDER BY DESC LIMIT 5 для ориентации, to не запрашивать данные за ошибочную дату.

**20. Код закоммичен — деплой сразу:**
When server-side код исправлен и закоммичен → задеплоить сразу как последний шаг сессии, to не допустить запуск продакшна со старым кодом.

**21. Расхождение с внешним биллингом — отложенное наблюдение:**
When расхождение между нашим измерением и внешним биллингом → проверить гипотезу отложенным наблюдением до реализации фикса, to не реализовывать фикс на непроверенной гипотезе.

**22. Бэклог с числовым примером — проверь через первопринципы:**
When бэклог содержит числовой пример противоречащий бизнес-логике фичи → проверить пример через первопринципы до кодинга, to не реализовывать неверный алгоритм по ошибочной спеке.

**23. Deploy script — два SSH-вызова вместо одного:**
When deploy.sh объединяет pkill + systemctl restart в один длинный SSH-вызов → разбить на два вызова: upload/config и restart/verify, to убедиться что сервис перезапущен даже если SSH рвётся.
