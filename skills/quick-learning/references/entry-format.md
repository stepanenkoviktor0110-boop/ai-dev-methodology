# Entry Format & Rules

## Entry format

Append to `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`:

```markdown
### {YYYY-MM-DD} {feature-name} / session {N}: {pattern title}

**Seen:** 1
**Adapted:** —
**Cognitive Error:** {3-5 word name, e.g. "partial mutation bias"}
**Triad:** {situation type} → {corrective thinking rule} → {cognitive trap to avoid}
**Context:** {what thinking mistake was made — 1 sentence, domain-free}
**Pattern:** {corrective rule — 1-2 sentences, imperative, domain-free}
**Scope:** {universal | situational}
**Situation:** {only for situational}
**Category:** {sequencing | information-gathering | problem-decomposition | scope-management | recovery | communication | tool-selection | design-taste | design-process | design-iteration}
```

## Rules

- Must name a **cognitive error** — can't name in 3-5 words → describing an event.
- Must be **domain-free** — no file/tool/framework/role names. Pure thinking logic.
- Must be **non-obvious** — "write tests" is obvious. "Existence ≠ active participation" is not.
- Max 2 entries per session. Every entry must have Cognitive Error, Triad, Adapted.
- **Scope:** universal = any project/stack/domain → `## Universal`. Situational = specific context → `## Situational` + `Situation` field.
- **Backward compat:** old entries without Cognitive Error remain valid. New entries MUST include it.

## Three-Tier Knowledge System

| Tier | File | Purpose | Writers | Readers |
|------|------|---------|---------|---------|
| 0 | `triad-index.md` | 1-line dedup index + Adapted col | ql | ql (always), skill-trainer |
| 1 | `reasoning-patterns.md` | Full entries + context | ql | ql (on merge only) |
| 2 | `{skill}/SKILL.md` | Embedded instructions | skill-trainer | skill itself |
| 3 | `quick-ref-{skill}.md` | Top-10 reminders | skill-trainer | skill at start |

Quick-ref files: `$AGENTS_HOME/skills/quick-learning/references/quick-ref-{skill-name}.md`.

## Triad Index format

File: `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`

```markdown
| # | Trigger | Action | Goal | Scope | Seen | Section | Adapted |
|---|---------|--------|------|-------|------|---------|---------|
| 1 | before review | run smoke test | avoid wasted review rounds | universal | 2 | Universal | feature-execution |
```

- Updated on every write/merge/Seen increment. Never removed.
- `Adapted: —` = unprocessed. `{skill}` = embedded. `n/a` = no matching skill.

## Guard-triggered Seen increment

When a guard catches an error matching an existing pattern's trigger — increment Seen in triad-index.md, even outside quick-learning flow.
