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

**Step A2 — Knowledge vs Reasoning gate.** What fixes the problem — "learn a fact" or "change how you reason"?
- Fix = learn a fact (checklist item, OWASP rule, linting rule, framework API, docs) → **knowledge, skip.**
- Fix = change the reasoning process (no checklist would catch this, expert still falls for it) → **reasoning, proceed.**
- Indicator: if the pattern reduces to a checklist entry (security, code style, API usage) — it's knowledge. If no existing checklist covers it — it's reasoning.

**Step B — Domain-strip test.** Mechanical, not mental. Do NOT skip sub-steps.

**B1. Write draft** triad (Trigger → Action → Goal) using whatever words come naturally.

**B2. List every domain noun** in the draft: tool names, file names, framework names, platform names, role names, project-specific terms, technical stack terms. Write the list explicitly.

**B3. Replace each domain noun** with its abstract equivalent or delete it. If a field becomes empty or loses meaning → the pattern is domain-specific, skip it.

**B4. Verify:** read the stripped version aloud. Would someone working on a completely different project (mobile game, hardware driver, marketing campaign) understand and benefit from this rule? No → rewrite or skip.

| Level | Example | Verdict |
|-------|---------|---------|
| Bad | "проверить project-knowledge перед деплоем на Vercel" | 3 domain nouns → domain-specific |
| Bad | "после объединения задач пересчитать wave по depends_on" | Domain-specific → meaningless after strip |
| Medium | "после мутации графа перевалидировать топологический порядок" | Structural, but no cognitive error |
| Good | "решение казалось очевидным из категории объекта — не проверил данные о конкретном случае. Ошибка: category default bias" | Cognitive error, domain-free, transferable |

**⚠️ Common failure mode:** writing abstract Cognitive Error name but leaving domain nouns in Trigger/Action/Goal fields. ALL THREE fields must pass domain-strip independently.

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
- [ ] **Knowledge vs Reasoning passed** — fix = "learn fact" → skip; fix = "change reasoning" → proceed
- [ ] **Domain-strip passed** — ran B1→B4 mechanically; listed domain nouns explicitly; ALL THREE triad fields stripped independently
- [ ] **Triad orientation** — Trigger=situation type, Action=corrective rule, Goal=trap name
- [ ] No duplicates — existing patterns got Seen++
- [ ] Max 2 entries, Adapted: — set on all new entries
- [ ] Summary shown; `| — |$` count; if ≥25 → notify about /skill-trainer
