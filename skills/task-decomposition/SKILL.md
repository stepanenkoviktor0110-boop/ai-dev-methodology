---
name: task-decomposition
description: |
  Decompose approved tech-spec into atomic task files with parallel creation and validation.

  Use when: "разбей на задачи", "декомпозиция", "decompose tech-spec",
  "создай задачи из техспека", "/decompose-tech-spec"
---

# Task Decomposition

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Decompose tech-spec Implementation Tasks into individual task files with parallel creation and validation.

Before starting, read [quick-ref-task-decomposition.md](../quick-learning/references/quick-ref-task-decomposition.md) — top reasoning patterns for this skill (if file exists and non-empty).

**Input:** `work/{feature}/tech-spec.md` (status: approved)
**Output:** `work/{feature}/tasks/*.md` (validated)
**Language:** Task files in English, communication in Russian

## Phase 0: Scope Estimation

Before creating tasks, present the user a structural plan:

1. Read tech-spec Implementation Tasks section.
2. Estimate total lines of code for the feature.
3. **Break down into blocks of ~1200 lines (±300)**, each block into **steps of ~300 lines (±100)**.
4. Present the plan as a table: blocks → steps with line estimates. Add a **Complexity** column:
   - **L1** (trivial) — estimated_loc < 50 AND task description contains none of: auth, login, password, token, session, input validation, upload, file input, database query, SQL, API endpoint, CORS, RBAC, permission
   - **Standard** — everything else

   L1 tasks get `reviewers: [code-reviewer]` only (security-auditor and test-reviewer skipped). Audit Wave covers security holistically at feature level regardless.

5. Get user confirmation before proceeding to task creation.

This ensures predictable scope, manageable task sizes, and clear progress tracking. Each "step" typically maps to one task file. Each "block" maps to a wave or a group of related tasks.

**Important:** Save LOC estimates per task — they will be used in Phase 4 (Session Planning). Pass `estimated_loc` to each task-creator in Phase 1.

## Phase 1: Create Tasks

1. Ask user for feature name if not provided.

2. Read `work/{feature}/tech-spec.md`. Check frontmatter `status: approved`.
   If not approved — tell user: "tech-spec не утверждён. Сначала запусти `/new-tech-spec` и доведи до approved." Stop.

3. Read `work/{feature}/user-spec.md`.

4. Note the task template path: `~/.claude/shared/work-templates/tasks/task.md.template`

5. Read skills/reviewers catalog from [skills-and-reviewers.md](~/.claude/skills/tech-spec-planning/references/skills-and-reviewers.md) — for passing correct skills/reviewers to task-creators.

6. For each task in Implementation Tasks — launch [`task-creator`](~/.claude/agents/task-creator.md) subagent in parallel.
   Pass each task-creator:
   - feature_path, task_number, task_name
   - template_path: `~/.claude/shared/work-templates/tasks/task.md.template`
   - files_to_modify, files_to_read (from tech-spec)
   - depends_on, wave, skills, verify (from tech-spec)
   - reviewers: if task was classified **L1** in Phase 0 → pass `[code-reviewer]`; otherwise pass reviewers from tech-spec
   - teammate_name (if specified in tech-spec, optional)
   Each task-creator copies the template to `tasks/{N}.md` first, then edits each section in place. This ensures no sections are skipped.

7. Confirm each task-creator returned a file path. Skip reading task content — preserve context budget for validation phase.
8. Git commit: `draft(tasks): create {N} tasks from tech-spec for {feature}`

**Checkpoint:**
- [ ] All `tasks/*.md` files created
- [ ] Each task-creator returned file path
- [ ] Draft committed

## Phase 2: Validation (up to 3 iterations)

Tech-spec was already validated by 5 validators. This phase checks only: (1) task-creator correctly expanded tasks by template, (2) no mismatches with real code appeared during detailing.

### Validators

Launch both in parallel:

[`task-validator`](~/.claude/agents/task-validator.md) (sonnet) — Template Compliance + AC/TDD carry-forward:
- Batch: 5 tasks per call
- Pass: feature_path, task_numbers array, batch_number, iteration
- Report: `logs/tasks/template-batch{N}-review.json`

[`reality-checker`](~/.claude/agents/reality-checker.md) (sonnet) — Reality & Adequacy:
- Batch: 3 tasks per call
- Pass: feature_path, task_numbers array, batch_number, iteration
- Report: `logs/tasks/reality-batch{N}-review.json`

### Process

1. Launch both validators in parallel (task-validator in batches of 5, reality-checker in batches of 3).
2. Read JSON reports, collect findings.
3. If issues found — for each task with issues, launch [`task-creator`](~/.claude/agents/task-creator.md) in fix mode:
   - Pass: same inputs as creation + `mode: fix` + `findings` from validators
   - task-creator reads existing task, applies fixes, overwrites file
