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

## Situational

Patterns that apply only in specific contexts. Each has a `Situation` field describing when it's relevant.

<!-- Append situational patterns below -->
