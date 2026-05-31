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

## ⛔ Karpathy Rules — override all defaults below

**1. Think Before Coding**
Before writing a single line: list every assumption you are making. If uncertain → ask, don't guess. If multiple interpretations exist → present them, don't pick silently. If something is unclear → stop and name it.

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

   Apply IF task touches UI: создаёт/правит `.css`/`.scss`/`.tsx`/`.jsx`/`.vue`/`.svelte`/`.html`, или собирает новый компонент/страницу. Skip для bugfix/refactor без визуальных изменений.

   a. **CIP brief (always for UI).** Запустить CLI из `CLAUDE.md → CIP / UI Design CLI` с query=индустрия/контекст, brand=имя проекта. Output (palette/typography/style/anti-patterns) держать в рабочем контексте — план и верстка должны на него опираться.

   b. **Deep reasoning (conditional).** Если задача = новый продукт / нестандартный домен / multi-stack И CIP-данных недостаточно → `Skill(ui-ux-pro-max:ui-ux-pro-max)` для 161 industry-правил и stack-specific guidelines.

   c. **Execution principles (new-from-scratch only).** Если задача = «build new UI component/page» (не правка) → `Skill(frontend-design:frontend-design)` перед версткой — для bold aesthetic и защиты от generic-AI-эстетики.

4. **Analyze & Review Approach**
   - Grep usages of code to modify, read files that will change
   - Verify solution follows project patterns, identify reusable code
   - If modifying existing code, run existing tests for baseline
   - If concerns → discuss with user before proceeding

**Checkpoint:** List completed preparation steps before moving to implementation.

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

**Checkpoint:** List implemented functionality and test results.

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

5. **Run Reviews** (launch in parallel)

   **Working as part of a team?** Follow team protocol from team lead instead of steps below.

   **Reviewer selection:** task file → reviewers from task's "Reviewers" section; standalone → code-reviewer, security-auditor, test-reviewer.

   For each reviewer: spawn subagent (subagent_type = reviewer name), pass git diff + paths to task/tech-spec/user-spec. Reports go to `logs/working/task-{N}/{reviewer-name}-{round}.json`. Re-review → incremented round number.

6. **Process Findings**

   Evaluate each finding on merit — severity is metadata, not a filter. For each:
   - **Valid** → apply (any severity) | **Disagree** → discuss with user | **Out of scope** → skip, note in log

   Produce findings log: `| # | Source | Severity | Finding | Action | Reason |`
   After fixes → re-run tests → re-run reviewer(s). Limit: 3 iterations, then ask user.

**Checkpoint:** List post-work steps completed.

## Self-Verification

- [ ] All phases completed; tests pass
- [ ] Smoke verification executed (if task had Smoke/User checks)
- [ ] Each reviewer finding evaluated; findings log table produced; reports saved
- [ ] Design tokens used via CSS custom properties for UI files (if tokens.json was loaded)


## Promoted Patterns

- **Маскируй секреты ДО выполнения команды** (Seen: 2): при любом чтении конфигов удалённой машины — встраивать маскировку в команду (`sed 's/:[^@]*@/:***@/'`) или проверять наличие переменной через `grep -c`. Никогда не выводить `.env` целиком.
- **Assertions на output-формат, не на input-атрибуты** (Seen: 2): перед написанием assertions прочитать реальный пример вывода функции. Для format-conversion функций (JSON→MD, dict→текст) assertions должны соответствовать output-формату — иначе тест проверяет input surface и не ловит баги конвертации.
- **Path traversal из любых внешних данных — allowlist** (Seen: 2): Перед построением файлового пути из любого внешнего значения (данные с диска, user input, API-параметры) — валидировать каждое значение против allowlist. Даже значения, записанные самим приложением, могут быть изменены между записью и чтением.

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during code writing.

