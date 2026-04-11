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

**Format owner** for the unified methodology knowledge system. Defines triad structure, similarity check, Seen counters, and Adapted tracking. Both quick-learning and retrospective follow these rules when writing entries.

**Time budget:** Under 60 seconds. This is NOT a full retrospective.
**Input:** `work/{feature}/decisions.md` + git log of current session
**Output:** entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`
**Language:** Entries in Russian, communication in Russian.

## What This Is NOT

- NOT a code review (that's done per-task by reviewers)
- NOT responsible for embedding patterns into skills (that's `/skill-trainer`)

## Design: TRIZ-Optimized

1. **Signal gate** (TRIZ-15: Dynamicity) — analyze by signal, not schedule. No signals = skip immediately, zero cost.
2. **Write-only** (TRIZ-2: Extraction) — only writes patterns. Reads triad-index.md for dedup only. Embedding into skills is done by skill-trainer.
3. **Three-tier graduation** (TRIZ-1: Segmentation + TRIZ-10: Prior action) — raw buffer → skill instructions → quick reference. Each tier smaller and cheaper.
4. **Scope segmentation** (TRIZ-1) — universal vs situational. Different read cost, different application rules.

## Procedure

### Step 1: Signal Gate (5 sec)

Check 4 binary signals. If ALL are zero — **skip entirely** with "Clean session, no new patterns."

| Signal | How to check | Meaning |
|--------|-------------|---------|
| Fix rounds | `git log --oneline -20` — count `fix:` commits | Something went wrong and was corrected |
| Scope change | `decisions.md` — any deviation, unplanned work, changed approach | Plan didn't survive contact with reality |
| Recovery event | `git log` — rollbacks, retries, blocked→unblocked | A non-obvious recovery path was found |
| Context waste | `decisions.md` — Concerns field contains description of repeated reads of unchanged file | Inefficient tool use, not a logic error |

**For design sessions** (called from design-generate):

| Signal | How to check | Meaning |
|--------|-------------|---------|
| Iteration rounds | Count user feedback cycles in session | Multiple rounds = initial approach missed |
| Taste correction | User changed color/font/spacing after proposal | Proposal didn't match aesthetic sense |
| Layout rework | User rejected layout and asked for different one | Wrong layout pattern selected |

**If at least 1 signal is present → proceed to Step 2.**

> Checkpoint: at least one signal confirmed. If all signals are zero — exit with "Clean session."

### Step 2: Analyze (15 sec)

> **Scope change vs Context waste:** scope change = *what* was done changed (plan didn't hold); context waste = *how* it was done was inefficient (tool used suboptimally). Both may appear in the same session — analyze independently.

For each detected signal, ask:

1. **Was the first approach right?** If not — what signal should have told us to try something different earlier?
2. **What was the actual cost of the detour?** (fix rounds, wasted review cycles, rework)
3. **Is this transferable?** Would this insight help someone on a DIFFERENT project?

Write only patterns that are genuinely non-obvious and transferable. Skip if analysis produces nothing new.

### Step 3: Write (20 sec)

Append to `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`.

**Run the Similarity Check before writing (mandatory).**

#### Similarity Check

Decompose insight into a **trigger → action → goal** triad. Two patterns are the SAME if they share action+goal, even with different wording.

1. Formulate triad: **Trigger** / **Action** / **Goal**
2. Read `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`. Compare each row:

| Match level | Criteria | What to do |
|-------------|----------|-----------|
| **Exact** | Same action AND same goal | Increment `Seen`. Do NOT add new entry. |
| **Near** | Same goal, different action (or same action, different goal) | Merge: keep most actionable wording, combine triggers, Seen++. |
| **Distinct** | Different goal | Add as new entry. |

**Mechanical pre-filter:** if new Goal shares 3+ content words with existing Goal — treat as Near match candidate and verify manually.

When merging: keep the most general trigger and most actionable wording. Update date.

**Updating reasoning-patterns.md (Exact / Near):** Use Grep to locate the entry by pattern title or unique trigger phrase — do NOT read the full 235 KB file. Then use Edit to update only that entry (increment Seen, update trigger/wording if merging).

#### Entry format

```markdown
### {YYYY-MM-DD} {feature-name} / session {N}: {pattern title}

**Seen:** 1
**Adapted:** —
**Triad:** {trigger} → {action} → {goal}
**Context:** {what situation triggered this insight — 1 sentence}
**Pattern:** {the transferable reasoning approach — 1-2 sentences, imperative}
**Scope:** {universal | situational}
**Situation:** {only for situational — when this applies}
**Category:** {sequencing | information-gathering | problem-decomposition | scope-management | recovery | communication | tool-selection | design-taste | design-process | design-iteration}
```

**Scope rules:**
- **universal** — any project, any stack, any domain. Goes to `## Universal` section.
- **situational** — specific context required. Goes to `## Situational` section. Must have `Situation` field.