4. After each validation round, git commit: `chore(tasks): validation round {N} — {summary}`
5. Re-validate fixed tasks (repeat 1-4). Maximum 3 iterations.
6. If problems remain after 3rd iteration — show user: "Вот что осталось — давай решим вместе."

### Cross-Task Integration Check

After individual validation passes, run a final cross-task check:

1. Launch both validators on ALL tasks in a single batch (not split into smaller batches):
   - `task-validator` — focus: shared resource ownership (one owner, consumers depend_on owner), no competing instances in same wave
   - `reality-checker` — focus: duplicate heavy resource init, hidden dependencies, inconsistent approaches across tasks

2. If issues found → launch `task-creator` in fix mode for affected tasks. Re-validate fixed tasks.

3. Max 2 iterations for cross-task check (on top of the 3 individual iterations).

**Checkpoint:**
- [ ] Both validators: status=approved OR user resolved remaining issues
- [ ] Cross-task integration check: no cross-task conflicts

## Phase 3: Present to User

1. Summary: task count, waves, dependencies, validation results (iterations, issues found/fixed).
2. Wait for user approval.
3. Git commit: `chore(tasks): task decomposition approved for {feature}`

**Checkpoint:**
- [ ] Summary presented to user
- [ ] User approved task decomposition
- [ ] Approval committed

## Phase 4: Session Planning

After user approves task decomposition, calculate session grouping for predictable execution.

1. Read all task files, collect per task: `wave`, `estimated_loc`, Context Files list.
2. Group waves into sessions using LOC budget:
   a. **Session LOC budget = ~1200 lines (±300)** — matches Phase 0 block size.
   b. Walk waves in order. For each wave, sum `estimated_loc` of its tasks.
   c. Accumulate wave LOC into current session. If adding next wave exceeds budget → start new session.
   d. **Never split a wave across sessions.**
   e. **Audit Wave + Final Wave → always the last session** (fixed, no LOC budget — these are review & deploy).
   f. If a single wave > budget → it gets its own session (warn user: "Wave N exceeds session budget").
3. For each session, collect unique Context Files from all tasks in that session (deduplicate).
4. Give each session a short descriptive title based on its tasks' descriptions.
5. Generate `work/{feature}/logs/session-plan.md` from template `~/.claude/shared/work-templates/session-plan.md.template`. Include prompts for ALL sessions in the file (for reference).
6. Present session plan to user as a table: session number, title, waves, tasks, estimated LOC.
7. Git commit: `chore(tasks): session plan for {feature} — {N} sessions`
8. Show ONLY the prompt for Session 1. Do NOT show prompts for later sessions — they are in session-plan.md and will be delivered by feature-execution at the end of each session.

**Checkpoint:**
- [ ] session-plan.md created and committed
- [ ] User saw session grouping

## Final Check

- [ ] All phases completed (tasks created, validation passed)
- [ ] All tasks match template (frontmatter: status, depends_on, wave, skills, reviewers, teammate_name)
- [ ] Validation: both validators passed or user confirmed remaining issues

## Promoted Patterns

**Verify all cross-references after task generation (Seen: 2):** Check file paths via `test -e`, decision numbers by counting in tech-spec, depends_on by confirming the dependency actually produces the referenced artifact. Agents generate references by analogy/assumption, not by verification.

**Тест на стыке задач — добавить явно в spec/AC (Seen: 2):** Если при выполнении Task N обнаруживается тест, относящийся к scope Task M — добавить его явно в AC или TDD Anchor задачи M. Записи в decisions.md недостаточно: агент Task M decisions.md предыдущих задач не читает.

**Wave поля Audit/Final Wave — числа, не метки (Seen: 2):** Если имплементационных волн N — audit = N+1, final = N+2. Передавать task-creator числа явно. Строки "audit"/"final" не проходят frontmatter schema-validation.

**String-output assertions — ограничивай scope (Seen: 2):** Для тестов структурированного string-output (markdown, отчёты) недостаточно проверять наличие значения — добавь assertion на scope: извлекай нужную секцию (regex/split), затем проверяй значение внутри неё. Это отличает "значение есть" от "значение в нужном месте".

**Scope задач разных волн для одного файла (Seen: 2):** Если задача A создаёт файл а задача B в позднейшей волне его расширяет — явно ограничить scope A ("только save/load — нужны в wave 1"), и в бриф B включить: "файл уже существует с функциями X, Y. Добавить только Z." Параллельные task-creator'ы не общаются — scope должен быть однозначен в каждом брифе.

**Wave ordering: последовательные задачи внутри одной "названной волны" (Seen: 2):** Если tech-spec называет группу "Final Wave" — это семантическая метка, не число. Если задачи внутри группы зависят друг от друга (A→B→C) — каждая получает своё число: A=N, B=N+1, C=N+2. Проверять после генерации: wave(задача) > max(wave(depends_on)).

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during task decomposition.
