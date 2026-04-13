---
name: quick-learning
disable-model-invocation: true
description: |
  Owner of the unified methodology knowledge system: format, triad structure,
  similarity check, Seen counters, and Adapted tracking.

  Signal-gated: skips clean sessions automatically (zero cost).

  Automatic trigger: called by feature-execution, do-task, and design-generate (context exhaustion).

  Use when: "quick learning", "быстрый анализ", "что улучшить в процессе",
  "извлеки паттерн", "запиши урок сессии", "analyze session patterns"
---

# Quick Learning

**Time budget:** Under 60 seconds. Not a full retrospective. Not a code review. Not responsible for embedding (that's `/skill-trainer`).
**Input:** `work/{feature}/decisions.md` + git log of current session
**Output:** entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`
**Language:** Entries in Russian, communication in Russian.

## Procedure

### Step 1: Signal Gate (5 sec)

Check 4 binary signals. If ALL zero — **skip** with "Clean session, no new patterns."

| Signal | How to check | Meaning |
|--------|-------------|---------|
| Fix rounds | `git log --oneline -20` — count `fix:` commits | Something went wrong and was corrected |
| Scope change | `decisions.md` — any deviation, changed approach | Plan didn't survive contact with reality |
| Recovery event | `git log` — rollbacks, retries, blocked→unblocked | Non-obvious recovery path found |
| Context waste | `decisions.md` — Concerns field, repeated reads of unchanged file | Inefficient tool use |

**Design sessions** (from design-generate) — additional signals: iteration rounds, taste correction, layout rework.

At least 1 signal → proceed. All zero → exit.

### Step 2: Analyze (15 sec)

> Scope change = *what* was done changed; context waste = *how* it was done was inefficient. Analyze independently.

For each signal:
1. **What thinking mistake was made?** Name the cognitive error in 3-5 words. Can't name it → it's an event, not a pattern. Skip.
2. **Was the first approach right?** What signal should have told us earlier?
3. **Cost of the detour?** (fix rounds, wasted reviews, rework)
4. **Transferable?** Would someone on a completely different project benefit from knowing this trap?

Skip if analysis produces only domain-specific events.

### Step 3: Write (20 sec)

Append to `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`.

#### Abstraction Gate (mandatory before writing)

The gate ensures entries capture **cognitive errors**, not events.

**Step A — Name the cognitive error** in 3-5 words. Examples:
- "partial mutation bias" (local change → assume global invariant holds)
- "existence ≠ active use", "scope anchoring", "authority by proximity", "silent dependency assumption"

Can't name it → skip.

**Step B — Domain-strip test.** Remove ALL domain nouns. Must remain a useful **thinking rule**.

| Level | Example | Verdict |
|-------|---------|---------|
| Bad | "после объединения задач пересчитать wave по depends_on" | Domain-specific → meaningless after strip |
| Medium | "после мутации графа перевалидировать топологический порядок" | Structural, but no cognitive error |
| Good | "изменил часть системы с инвариантом — не перепроверил, потому что остальное выглядело нетронутым. Ошибка: partial mutation bias" | Cognitive error, domain-free, transferable |

**Step C — Triad orientation.**
- Trigger = **situation type** (NOT event)
- Action = **corrective thinking rule**
- Goal = **cognitive trap name to avoid**

#### Similarity Check

Decompose into **trigger → action → goal** triad. Same action+goal = same pattern.

Read `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`:

| Match | Criteria | Action |
|-------|----------|--------|
| **Exact** | Same action AND goal | Seen++. No new entry. |
| **Near** | Same goal, different action (or vice versa) | Merge: best wording, combine triggers, Seen++. |
| **Distinct** | Different goal | Add new entry. |

Pre-filter: new Goal shares 3+ words with existing → Near candidate. Merging: keep most general trigger.

**Updating existing entries:** Grep by title/trigger phrase — do NOT read full file. Edit only that entry.

#### Entry format

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

**Rules:**
- Must name a **cognitive error** — can't name in 3-5 words → describing an event.
- Must be **domain-free** — no file/tool/framework/role names. Pure thinking logic.
- Must be **non-obvious** — "write tests" is obvious. "Existence ≠ active participation" is not.
- Max 2 entries per session. Every entry must have Cognitive Error, Triad, Adapted.
- **Scope:** universal = any project/stack/domain → `## Universal`. Situational = specific context → `## Situational` + `Situation` field.
- **Backward compat:** old entries without Cognitive Error remain valid. New entries MUST include it.

### Step 4: Summary (5 sec)

Count unadapted triads: rows where line **ends with** `| — |` (use `| — |$` — middle columns also contain `| — |`, don't count those).

Show: `Quick Learning: {1 sentence summary, or "Clean session, no signals detected."}`
If count ≥ 25: append "Накопилось {N} необработанных триад — запусти /skill-trainer."

## Three-Tier Knowledge System

| Tier | File | Purpose | Writers | Readers |
|------|------|---------|---------|---------|
| 0 | `triad-index.md` | 1-line dedup index + Adapted col | ql | ql (always), skill-trainer |
| 1 | `reasoning-patterns.md` | Full entries + context | ql | ql (on merge only) |
| 2 | `{skill}/SKILL.md` | Embedded instructions | skill-trainer | skill itself |
| 3 | `quick-ref-{skill}.md` | Top-10 reminders | skill-trainer | skill at start |

Quick-ref files: `$AGENTS_HOME/skills/quick-learning/references/quick-ref-{skill-name}.md`.

### Triad Index format

File: `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`

```markdown
| # | Trigger | Action | Goal | Scope | Seen | Section | Adapted |
|---|---------|--------|------|-------|------|---------|---------|
| 1 | before review | run smoke test | avoid wasted review rounds | universal | 2 | Universal | feature-execution |
```

- Updated on every write/merge/Seen increment. Never removed.
- `Adapted: —` = unprocessed. `{skill}` = embedded. `n/a` = no matching skill.

### Guard-triggered Seen increment

When a guard catches an error matching an existing pattern's trigger — increment Seen in triad-index.md, even outside quick-learning flow.

## Self-Verification

- [ ] Signal gate checked — clean sessions skipped
- [ ] Context waste checked separately from scope change
- [ ] **Cognitive error named** — 3-5 word name on every new entry
- [ ] **Domain-strip passed** — no domain nouns, still a thinking rule
- [ ] **Triad orientation** — Trigger=situation type, Action=corrective rule, Goal=trap name
- [ ] No duplicates — existing patterns got Seen++
- [ ] Max 2 entries, Adapted: — set on all new entries
- [ ] Summary shown; `| — |$` count; if ≥25 → notify about /skill-trainer