- When зависимость мемоизированного вычисления ссылается на промежуточное значение созданное в render → вынести нормализацию внутрь вычисляющей функции, зависимость — исходный prop/state, to гарантировать стабильность референса и реальную работу мемоизации
- When проект с модульной системой ESM, нужен legacy-совместимый скрипт с CommonJS-зависимостями → выделить скрипт в отдельный файл с явным расширением для legacy-модулей, использовать DI для тестируемых зависимостей, to избежать runtime ошибки несовместимости модулей и хаков при тестировании
- When написание теста для finally-блока с except Exception → использовать BaseException (например KeyboardInterrupt) как trigger, to гарантировать что finally реально выполняется при любом исходе
- When скрипт с дорогостоящей инициализацией (auth flow, DB connection) создаёт объект внутри цикла → вынести init за цикл и указать явно в spec, to предотвратить дублирование auth flow и N лишних round-trips
- When кнопка делает async-запрос (destructive action или оптимистичный UI) → добавить disabled+loading state на время запроса AND .catch() восстанавливающий state при ошибке — до первого review, to предотвратить fix-раунд на предсказуемый UX concurrency guard
- When расширение API-ответа новым полем → grep тесты на exact-equality assertions для этого endpoint, to не допустить отложенного тест-фейла в следующей сессии
- When файл не менялся с момента первого чтения → не читать повторно, to экономить токены
- When несколько git репо в одной bash сессии → всегда указывать `git -C /path/repo` вместо надежды на рабочую директорию, to избежать silent failures от команд из неправильного репо
- When нужно изучить внешнее репо (GitHub) или прочитать >5 файлов подряд в главной сессии → делегировать сканирование Explore subagent'у одним вызовом, to не исчерпать контекст главной сессии
- When компонент хранит типизированные async данные, UI переключает режим/таб → сбрасывать данные в начале каждого async-запроса и проверять тип перед обращением к типо-специфичным полям, to предотвратить runtime ошибку из промежуточного рендера со stale типизированными данными
- When скрипт использует Unix-пути (/tmp, /dev/null) в кросс-платформенном окружении → проверить целевую ОС и использовать платформо-специфичный эквивалент пути, to не получать FileNotFoundError из-за несовместимого системного пути
- When экспорт данных с числовыми или непредсказуемыми ключами в табличный формат → передавать явный массив заголовков вместо порядка ключей объекта, to гарантировать правильный порядок колонок в итоговом файле
- When SQL UPDATE обновляет подмножество полей таблицы с NOT NULL → использовать COALESCE($N, column_name) для полей не переданных в запросе, to предотвратить constraint violation при частичном обновлении.
- When выбор JS scroll/animation библиотеки для SSR-фреймворка → предпочесть CSS-native решение (sticky, scroll-snap) вместо JS-управляемого pin/scroll, to избежать конфликта JS-плагина с SSR layout-моделью и последующего рефакторинга
- When архитектурное решение изменилось в ходе реализации → обновить architecture.md/patterns.md немедленно, не в конце сессии, to не передать следующей сессии устаревшую документацию.
- When соседние секции имеют разный backgroundColor при общем overlay-фоне → сделать все секции transparent, базовый цвет — только на wrapper/overlay, to убрать жёсткий шов на границе секций.
- When добавление prop к JSX через Edit → прочитать весь элемент и проверить существующие props, to не создавать дубликаты.
- When сервис отвечает мгновенно локально, но медленно снаружи → проверить все вызовы на уровне module import — сетевые, I/O, внешние API; вынести в background thread, to убрать блокировку worker startup.
- When серверный код должен инициировать auth flow (reset password, verify email) → вызвать серверный API auth-библиотеки, не писать токен в БД вручную, to обеспечить совпадение токенов с форматом который валидирует клиентская часть.
- When таблица с overflow-x-auto + sticky колонкой → не ставить промежуточный div между scroll-контейнером и table — sticky ломается в Safari, to корректное sticky-поведение колонки во всех браузерах.
- When делегирование кодогенерации внешнему AI-агенту на много файлов → инструктировать "пиши файлы по одному, не все разом", to предотвратить зависание агента на генерации гигантского патча.
- When d3 `.each()` на SVG элементах отрисованных React → lookup по data-* атрибутам вместо bound data, to предотвратить crash от undefined datum.
- When делегирование write-задачи sandboxed-инструменту → проверить write permissions тестовой операцией до полного промта, to не терять время на failed delegation + ручную реализацию.
- When VPS нужен публичный URL → перед выбором tunnel-сервиса проверить outbound connectivity VPS (HTTPS? SSH?), to не тратить попытки на несовместимые решения.
- When JS frontend хранит список в in-memory state → POST мутирует один элемент → после успешного POST обновить запись в state синхронно (state[key] = newValue), to не допустить stale display при последующем re-render.
- When batch endpoint валидирует каждый элемент и возвращает 400 если хоть один неизвестен → изменить на "skip unknowns, return known" (partial success), to не ломать весь batch из-за одного невалидного элемента.
- When same parameter/field name used across any boundary (SQL JOIN, API, function call) → verify both sides agree on the identifier's semantic domain, to avoid name-match semantics-mismatch where identical names mask different meanings.
- When стилевой модуль импортирует файл содержащий глобальные селекторы через @use → выносить переменные в отдельный partial без глобальных правил, модули @use только partial, to предотвратить purity error сборщика из-за non-local селекторов в модуле
- When jsdom integration-тест использует history.replaceState с абсолютным URL → использовать window.location.hash или относительный путь вместо абсолютного URL, to избежать SecurityError в jsdom test environment
- When визуальный баг в SVG/Canvas layout → вывести координаты нод через unit-тест до фикса, to не итерировать вслепую
- When нужна визуальная проверка из CLI → Playwright скриншот dev server + Read tool, to не деплоить ради проверки глазами
- When баг в визуальном поведении, код кажется "неправильным" → сначала читать project-knowledge (domain glossary, patterns), потом код, to не делать ложных выводов из реализации, противоречащих спеке
- When промт для внешнего AI-агента содержит API-сигнатуры → верифицировать каждую через inspect.signature() или docs до отправки, to не вызвать fix round из-за неверных фактов
- When настройка bind-адреса процесса внутри контейнера для ограничения внешнего доступа → применять сетевое ограничение на уровне port mapping хоста, внутри контейнера слушать на 0.0.0.0, to не сделать сервис недостижимым из-за применения ограничения на неверном уровне абстракции
