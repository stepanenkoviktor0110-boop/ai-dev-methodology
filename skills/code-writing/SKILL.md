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

## ⛔ Communication Rule — override all defaults

When communicating with the user during code writing: use only plain, non-technical language. Describe what the code *does* and *why* — not how it works internally. No class names, method signatures, library names, or implementation details in explanations. If the user needs to make a decision → describe it as a product/logic choice, not a technical one.

## ⛔ Scope — override all defaults

Deliver what was asked, at the scope intended. Make routine judgment calls yourself; check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked — do not quietly narrow, widen, or transform it. Finish the whole task; stop short of actions clearly beyond it.

Out of scope unless asked: refactoring adjacent code, adding configurability, adding error handling for scenarios that cannot happen, adding docstrings or types to code you did not change, creating abstractions for one-time operations.

Work directly rather than delegating. Spawn a subagent only for a genuinely independent, sizeable track — a wide multi-file investigation you cannot finish in a handful of tool calls. Never spawn one to verify or double-check your own work.

## ⛔ Karpathy Rules — override all defaults below

**1. Think Before Coding**
Before writing a single line: name the assumptions the task rests on. Resolve the routine ones yourself. Stop and ask only where two readings would produce materially different code — then present the readings instead of picking silently.

**2. Simplicity First**
Write the minimum code that solves the problem. No abstractions for single-use code. No flexibility or configurability that wasn't requested. No error handling for impossible scenarios. If you write 200 lines and 50 would do → rewrite it. Test: "Would a senior engineer say this is overcomplicated?" If yes → simplify before continuing.

**3. Surgical Changes**
Every changed line must trace directly to the user's request. Don't improve adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style even if you'd do it differently. If YOUR changes create orphan imports/variables/functions → remove them. Pre-existing dead code → mention it, don't touch it.

---

