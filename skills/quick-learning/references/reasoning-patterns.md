# Reasoning Patterns

Accumulated meta-level insights about decision-making logic across projects.
These patterns are NOT about specific technical choices — they're about HOW to approach problems.

**This is a transit buffer.** Patterns that reach `Seen: 3` get promoted into skill SKILL.md files and removed from here. Stale entries (Seen: 1, older than 30 days) get pruned.

---

## Universal

Patterns that apply to any project, any stack, any domain.

<!-- Append universal patterns below -->

### 2026-03-26 quick-learning / meta: Верифицируй доставку, а не только создание

**Seen:** 1 (quick-learning/meta)
**Triad:** создание нового артефакта → проверить доступность в runtime среде → не объявлять "готово" пока не виден потребителю
**Context:** Скилл quick-learning был создан в репо и закоммичен, но не попал в ~/.claude/skills/ — Claude Code его не видел, /quick-learning не работал.
**Pattern:** После создания любого артефакта (скилл, конфиг, шаблон) — проверь что он доступен в той среде, где будет использоваться. Создать в репо ≠ доставить потребителю.
**Scope:** universal
**Category:** sequencing

### 2026-03-26 shift-confirmation / session 2: Build-before-commit при изменении сигнатур

**Seen:** 1
**Triad:** изменение сигнатуры функции-callback → запустить build до коммита → не ломать deploy из-за type error
**Context:** Добавил optional параметр в `applyFilters()`, которая использовалась как `onClick` handler. TypeScript локально не ругался (vitest не проверяет JSX), но production build упал — `MouseEvent` не совместим с `"list" | "grid"`. Deploy failed, потерял ~3 мин на fix + redeploy.
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

## Situational

Patterns that apply only in specific contexts. Each has a `Situation` field describing when it's relevant.

<!-- Append situational patterns below -->
