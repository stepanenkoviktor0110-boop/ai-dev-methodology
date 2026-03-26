# Reasoning Patterns

Accumulated insights about decision-making logic across projects.
Single transit buffer for ALL methodology knowledge — both reasoning patterns and operational lessons.

**This is a transit buffer.** Patterns that reach `Seen: 3` get promoted into skill SKILL.md files and removed from here. Stale entries (Seen: 1, older than 30 days) get pruned.

---

## Universal

Patterns that apply to any project, any stack, any domain.

<!-- Append universal patterns below -->

### 2026-03-26 quick-learning / meta: Верифицируй доставку, а не только создание

**Seen:** 1
**Triad:** создание нового артефакта → проверить доступность в runtime среде → не объявлять "готово" пока не виден потребителю
**Context:** Скилл quick-learning был создан в репо и закоммичен, но не попал в ~/.claude/skills/ — Claude Code его не видел, /quick-learning не работал.
**Pattern:** После создания любого артефакта (скилл, конфиг, шаблон) — проверь что он доступен в той среде, где будет использоваться. Создать в репо ≠ доставить потребителю.
**Scope:** universal
**Category:** sequencing

### 2026-03-26 shift-confirmation / session 2: Build-before-commit при изменении сигнатур

**Seen:** 2
**Triad:** изменение сигнатуры функции-callback → запустить build до коммита → не ломать deploy из-за type error
**Context:** Добавил optional параметр в `applyFilters()`, которая использовалась как `onClick` handler. TypeScript локально не ругался (vitest не проверяет JSX), но production build упал — `MouseEvent` не совместим с `"list" | "grid"`. Deploy failed, потерял ~3 мин на fix + redeploy. Паттерн подтверждён дважды (quick-learning + retrospective).
**Pattern:** При изменении сигнатуры функции, которая используется как event handler или callback — запускай `npm run build` до коммита. Vitest не проверяет JSX-совместимость типов, только build ловит эти ошибки.
**Scope:** universal
**Category:** sequencing

### 2026-03-26 mvp-parser / session 1: Retry-декоратор должен знать, что НЕ ретраить

**Seen:** 1
**Triad:** generic retry decorator оборачивает API-вызов → явно исключить non-retryable exceptions → не ретраить ошибки, которые повторятся всегда
**Context:** `retry_with_backoff` ловил все Exception, включая HTTP 429 (quota exceeded). Ревьюер поймал: quota не восстановится через 30 секунд, retry бессмыслен и тратит время. Пришлось менять архитектуру: _request возвращает Response без raise, caller проверяет status code.
**Pattern:** При проектировании retry-обёртки сразу определи список non-retryable исключений. Если декоратор generic (ловит Exception) — добавь параметр `exclude` или проверяй тип перед retry. Retryable = транспортные ошибки + 5xx. Non-retryable = 4xx (quota, auth, not found).
**Scope:** universal
**Category:** tool-selection

### 2026-03-26 tech-spec / meta: Верифицируй библиотечные методы из code-research

**Seen:** 1
**Triad:** tech-spec использует библиотечные методы из code-research → проверить методы по реальной документации до включения в спек → предотвратить propagation миражей code-research → tech-spec → implementation
**Context:** Code-research может содержать неточные или устаревшие описания API — если tech-spec копирует их без проверки, мираж распространяется до реализации.
**Pattern:** Перед включением конкретных методов/функций из code-research в tech-spec — проверь их существование и сигнатуры по официальной документации или исходникам библиотеки.
**Scope:** universal
**Category:** information-gathering

### 2026-03-26 tech-spec / meta: Error state machine для внешних API

**Seen:** 1
**Triad:** tech-spec для проекта с внешними API → задокументировать error state machine (HTTP код → состояние приложения) в Decisions → предотвратить неоднозначную реализацию error handling разными исполнителями
**Context:** Без явной error state machine каждый исполнитель реализует error handling по-своему — результат непредсказуем.
**Pattern:** При написании tech-spec для фичи с внешними API — добавь в Decisions таблицу: HTTP status → app state → user message → retry policy. Это устраняет неоднозначность реализации.
**Scope:** universal
**Category:** information-gathering

### 2026-03-24 payroll-full-calc: Post-deploy UX-правки — это норма

**Seen:** 1
**Triad:** post-deploy verification с пользователем → планировать 2-4 итерации UX-правок как норму → не считать UX-корректировки проблемой процесса
**Context:** 6 post-deploy коммитов с UX-правками (скрыть штрафы, показать обе ставки, авто-перезагрузка, выравнивание, добавить роль ADMIN). Все обнаружены только при live-верификации — user-spec не покрывал UI-детали.
**Pattern:** При post-deploy verification — планировать 2-4 итерации UX-правок. Пользователь видит реальный UI впервые и уточняет требования. Коммитить каждый фикс отдельно для чистой истории.
**Scope:** universal
**Category:** scope-management