**Writing rules:**
- Must be actionable — a concrete instruction, not vague advice.
- Must be non-obvious — "write tests" is obvious. "Run smoke before spawning reviewers" is not.
- Must capture REASONING LOGIC, not implementation specifics. Transferable to any project. Bad: "удалять Лист1 в Google Sheets по имени". Good: "при программном создании документа — зачищать дефолтные артефакты по имени, не по содержимому".
- Max 2 entries per session.
- Every entry must have Triad and Adapted fields.

**Abstraction gate (mandatory before writing — applies to ALL fields, not just Triad):**
For each field (Triad, Context, Pattern), apply this test:
1. Replace every product/service/file/component name with its category. "Vercel" → "хостинг-платформа", "page.tsx" → "entry point", "Barista" → "компонент", "globals.scss" → "глобальный стилевой файл".
2. If the field still makes sense after replacement — it's abstract enough. If it becomes meaningless — the logic was hiding behind the specific name; reformulate.
3. Every field must answer "what reasoning error to avoid" — not "which file to check" or "which button to click".

Bad Context: "Включил Barista в tech-spec, но он закомментирован в page.tsx" → project-specific.
Good Context: "Включил компонент в scope рефакторинга по наличию файлов, но он был отключён в entry point" → transferable.
Bad Pattern: "Проверяй page.tsx на закомментированные импорты" → file-specific.
Good Pattern: "Проверяй entry point на фактический рендеринг каждого компонента перед включением в scope" → transferable.

> Checkpoint: reasoning-patterns.md and triad-index.md both updated. New entries ≤ 2. Adapted: — set on all new rows.

### Step 4: Summary (5 sec)

Count rows where the **last column** (`Adapted`) is exactly `—`. Use pattern `| — |$` (line ends with `| — |`).

**WARNING:** many rows contain `| — |` in middle columns (Goal, Section). Do NOT count those. Only rows where the ENTIRE line ends with `| — |` qualify. Using `| — |` without `$` anchor will produce ~2× overcounts.

Show user ONE line:
```
Quick Learning: {1 sentence summary, or "Clean session, no signals detected."}
```

If count ≥ 25: append "Накопилось {N} необработанных триад — запусти /skill-trainer."

## Three-Tier Knowledge System

```
Tier 0: Triad Index          Tier 1: Transit Buffer        Tier 2: Skill Instructions    Tier 3: Quick Ref Cards
triad-index.md               reasoning-patterns.md         {skill}/SKILL.md              quick-ref-{skill}.md
━━━━━━━━━━━━━━━━━━━━         ━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━            ━━━━━━━━━━━━━━━━━━━━
1-line + Adapted col         Full entries + context        Embedded by skill-trainer     Generated by skill-trainer
Read: ALWAYS (dedup)         Read: on merge only           Read: by skill itself         Read: by skill at start
Writers: ql                  Writers: ql                   Managed by: skill-trainer     Stored in: this references/
```

Quick-ref files live in `$AGENTS_HOME/skills/quick-learning/references/quick-ref-{skill-name}.md`.
They are written by skill-trainer after embedding, not by quick-learning.
Each pipeline skill reads its own file at session start for a top-10 pattern reminder.

### Tier 0: Triad Index (the similarity engine)

File: `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`

Compact index of all patterns — one line per entry. Read ONLY this file for similarity check.

Format:
```markdown
# Triad Index
| # | Trigger | Action | Goal | Scope | Seen | Section | Adapted |
|---|---------|--------|------|-------|------|---------|---------|
| 1 | before review | run smoke test | avoid wasted review rounds | universal | 2 | Universal | feature-execution |
| 2 | multi-task feature | define shared types in task 1 | prevent type drift | situational | 1 | Situational | — |
```

**Rules:**
- Updated on every write, merge, or Seen increment.
- Entries are never removed — Adapted column tracks processing status.
- `Adapted: —` = not yet processed by skill-trainer.
- `Adapted: {skill}` = embedded into that skill. Multiple skills: comma-separated.
- `Adapted: n/a` = reviewed by skill-trainer, no matching skill found.

### Guard-triggered Seen increment

When a guard (smoke test, reviewer, self-verification) catches an error matching an existing pattern's trigger — increment Seen in `triad-index.md`, even outside quick-learning flow. Patterns catching real issues get prioritized by skill-trainer.

## Self-Verification

- [ ] Signal gate checked — clean sessions skipped
- [ ] Context waste signal checked separately from scope change
- [ ] Patterns capture reasoning LOGIC, not specific technical decisions
- [ ] Scope correctly classified (universal vs situational)
- [ ] No duplicates — existing patterns got Seen++ instead
- [ ] Max 2 entries written
- [ ] Adapted: — field set on all new entries in both reasoning-patterns.md and triad-index.md
- [ ] Summary shown; count by pattern `| — |$` (last column only — NOT `| — |` without anchor); if ≥25 — user notified about /skill-trainer
