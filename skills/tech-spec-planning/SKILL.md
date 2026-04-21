---
name: tech-spec-planning
description: |
  Creates tech-spec.md with architecture, decisions, testing strategy, and implementation plan.

  Use when: "сделай техспек", "составь техспек", "техническая спецификация",
  "tech spec", "создай тз", "составь тз", "new-tech-spec", "/new-tech-spec"

  Requires existing user-spec.md as input (create with user-spec-planning skill first if missing).
---

# Tech Spec Planning

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Create technical specification through code research, adaptive clarification, and multi-validator review.

**Input:** `work/{feature}/user-spec.md` + Project Knowledge
**Output:** `work/{feature}/tech-spec.md` (approved)
**Language:** Technical documentation in English, communication in Russian

Before starting, read [quick-ref-tech-spec-planning.md](../quick-learning/references/quick-ref-tech-spec-planning.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Load Context

1. Ask user for feature name if not provided. Check `work/{feature}/` exists, create if needed.
2. Read `work/{feature}/user-spec.md`. Missing → ask user to describe task or create user-spec first. Extract `size: S|M|L` from frontmatter.
3. Read all files in `.claude/skills/project-knowledge/references/` (missing files are fine).
4. user-spec.md is the single input source — interview.yml and code research are already consolidated there.

## Phase 2: Code Research

Launch `code-researcher` subagent (opus) with feature path and user-spec path. It reads existing `code-research.md` (from user-spec phase) and deepens for implementation.

After completion — read `{feature_path}/code-research.md`. If gap discovered later — re-launch with specific question.

## Phase 3: Clarification (Adaptive)

**⛔ Think Before Coding (Karpathy — overrides default behavior):**
Before writing any architecture: list every assumption you are making about the system — explicitly, as a numbered list. For each assumption that isn't confirmed in user-spec or code research → ask the user. If multiple architectural interpretations exist → present them, don't pick silently. If something is unclear → stop and name it before proceeding.

Analyze if additional information is needed based on user-spec and code research.
- Ask technical questions if gaps exist (no limit on count). Focus: constraints, integration points, data sources, external deps.
- Gaps in user-spec requirements → discuss with user and update user-spec too.
- Fundamentally unclear → suggest creating user-spec first.

## Phase 3.5: Stack Research Gate (deep)

Before writing Architecture / Decisions / Shared Resources in Phase 4, collect every stack element that will be used or touched: external APIs, third-party services, new libraries not already covered in the existing `stack-research.md` registry, and libraries whose usage pattern differs from what's documented there.

Classify each candidate:

**Critical** (BLOCK — must be researched at `depth=deep`):
- External APIs (AI, payments, messaging, data providers)
- External services (deploy platforms, auth providers, queues)
- Libraries NOT in the whitelist (`~/.claude/skills/stack-research/references/stable-libraries-whitelist.md`)
- Library with major version < 1.0
- Niche tools (Paged.js, remark/rehype plugins, MCP servers, etc.)
- Any element where the tech-spec will rely on specific endpoints, rate limits, auth flow, or edge-case behavior

**Familiar** (PROMPT — may skip):
- Whitelisted libraries used in a standard way

**Action by class:**

- **Critical candidates present** → STOP. Output:
  > "Перед формулировкой архитектуры и решений требуется deep-ресёрч критичных элементов: [candidate list]. Вызови `/stack-research` с параметрами:
  > - decision_context: {one-sentence, what this tech-spec uses the element for}
  > - candidates: [list with type]
  > - depth: deep
  > - project_context: {2-3 sentences including user-spec constraints}
  > - feature_path: {work/{feature}}
  >
  > Скажи 'продолжаем' после завершения — прочитаю отчёты и продолжу."
  >
  > Do not write Architecture / Decisions / Shared Resources sections for critical candidates without a fresh deep entry in `stack-research.md` or a report under `{feature_path}/logs/stack-research/`.

- **Only familiar candidates** → Output:
  > "Новые/изменённые элементы стека — только из whitelist: [list]. Deep-ресёрч опционален: `/stack-research`. Вызывать? (да / пропускаем)"
  >
  > Wait for answer. Proceed either way.

After the gate passes, read the fresh report(s) and the registry. In Phase 4, when writing Decisions, cite report paths as the source of non-trivial technical claims. Do NOT mix memory-based claims with researched facts.

## Phase 4: Create tech-spec

**⛔ Simplicity First (Karpathy — overrides default behavior):**
Design the minimum architecture that solves today's problem. No components added "for future flexibility". No abstractions until needed by at least 2 concrete use cases in this spec. Before adding any architectural element ask: "Is this required by user-spec, or am I speculating?" If speculating → don't add it. If the spec grows beyond 15 tasks → treat it as a signal of overengineering, not scope, and propose MVP split before continuing.

1. Copy template and edit sections one by one:
   ```bash
   cp ~/.claude/shared/work-templates/tech-spec.md.template work/{feature}/tech-spec.md
   ```

2. Fill frontmatter: `created` (today), `status: draft`, `size` (from user-spec), `branch`: `dev` (simple) or `feature/{name}` (multi-component).

3. Fill all template sections. Architecture → Shared Resources: list heavy resources (ML models, DB pools, API clients) with owner, consumers, instance count.

4. Fill Implementation Tasks by waves. For each task: Description (2-3 sentences, WHAT+WHY not HOW), Skill, Reviewers, Verify-smoke (optional), Verify-user (optional), Files to modify, Files to read. Select skill and reviewers from [skills-and-reviewers.md](references/skills-and-reviewers.md).

   `Verify-smoke:` — when task involves external API, library init, Docker/infra, LLM/prompt, MCP-verifiable UI. Write concrete command + expected response.
   `Verify-user:` — when user should check UI/behavior on localhost.
   Omit both if purely internal logic covered by unit tests.

   **Task brevity:** tasks are brief scope descriptions. Detailed steps, AC, TDD anchors, `estimated_loc` come from task-decomposition phase. All technical decisions belong in Decisions section, not tasks.

5. Last two waves always **Audit Wave** + **Final Wave**:

   **Audit Wave** — 3 parallel tasks, `reviewers: none`:
   - Code Audit (`code-reviewing`), Security Audit (`security-auditor`), Test Audit (`test-master`)
   Auditors read all feature files, write reports. Issues found → feature-execution spawns fixer.

   **Final Wave:**
   - QA (`pre-deploy-qa`) — mandatory. Acceptance testing against user-spec + tech-spec.
   - Deploy (`deploy-pipeline`) — if needed.
   - Post-deploy verification (`post-deploy-qa`) — if live-environment checks needed.

6. >15 tasks → propose splitting into MVP + Extension. Wait for user decision.

7. Git commit: `draft(techspec): create tech-spec for {feature}`

## Phase 5: Validation

### Run 5 validators in parallel

Each writes JSON report to `logs/techspec/{name}-review.json`:

| Validator | Agent | Checks |
|-----------|-------|--------|
| Mirage detector | `skeptic` | Non-existent files, APIs, functions, dependencies |
| Completeness | `completeness-validator` | Traceability, scope creep, over/underengineering |
| Security | `security-auditor` | OWASP, input validation, auth, sensitive data |
| Testing strategy | `test-reviewer` | Test plan adequacy for size S/M/L |
| Template + waves | `tech-spec-validator` | Sections, frontmatter, skills/reviewers, wave conflicts |

Pass to each: `work/{feature}/tech-spec.md` + `work/{feature}/user-spec.md`.

### Process findings

Read all 5 reports. Fix if valid, reject with reasoning if disagree, discuss with user if controversial.

After fixes → commit `chore(techspec): validation round {N} — {summary}` → re-run validators. Max 3 iterations, then escalate to user.

## Phase 6: User Approval

1. Show tech-spec.md + validation summary (iterations, issues resolved).
2. Wait for explicit approval. Comments → fix, re-validate, show again.
3. Set `status: approved`, commit `chore(techspec): approve tech-spec for {feature}`.
4. Suggest `/decompose-tech-spec` as next step.

## Promoted Patterns

- **Верифицируй целевые файлы перед описанием операции (Seen: 2):** Когда spec описывает трансформацию "удалить X из N файлов" или "заменить Y" — grep по каждому файлу перед тем как зафиксировать тип операции. Файл без X требует add, не replace. Ошибка типа операции обнаруживается только при выполнении задачи.
- **Верифицируй API response shapes live-вызовом (Seen: 2):** При интеграции с внешним API — перенести в спек ВСЕ коды ответа, формат данных, edge cases. Перед включением response shapes из code-research — live API call для проверки. Один вызов дешевле propagation миража через pipeline.
- **Верифицируй файловые пути через ls/glob (Seen: 2):** Перед написанием путей в tech-spec — проверить через ls/glob, не из памяти или architecture docs. Docs описывают намерение, а не реальность. Перед записью "call sites функции X в файле Y" в Files to modify — grep по имени функции, подтвердить что вызовы реально существуют в указанном файле.

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during spec planning.

- When a proposal involves project-scope migration to reduce global overhead → first clarify whether the resource is universal or domain-specific, to avoid breaking universal-access requirements.
- When tech-spec contains a production default (run time, port, limit) → explicitly verify the value with the user during spec/task phase, to avoid late correction cascading across multiple files.
- When user requests «проверь соответствие первоисточнику» → fetch the source first, then apply corrections, to avoid inventing data.
- When spec contains explicit permission matrix for one destructive operation (delete) → verify ALL analogous destructive operations (deactivate, activate, reset, role change) against the same matrix, to find authorization gaps before implementation.
- When user-spec AVP contains URLs/endpoints written from memory → grep/verify each URL+method in the codebase before approving user-spec, to prevent URL mirage from propagating into tech-spec skeptic pass.
- When spec defines GET=admin+manager and PUT=manager-only on an endpoint where existing guard allows both roles → explicitly describe creation of a new guard for PUT in the task, to prevent auth gap discovered only at security audit.
- When запуск task-creator агентов → проверить runner (jest/vitest/pytest) и тест-директории, передать явно в каждый бриф, to предотвратить генерацию неработающих TDD Anchor путей.
- When написание depends_on для audit wave задач → перечислить ВСЕ задачи, создающие аудируемые файлы (не только последнюю волну), to гарантировать существование всех файлов к моменту аудита.
- When вопрос об инфраструктуре, деплое или production URL → читать decisions.md (changelog) ДО project-knowledge docs, to не дать ответ из устаревшего статичного снимка.
- When tech-spec Data Models содержит UPDATE SQL для существующей таблицы → reality-checker сверяет SQL против реального route.ts ища пропущенные существующие параметры, to предотвратить тихую потерю данных.
- When Wave 1 создаёт shared module с named exports, Wave 2 потребляет его → перечислить ВСЕ export-символы явно в брифе Wave 1 и передать точную строку импорта в каждый Wave 2 бриф, to предотвратить naming divergence.
- When планирование агрегации из log-таблицы по колонке добавленной ALTER TABLE → проверить заполненность исторических строк, не только наличие колонки, to не получить пустую агрегацию из "наполненной" таблицы.
- When бриф task-creator содержит compatibility constraint (ES5/legacy) + файл уже использует конкретный HTTP-паттерн → явно указать разрешённые API с примером строки из существующего кода, to предотвратить выбор устаревшего API вопреки code style.
- When трансформация структурированных данных (items, checklist, AC) в прозаический документ (spec, report, Solution) → перед написанием пройтись по каждому item источника, отметить что попал в целевой документ, to не потерять обсуждённые темы при смене формата представления.
- When tech-spec содержит публичный POST endpoint без авторизации → применить security checklist: CSRF/Origin, input sanitization (XSS+injection), IP extraction source, rate-limit, security headers, to не добавлять security decisions только после аудита.
- When test-reviewer возвращает fail в фазе tech-spec, ссылаясь на отсутствие тестов в файлах → признать false fail; указывать в промпте "проверь план, а не файлы", to не тратить раунд ревалидации на проблему формулировки промпта.
- When задача касается N≥3 незнакомых интерфейсов → верифицировать каждый интерфейс до генерации, to избежать O(N) фактических ошибок, каждая стоит review round.
- When планирование рефакторинга на основе файловой структуры или пользовательской диагностики → верифицировать через code research что каждый артефакт реально используется (рендерится, импортируется) до включения в scope, to не планировать работу над мёртвым кодом и не строить спек на ложных предпосылках.
- When формирование списка решений для обсуждения с пользователем (tech-spec) → фильтровать каждое решение: «изменится ли поведение продукта для пользователя?» — если нет, принять самостоятельно, to не тратить раунды коммуникации на чисто технические решения.
