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

**Time budget:** Under 60 seconds. Not a retrospective. Not a code review.
**Input:** `work/{feature}/decisions.md` + git log of current session
**Output:** entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`

## Step 1: Signal Gate (5 sec)

Check 4 binary signals. If ALL zero — **exit** with "Clean session, no new patterns."

| Signal | How to check | Meaning |
|--------|-------------|---------|
| Fix rounds | `git log --oneline -20` — count `fix:` commits | Something went wrong and was corrected |
| Scope change | `decisions.md` — any deviation, changed approach | Plan didn't survive contact with reality |
| Recovery event | `git log` — rollbacks, retries, blocked→unblocked | Non-obvious recovery path found |
| Context waste | `decisions.md` — Concerns field, repeated reads | Inefficient tool use |

**Design sessions** — additional signals: iteration rounds, taste correction, layout rework.

At least 1 signal → proceed. All zero → exit.

## Step 2: Analyze (15 sec)

> Scope change = *what* changed; context waste = *how* was inefficient. Analyze independently.

For each signal:
1. **What thinking mistake?** Name the cognitive error in 3-5 words. Can't name → skip.
2. **Was the first approach right?** What signal should have told us earlier?
3. **Cost of the detour?** (fix rounds, wasted reviews, rework)
4. **Transferable?** Would someone on a different project benefit?

Skip if analysis produces only domain-specific events.

## Step 3: Write (20 sec)

### Abstraction Gate
Read [abstraction-gate.md](references/abstraction-gate.md) — run Steps A→A2→B→C mechanically. All three triad fields must pass domain-strip independently. Can't name cognitive error → skip.

### Similarity Check (grep-first)

Extract 3-4 key words from the new pattern's trigger and goal.
**Grep** `$AGENTS_HOME/skills/quick-learning/references/triad-index.md` for those words.

| Grep result | Action |
|-------------|--------|
| **No matches** | Distinct — add new entry without reading full index |
| **Matches found** | Read only matching lines ± 2 context. Classify: Exact (same action+goal → Seen++), Near (same goal, different action → merge, Seen++), or Distinct (add new) |

**Updating existing:** Grep reasoning-patterns.md by title/trigger — do NOT read full file. Edit only that entry.

### Write entry
Read [entry-format.md](references/entry-format.md) for format, rules, and triad-index spec. Max 2 entries per session.

## Step 4: Summary (5 sec)

Count unadapted triads: grep `| — |$` in triad-index.md (use `$` anchor — middle columns also contain `| — |`).

Show: `Quick Learning: {1 sentence summary, or "Clean session, no signals detected."}`
If count ≥ 25: append "Накопилось {N} необработанных триад — запусти /skill-trainer."

## Self-Verification

- [ ] Signal gate checked — clean sessions skipped
- [ ] Cognitive error named (3-5 words) on every new entry
- [ ] Knowledge vs Reasoning passed — "learn fact" → skip
- [ ] Domain-strip passed — B1→B4 run mechanically, all triad fields stripped
- [ ] Similarity check: grep-first, no full index read unless matches found
- [ ] No duplicates — existing patterns got Seen++
- [ ] Max 2 entries, Adapted: — set on all new
- [ ] Summary shown; if ≥25 unadapted → notify about /skill-trainer
