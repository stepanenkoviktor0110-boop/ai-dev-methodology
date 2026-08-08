---
name: quick-learning
disable-model-invocation: true
description: |
  Owner of the unified methodology knowledge system: format, triad structure,
  similarity check, Seen counters, and Adapted tracking.

  Signal-gated: skips clean sessions automatically (zero cost).

  Automatic trigger: called by feature-execution and do-task (context exhaustion).

  Use when: "quick learning", "быстрый анализ", "что улучшить в процессе",
  "извлеки паттерн", "запиши урок сессии", "analyze session patterns"
---

# Quick Learning

**Time budget:** Under 60 seconds. Not a retrospective. Not a code review.
**Input:** `work/{feature}/decisions.md` + git log of current session
**Output:** entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`

Entries are written in **English**, whatever language the session ran in. They are embedded
into skill bodies later by skill-trainer, and skill bodies carry English.

## Step 1: Signal Gate (5 sec)

Check the signals below. If ALL are zero — **exit** with "Clean session, no new patterns."

| Signal | How to check | Meaning |
|--------|-------------|---------|
| Fix rounds | `git log --oneline -20` — count `fix:` commits | Something went wrong and was corrected |
| Scope change | `decisions.md` — any deviation, changed approach | Plan didn't survive contact with reality |
| Recovery event | `git log` — rollbacks, retries, blocked→unblocked | Non-obvious recovery path found |
| Context waste | `decisions.md` — Concerns field, repeated reads | Inefficient tool use |
| Silent correction | `decisions.md` / diff — an approach was replaced mid-task without a `fix:` commit ever appearing | The detour happened but left no commit trace |

**Design sessions** — additional signals: iteration rounds, taste correction, layout rework.

At least 1 signal → proceed. All zero → exit.

> The first four signals count *commits and notes*. When an executor corrects itself inside a
> single pass, the lesson is real but the commit trail is empty — that is what the fifth signal
> catches. A gate built only on `fix:` counts goes quiet exactly as self-correction improves.

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

### Choose the carrier

A lesson that some state on disk can settle is worth more as a command than as a sentence.
Note it in the entry: `Carrier: command` when a file, a field or a command's output answers
the question, `Carrier: rule` when only judgement does. skill-trainer reads this and embeds
accordingly.

## Step 4: Summary (5 sec)

Count unadapted triads: grep `| — |$` in triad-index.md (use `$` anchor — middle columns also contain `| — |`).

Show: `Quick Learning: {1 sentence summary, or "Clean session, no signals detected."}`
If count ≥ 25: append "Накопилось {N} необработанных триад — запусти /skill-trainer."

### Recurring-defect detector

Run the measurement in [recurring-defect.md](references/recurring-defect.md): a file whose fix-ratio
is twice the repository's own baseline, over at least 8 fix commits, is where a contradiction sits.
Output non-empty → append one line naming the file and offering `/triz-synergy`. It never invokes
anything.

## Checks against state

```bash
# 1. new entries carry Adapted: — and did not exceed two per session
rg -c "^\*\*Adapted:\*\* —" "$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md"

# 2. unadapted count for the summary line, and the /skill-trainer threshold
rg -c "\| — \|$" "$AGENTS_HOME/skills/quick-learning/references/triad-index.md"

# 3. a merged pattern incremented Seen rather than adding a duplicate row
rg -n "{3-4 key words from the new pattern}" "$AGENTS_HOME/skills/quick-learning/references/triad-index.md"
```

Check 1 must have grown by at most 2. Check 3 must return one row, not two: two rows for the
same trigger and goal means the similarity check added a duplicate instead of merging.