### 2026-03-25 design-pipeline: Проверяй пути в сгенерированных задачах

**Seen:** 1
**Triad:** генерация задач из tech-spec → проверять каждый путь через test -e, валидировать depends_on → предотвратить задачи с несуществующими файлами
**Context:** Первый раунд валидации нашёл несуществующие пути к файлам и неверные depends_on ссылки в 12 задачах. Task creator генерировал пути по предположению из tech-spec.
**Pattern:** После генерации задач проверяй каждый путь к файлу через `test -e`. Валидируй depends_on: зависимость должна создавать артефакт, который зависимая задача читает.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-26 design-pipeline-v1: AC через артефакты, не через поведение

**Seen:** 1
**Triad:** AC для markdown-only фич → формулировать через наличие конкретных артефактов → сделать AC автоматически проверяемыми
**Context:** User-spec прошёл 2 раунда валидации — AC описывались на уровне поведения агента ("агент предлагает"), а не верифицируемых артефактов. Переписаны в формат "файл X содержит Y".
**Pattern:** При написании AC для markdown-only фич (скиллы, reference-файлы) формулировать критерии через наличие конкретных артефактов: "файл X содержит Y", "SKILL.md содержит шаг Z в Phase N".
**Scope:** universal
**Category:** scope-management

## Situational

Patterns that apply only in specific contexts. Each has a `Situation` field describing when it's relevant.

<!-- Append situational patterns below -->

### 2026-03-24 payroll-full-calc: Audit agents — lead записывает за них

**Seen:** 1
**Triad:** audit-агенты сообщают о невозможности записи → lead сразу записывает результаты сам → не терять время на повторные попытки агента
**Context:** Все 3 audit-агента (code, security, test) завершили аудит, но не смогли записать JSON-отчёты из-за ограничений прав. Team lead вручную записывал результаты.
**Pattern:** После spawn audit-агентов, если агент сообщает о невозможности записать файлы — lead сразу записывает результаты сам, не ожидая повторных попыток от агента.
**Scope:** situational
**Situation:** multi-agent workflow с audit-субагентами
**Category:** communication

### 2026-03-26 shift-confirmation: Ошибки повторяются между волнами

**Seen:** 1
**Triad:** ревью нашло паттерн ошибки (не разовый баг) → добавить предупреждение в промт следующего teammate → предотвратить повторение ошибки в следующих задачах
**Context:** В Task 1 ревьюер нашёл `confirmationStatus: string` вместо enum. Исправили. В Task 4 — ровно та же ошибка. Агент Task 4 не знал о находке Task 1, т.к. каждый teammate с чистым контекстом.
**Pattern:** Когда ревью находит паттерн ошибки (не разовый баг), lead добавляет предупреждение в промт следующего teammate: "В предыдущих задачах ревьюеры находили [X] — убедись, что новый код не повторяет эту ошибку."
**Scope:** situational
**Situation:** multi-agent feature execution с несколькими волнами
**Category:** communication

### 2026-03-26 shift-confirmation: Behavioral тесты вместо implementation

**Seen:** 1
**Triad:** написание тестов в multi-agent workflow → требовать assertion на результат функции, не только на mock → тесты ловят баги, а не проверяют форму вызова
**Context:** В каждой задаче (1, 2, 4) test-reviewer находил тесты с `toHaveBeenCalledWith` как единственной проверкой. Агенты оптимизируют на "тест проходит", не на "тест ловит баг".
**Pattern:** В промт teammate добавить: "Каждый тест ОБЯЗАН иметь assertion на результат функции (return value / output shape), а не только на аргументы вызова mock."
**Scope:** situational
**Situation:** multi-agent workflow, генерация тестов агентами
**Category:** tool-selection

### 2026-03-26 shift-confirmation: Known-issues реестр для аудитов

**Seen:** 1
**Triad:** security/code audit в multi-task feature → вести known-issues.md, аудитор читает перед ревью → не тратить время на повторный репорт известных проблем
**Context:** Security auditor нашёл IDOR в `markEvent()` при ревью Task 2. Та же находка повторилась в audit wave. Нет реестра известных проблем — тратит время на уже известное.
**Pattern:** Завести `known-issues.md` на уровне проекта. Перед ревью агент читает его и пропускает задокументированные проблемы.
**Scope:** situational
**Situation:** multi-task features с security/code audit
**Category:** information-gathering