Before starting, read [quick-ref-code-writing.md](../quick-learning/references/quick-ref-code-writing.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Preparation

1. **Parse Requirements**
   - Extract what to build, clarify ambiguities, formulate acceptance criteria

2. **Read Project Context (Graceful)**

   **Working on a task?** Read all files listed in the task's "Context" section.

   **Standalone (no task file)?** Read (skip if missing):
   - `.claude/skills/project-knowledge/references/project.md` — project overview
   - `.claude/skills/project-knowledge/references/architecture.md` — system structure
   - `.claude/skills/project-knowledge/references/patterns.md` — project conventions
   Then read `.claude/skills/project-knowledge/SKILL.md` (if exists) and relevant domain guides.

   **No project patterns?** Apply baseline from [universal-patterns.md](references/universal-patterns.md).

   **Design tokens (conditional).** Read `.design-system/tokens.json` as passive reference IF: file exists, <50 KB, valid JSON, AND task touches UI files (`.css`/`.scss`/`.tsx`/`.html`/`.vue`/`.svelte`). Silent skip if any condition unmet.

3. **Design Context (UI only — conditional)**

   Applies IF the task touches UI files (`.css`/`.scss`/`.tsx`/`.jsx`/`.vue`/`.svelte`/`.html`) or creates a new component/page. Skip for bugfix/refactor without visual changes.

   | Situation | Action |
   |---|---|
   | Project has `DESIGN.md` | Read it. It fixes the project's design direction — follow it, do not re-derive. No skill invocation. |
   | New UI file, no `DESIGN.md` yet | `Skill(design-ultimate)` — it is the single entry point for design and orchestrates its own dependencies. |
   | Edit to an existing UI file | Follow the surrounding code and `DESIGN.md`. No skill invocation. |

   Do not invoke `impeccable`, `design-motion-principles` or the taste overlays directly — they are muted on purpose and reachable only through `design-ultimate`.

4. **Analyze & Review Approach**
   - Grep usages of code to modify, read files that will change
   - Verify solution follows project patterns, identify reusable code
   - If modifying existing code, run existing tests for baseline
   - If concerns → discuss with user before proceeding

## Phase 2: Implementation (TDD)

1. **Write Tests First**

   Read [testing-guide.md](references/testing-guide.md) before writing tests.
   Write tests for business logic, validations, transforms, error handling. Skip trivial code.
   Tests should fail initially. One test = one scenario. Mocking >3 deps → use integration test.

2. **Write Code**
   - Implement to pass tests, follow project patterns or [universal-patterns.md](references/universal-patterns.md)
   - Use env vars for secrets, validate inputs at boundaries, comment WHY not WHAT
   - **Design tokens in UI code.** If tokens.json was loaded, use CSS custom properties instead of hardcoded values. Mapping rule: `--{category}-{remaining-path}` with hyphens.

     | JSON path prefix | CSS variable prefix | Example |
     |---|---|---|
     | `colors` | `--color` | `colors.primary.500` → `--color-primary-500` |
     | `typography.families` | `--font` | `.families.heading` → `--font-heading` |
     | `typography.sizes` / `.weights` / `.lineHeights` | `--font-size` / `--font-weight` / `--line-height` | `.sizes.base` → `--font-size-base` |
     | `spacing` / `radii` / `shadows` / `breakpoints` | `--space` / `--radius` / `--shadow` / `--breakpoint` | `spacing.4` → `--space-4` |

3. **Run Tests** — all new tests pass, fix any failures

## Phase 3: Post-work

1. **Run Lint/Format** — run project's linter and formatter before reviews

2. **Run Relevant Tests** — tests for changed files + task-specified tests. Save full suite for end of feature.

3. **Smoke Verification** (if task has Verification Steps → Smoke or User)
   Execute each Smoke command, record results in decisions.md. Fail → fix before reviews.
   User checks → ask user to verify, wait for confirmation.

4. **Post-Generation Guard**

   Load [quick-ref-code-writing.md](../quick-learning/references/quick-ref-code-writing.md) as reminders (if exists). Scan all generated/modified code for:

   - **Secrets in logs:** grep for `.env`, `password`, `secret`, `token`, `api_key` inside logging calls → remove immediately
   - **Missing timeout in HTTP calls:** all `fetch()`/`axios.*()`/`requests.*()` must have timeout → add 30s default
   - **Missing cache/dedup on rate-limited API calls:** repeated calls without caching → add cache/dedup. Paid APIs with quota → cache processed records in DB with skip-known logic across runs

   If violation found → fix, check if it matches a trigger in [triad-index.md](../quick-learning/references/triad-index.md), increment Seen counter.

5. **Select and run reviewers**

   **Working as part of a team?** Follow team protocol from team lead instead of steps below.

   A reviewer is a second pair of eyes with its own context, reading the committed diff — not a re-check of reasoning you already did. Pick reviewers by what the diff actually contains, not by which skill produced it. A task file's `reviewers:` field, when present, wins over this table.

   | Diff contains | Reviewer | Effort |
   |---|---|---|
   | Anything beyond a trivial edit | `code-reviewer` | medium |
   | auth, sessions, tokens, passwords, crypto, user input, SQL, file paths from external data, calls to external APIs | + `security-auditor` | medium |
   | new or modified test files, or the task carried a TDD Anchor | + `test-reviewer` | low |
   | CI/CD config, deploy scripts, secrets management | + `deploy-reviewer` | low |
   | Dockerfile, pre-commit hooks, project scaffolding | + `infrastructure-reviewer` | low |
   | LLM prompts | + `prompt-reviewer` | low |

   **Trivial edit — no reviewer at all:** a typo, a renamed local variable, a copy string, a version bump. Spawning three agents to look at a one-line change costs more than it can find.

   For each selected reviewer: spawn subagent (subagent_type = reviewer name), pass git diff + paths to task/tech-spec/user-spec. Reports go to `logs/working/task-{N}/{reviewer-name}-{round}.json`. Re-review → incremented round number.

6. **Process Findings**

   Evaluate each finding on merit — severity is metadata, not a filter. For each:
   - **Valid** → apply (any severity) | **Disagree** → discuss with user | **Out of scope** → skip, note in log

   Produce findings log: `| # | Source | Severity | Finding | Action | Reason |`

   After fixes → re-run tests → re-run the reviewer(s) that raised findings.

   **Stop condition is progress, not a round counter.** Continue while each round leaves strictly fewer open findings than the one before. The moment a round ends with the same or more open findings than the previous round, stop and escalate to the user with: what remains open, what was tried, why the last round did not move it. A loop that stopped converging will not converge on the next pass either.

## Проверки фактом

These are not a review of your own reasoning — they read state off disk. Run them, read the output, act on what it says. Skip a line only when its precondition does not apply.

```bash
# 1. decisions.md entry for this task exists
rg -n "Task {N}" work/{feature}/decisions.md

# 2. reviewer reports were actually written (skip if no reviewer was selected)
rg -l . work/{feature}/logs/working/task-{N}/

# 3. smoke results recorded (skip if the task had no Smoke/User steps)
rg -n -A3 "Verification" work/{feature}/decisions.md

# 4. no hardcoded colours left in changed UI files (skip unless tokens.json was loaded)
rg -n "#[0-9a-fA-F]{3,8}" <changed .css/.scss/.tsx files>
```

**Visual/Layout QA (UI only).** Confirm by measuring the render, never by eye: equal heights and widths across a row, alignment within a row, no seams at section borders, a companion font covering Cyrillic, digits not left in a display font that lacks their glyphs. See «Visual/Layout QA» in quick-ref-code-writing.md.

## Promoted Patterns

- **Маскируй секреты ДО выполнения команды** (Seen: 2): при любом чтении конфигов удалённой машины — встраивать маскировку в команду (`sed 's/:[^@]*@/:***@/'`) или проверять наличие переменной через `grep -c`. Никогда не выводить `.env` целиком.
- **Assertions на output-формат, не на input-атрибуты** (Seen: 2): перед написанием assertions прочитать реальный пример вывода функции. Для format-conversion функций (JSON→MD, dict→текст) assertions должны соответствовать output-формату — иначе тест проверяет input surface и не ловит баги конвертации.
- **Path traversal из любых внешних данных — allowlist** (Seen: 2): Перед построением файлового пути из любого внешнего значения (данные с диска, user input, API-параметры) — валидировать каждое значение против allowlist. Даже значения, записанные самим приложением, могут быть изменены между записью и чтением.

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during code writing.
