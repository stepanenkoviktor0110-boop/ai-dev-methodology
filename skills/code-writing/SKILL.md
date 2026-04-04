---
name: code-writing
description: |
  Universal quality coding process: plan, TDD, reviews.
  Use whenever code needs to be written — ad-hoc or as part of a task.

  Use when: "напиши код", "закодь", "реализуй", "write code", "implement"

  For planning tasks → tech-spec-planning skill. For specs → user-spec-planning skill.
---

# Code Writing

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Before starting, read [quick-ref-code-writing.md](../quick-learning/references/quick-ref-code-writing.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Preparation

1. **Parse Requirements**
   - Extract what needs to be built from user message or passed acceptance criteria
   - Clarify ambiguities — ask user if unclear
   - Formulate acceptance criteria (what "done" looks like)

2. **Read Project Context (Graceful)**

   **Working on a task?** Read all files listed in the task's "Context" section — it already specifies everything needed.

   **Standalone (no task file)?** Read (skip if missing):
   - `.claude/skills/project-knowledge/references/project.md` — project overview
   - `.claude/skills/project-knowledge/references/architecture.md` — system structure
   - `.claude/skills/project-knowledge/references/patterns.md` — project conventions

   Then read `.claude/skills/project-knowledge/SKILL.md` (if exists).
   Consider which domain-specific guides are relevant to your task and read those
   (e.g., `architecture.md` Data Model section for DB work, `ux-guidelines.md` for UI tasks).

   **No project patterns?** Apply baseline from [universal-patterns.md](references/universal-patterns.md) — naming, error handling, structure.

   **Design tokens (conditional).** If ALL conditions are true:
   - `.design-system/tokens.json` exists in the project root
   - File size is under 50 KB
   - File contains valid, non-empty JSON
   - The task touches at least one UI file (`.css`, `.scss`, `.tsx`, `.html`, `.vue`, `.svelte`)

   Then read `.design-system/tokens.json` and keep it as passive reference for Phase 2 (context budget: ~500-1000 tokens — the 50 KB size guard keeps the file manageable).

   **Standalone (no task file)?** Check if the files you are about to create or modify include any UI extension (`.css`, `.scss`, `.tsx`, `.html`, `.vue`, `.svelte`).

   **Silent skip** (no error, no message) if any condition above is not met.

3. **Analyze & Review Approach**

   Before coding, output your findings:
   - Grep for usages of code to be modified
   - Read all files that will be changed
   - Verify solution follows project patterns (or universal patterns)
   - Identify existing code that can be reused
   - If modifying existing code, run existing tests for the area to establish baseline

   If concerns → discuss with user before proceeding.

**Checkpoint:** List completed preparation steps before moving to implementation.

## Phase 2: Implementation (TDD)

1. **Write Tests First**

   **Before writing tests**, read [testing-guide.md](references/testing-guide.md) — when to write which test type, test structure.

   - Write tests for: business logic, validations, transforms, error handling. Skip trivial code without logic (simple getters, one-liners, configs)
   - Write tests for requirements and edge cases
   - Tests should fail initially (no implementation yet)
   - One test = one scenario, test behavior not implementation
   - If mocking >3 dependencies → wrong test type, use integration test

2. **Write Code**
   - Implement to pass tests
   - Follow project patterns (from Phase 1) or apply baseline from [universal-patterns.md](references/universal-patterns.md)
   - Use env vars for secrets, validate inputs at boundaries
   - Handle edge cases, comment WHY not WHAT
   - **Design tokens in UI code.** If tokens.json was loaded in Phase 1, use CSS custom properties (`var(--color-primary-500)`) instead of hardcoded values (`#3B82F6`, `16px`). Use category aliases to derive variable names:

     | JSON category prefix | CSS variable prefix |
     |---|---|
     | `colors` | `--color` |
     | `typography.families` | `--font` |
     | `typography.sizes` | `--font-size` |
     | `typography.weights` | `--font-weight` |
     | `typography.lineHeights` | `--line-height` |
     | `spacing` | `--space` |
     | `radii` | `--radius` |
     | `shadows` | `--shadow` |
     | `breakpoints` | `--breakpoint` |

     Append the remaining key path with hyphens: `colors.primary.500` → `--color-primary-500`, `typography.families.heading` → `--font-heading`, `typography.sizes.base` → `--font-size-base`, `spacing.4` → `--space-4`, `radii.md` → `--radius-md`, `shadows.md` → `--shadow-md`.

     For categories not in this table, use `--{category}-{remaining-path}` with hyphens as separators.

3. **Run Tests**
   - All new tests pass
   - Fix any failures

**Checkpoint:** List implemented functionality and test results.

## Phase 3: Post-work

1. **Run Lint/Format**
   - Run project's linter and formatter before reviews

2. **Run Relevant Tests**
   - Tests for files changed
   - Tests mentioned in task (if applicable)
   - Save full test suite for end of feature

3. **Smoke Verification** (if task has Verification Steps → Smoke or User)

   Execute each command from the Smoke section. Record results in decisions.md Verification section.
   If a check fails — fix the code before proceeding to reviews.
   If the task has User checks — ask the user to verify, wait for confirmation.

   Smoke catches integration bugs that mocked tests miss:
   real API responses, library initialization, config validity.

4. **Post-Generation Guard**

   Load [quick-ref-code-writing.md](../quick-learning/references/quick-ref-code-writing.md) as text reminders (if file exists). Scan all code generated or modified in this task for the following violations:

   **Check 1 — Secrets in log calls:**
   Grep generated code for `.env`, `password`, `secret`, `token`, `api_key` appearing inside `console.log`, `print`, `logger.*` or similar logging calls.
   If found → remove the secret from the log call immediately.

   **Check 2 — Missing timeout in HTTP calls:**
   Check all `fetch()`, `axios.*()`, `requests.*()` calls for a timeout parameter.
   If a call lacks timeout → add a 30 s timeout.

   **Check 3 — Missing cache/dedup on rate-limited API calls:**
   Check external API calls that may be rate-limited for cache or dedup logic.
   If repeated calls to the same endpoint without caching → add caching or dedup.
   If using a paid API with quota limits and data that can overlap between runs → cache processed records in DB with explicit skip-known logic across runs (not just per-session dedup), to avoid spending quota on already-processed data.

   **Fix-and-reinforce:** if any violation is found, fix the code before proceeding.
   After fixing, check whether the violation matches a trigger in
   [triad-index.md](../quick-learning/references/triad-index.md). If it matches →
   increment that pattern's Seen counter by 1.

5. **Run Reviews** (launch in parallel)

   **Working as part of a team** (received reviewer instructions from team lead via SendMessage)? Follow team protocol instead of steps below — team lead manages reviewer flow.

   **Reviewer selection:**
   - Working on a task file → run reviewers from the task's "Reviewers" section
   - Standalone (no task file) → default: code-reviewer, security-auditor, test-reviewer

   For each reviewer:
   1. Spawn subagent via Task tool (subagent_type = reviewer name, e.g. `code-reviewer`)
   2. Pass: git diff of changes, path to task file, path to tech-spec, path to user-spec
   3. Reviewer loads its own skill automatically (via agent frontmatter `skills:`)
   4. Report path: from the task's "Reviewers" section (or `logs/working/` if standalone)

   Reviewers write JSON reports to `logs/working/task-{N}/{reviewer-name}-{round}.json`.
   `{N}` = task number from task file; `"standalone"` if no task file.
   On re-review: new file with incremented round number, old file stays.

6. **Process Findings**

   Evaluate each finding on merit — severity is metadata, not a filter.
   A valid minor fix still improves quality. Reason: skipping valid findings
   silently degrades the codebase over time.

   For each finding:
   - **Valid, improves code** → apply (any severity: critical, major, minor, low)
   - **Disagree or uncertain** → discuss with user (explain reasoning)
   - **Out of scope** → skip, note in findings log

   Produce a findings log:
   | # | Source | Severity | Finding | Action | Reason |
   Each finding appears in this table — transparent decision trail.

   After applying fixes → re-run tests → re-run the reviewer(s) that reported them.
   Limit: 3 review iterations. If findings remain after round 3 → ask user.
   Reason: fixes can introduce new issues — a second pass catches regressions.

**Checkpoint:** List post-work steps completed.

## Self-Verification

Verify each item before marking complete. If any item fails, return to the relevant phase.

- [ ] All phases completed (Preparation, Implementation, Post-work)
- [ ] Tests pass
- [ ] Smoke verification executed (if task had Smoke/User checks)
- [ ] Each reviewer finding evaluated and logged
- [ ] Findings log table produced
- [ ] Review JSON reports saved to `logs/working/task-{N}/`
- [ ] Design tokens used via CSS custom properties for UI files (if tokens.json was loaded)


## Promoted Patterns

- **Маскируй секреты ДО выполнения команды** (Seen: 2): при любом чтении конфигов удалённой машины — встраивать маскировку в команду (`sed 's/:[^@]*@/:***@/'`) или проверять наличие переменной через `grep -c`. Никогда не выводить `.env` целиком.
- **Assertions на output-формат, не на input-атрибуты** (Seen: 2): перед написанием assertions прочитать реальный пример вывода функции. Для format-conversion функций (JSON→MD, dict→текст) assertions должны соответствовать output-формату — иначе тест проверяет input surface и не ловит баги конвертации.
- **Path traversal из любых внешних данных — allowlist** (Seen: 2): Перед построением файлового пути из любого внешнего значения (данные с диска, user input, API-параметры) — валидировать каждое значение против allowlist. Даже значения, записанные самим приложением, могут быть изменены между записью и чтением.

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during code writing.

- When useMemo dependency ссылается на промежуточный массив созданный в render → вынести null-guard/нормализацию внутрь вычисляющей функции, dependency — исходный prop/state, to гарантировать стабильность референса и реальную работу мемоизации
- When проект с "type":"module" и нужен CommonJS cron-скрипт с require() → именовать .cjs и использовать DI: main(_dep = require('dep')), to избежать runtime ошибки ESM и vi.mock-хаков при тестировании
- When написание теста для finally-блока с except Exception → использовать BaseException (например KeyboardInterrupt) как trigger, to гарантировать что finally реально выполняется при любом исходе
- When скрипт с дорогостоящей инициализацией (auth flow, DB connection) создаёт объект внутри цикла → вынести init за цикл и указать явно в spec, to предотвратить дублирование auth flow и N лишних round-trips
- When кнопка делает async-запрос (destructive action или оптимистичный UI) → добавить disabled+loading state на время запроса AND .catch() восстанавливающий state при ошибке — до первого review, to предотвратить fix-раунд на предсказуемый UX concurrency guard
- When расширение API-ответа новым полем → grep тесты на exact-equality assertions для этого endpoint, to не допустить отложенного тест-фейла в следующей сессии
- When задача требует повторного чтения файла, файл не менялся → прочитать файл один раз в начале, не читать повторно, to не расходовать токены на повторное чтение неизменного файла
- When несколько git репо в одной bash сессии → всегда указывать `git -C /path/repo` вместо надежды на рабочую директорию, to избежать silent failures от команд из неправильного репо
- When нужно изучить внешнее репо (GitHub) или прочитать >5 файлов подряд в главной сессии → делегировать сканирование Explore subagent'у одним вызовом, to не исчерпать контекст главной сессии
- When React компонент хранит typed async данные, UI переключает режим/таб → сбросить data в [] в начале useEffect + type guard перед рендером типизированных полей, to предотвратить TypeError из промежуточного рендера со stale typed данными
