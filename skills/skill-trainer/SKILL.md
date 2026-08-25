---
name: skill-trainer
disable-model-invocation: true
description: |
  Embeds accumulated triads from quick-learning into target skills as permanent instructions.
  Reads triads with Adapted=— from triad-index.md, analyzes each skill's existing logic,
  auto-applies new rules when no coverage exists, proposes refinements when partial coverage found.
  After embedding, updates Adapted field and cleans reasoning-patterns.md.

  Use when: "/skill-trainer", "обучи скиллы", "применить триады к скиллам", "встрой паттерны",
  "skill trainer", "обработай триады", "embed triads into skills", "apply learned patterns",
  "promote patterns to skills"
  Also triggered by: quick-learning after writing, when ≥25 entries with Adapted=— exist.
---

# Skill Trainer

Embeds accumulated quick-learning triads into target skills. Two outcomes per triad:
- **Auto-apply** — skill has no coverage of this case → add new rule directly
- **Dispute** — skill already has related logic but doesn't cover the specific case → propose refinement to user

## How a skill gets changed

Every edit this skill makes to another skill follows
[refinement-patterns.md](references/refinement-patterns.md) — fourteen patterns with the trigger
that calls each one, the change, and how to tell it landed. Read it before Phase 3, and again in
Phase 6.5 when auditing the result.

The two that decide where a rule goes:

| Triad describes | Embed as | Where |
|---|---|---|
| A judgement to make while working | one-line rule `When {trigger} → {action}, to {goal}` | Learned Patterns / write target |
| A state that can be read off disk — a file that must exist, a field that must be set, a command whose output settles it | a command | the skill's "Checks against state" section |

Prefer the command (P13). A rule restated as a self-check tick-box catches nothing: an executor that broke the rule in the body will not catch itself with a copy of that rule. Only reach for a prose rule when nothing on disk can answer the question.

Then prove it (P15). A command goes into a skill only after it has been run against live project data and matched something. One that matches nothing always returns empty, and empty reads as "the step was taken" — worse than no check at all. Measured 2026-08-20: `do-task` carried two such commands, both silently passing for as long as they existed.

Write every embedded rule in **English**, whatever language the session ran in (P7).

When a pattern here changes how skills are written, update
`project-knowledge/references/patterns.md` in the same pass (P14) — otherwise the next skill
authored against those conventions restores what was just removed.

## Category → Skill Mapping

| Category | Target skill |
|----------|-------------|
| sequencing | feature-execution |
| information-gathering | tech-spec-planning |
| problem-decomposition | task-decomposition |
| scope-management | user-spec-planning |
| recovery | feature-execution |
| communication | feature-execution |
| tool-selection | code-writing |

## Phase 1: Check

1. Count unadapted rows. Run this, do not hand-roll the pattern:

```bash
IDX="$AGENTS_HOME/skills/quick-learning/references/triad-index.md"
rg -c '\| — \|\s*$' "$IDX"          # unadapted rows
rg -c '^\| [0-9]+ ' "$IDX"           # all triad rows, for scale
```

**The end-of-line anchor is the whole check.** `Goal`, `Scope` and `Section` also hold `—`, so
`Adapted` is only the em dash that ends the row. Dropping `\s*$` counts adapted rows as
unadapted and inflates the number severalfold. Measured 2026-08-25: the unanchored pattern
reported 43 where the true count was 16, and the gate below was declared open when it was shut.
The file has CRLF endings, which is why the anchor is `\s*$` and not `$`.

2. If count < 25 → report: "Skill Trainer: {count}/25 триад накоплено. Запуск при ≥25." and exit.
   The number in that line is the command's output, never a recollection or a hand-made count.
3. If count ≥ 25 → proceed.

## Phase 2: Load Triads

1. Read `triad-index.md` — collect the unadapted rows with the same anchored pattern as Phase 1:

```bash
rg -n '\| — \|\s*$' "$AGENTS_HOME/skills/quick-learning/references/triad-index.md"
```

   The row count here must equal Phase 1's count. A larger set means the anchor was dropped again,
   and adapted triads are about to be re-embedded on top of rules that already exist.
2. For each row, load the full entry from `reasoning-patterns.md` by matching the title `### {date} {feature}: {title}`
3. Group triads by target skill using the Category → Skill mapping above

Secondary mapping: if the triad's Pattern field explicitly describes a workflow step present in another skill — add that skill to the list (max 2 target skills per triad).

## Phase 3+4: Analyze and Apply (delegated to Agents)

Spawn one Agent per target skill that has ≥1 triad assigned. Each skill is a genuinely
independent file, which is what makes delegation pay here. Do not split one skill across
several agents, and do not spawn an agent to review another agent's edit.

Agent prompt template:
```
You are processing skill-trainer triads for skill: {skill-name}
SKILL.md path: $AGENTS_HOME/skills/{skill-name}/SKILL.md

Triads to process (id | trigger | action | goal | scope):
{paste each triad row as-is from triad-index.md}

Task:
0. Read $AGENTS_HOME/skills/skill-trainer/references/refinement-patterns.md. Every edit
   you make below follows it.
1. Read SKILL.md
2. Find the "## Learned Patterns" section. Check if it contains a lazy-load reference
   (a link to a references/*.md file). If yes — that file is the write target.
   If no lazy-load reference — SKILL.md itself is the write target.
3. Read the write target file (if different from SKILL.md)
4. For each triad, search for existing logic covering the same trigger or goal
5. Classify each triad:
   - auto-apply: no coverage → add it. If the triad is settled by state on disk, add a
     command to the skill's "Checks against state" section instead of a prose rule (P13),
     and state what its result must be (P2).
     Otherwise add "When {trigger} → {action}, to {goal}" to the write target file
     (if writing to SKILL.md and no ## Learned Patterns section exists, create it at end of file)
   - dispute: partial coverage exists → do NOT edit file, return existing rule + proposed refinement
   - skip: already fully covered → no changes

6. Write in English regardless of the language of the triad text (P7).
7. Apply all auto-apply edits to the write target (Edit tool)
8. While you are in this file, report — do not fix — any violation of the patterns you
   noticed: a surviving self-check checklist (P1), a round counter (P5), a model or effort
   level in the body (P6), a named skill or agent that does not exist (P9), a
   machine-specific path (P10). Return them in `observed` so the owner decides.
9. Do NOT touch triad-index.md — main context will update it

Return ONLY this JSON (no extra text):
{
  "skill": "{skill-name}",
  "write_target": "{path to file where rules were written}",
  "applied": [{"id": N, "rule": "one-line rule added", "carrier": "command|rule"}],
  "disputes": [{"id": N, "existing": "...", "proposed": "..."}],
  "skipped": [N, N],
  "observed": [{"pattern": "P5", "evidence": "line 88: max 3 rounds"}]
}
```

Run all skill agents in parallel. Collect all JSON results before proceeding.

### Update triad-index.md (single pass)

After collecting all agent results — update `Adapted` in triad-index.md in one edit:
- applied triads → set `Adapted` to `{skill-name}`
- skipped triads → set `Adapted` to `{skill-name}`
- disputed triads → leave `Adapted: —` (will be resolved in Phase 5)

## Phase 5: Disputes

Present each dispute to the user one at a time, in Russian, and wait for a decision before
showing the next one:

```
Dispute: "{pattern title}" → {skill-name}

Триада: {trigger} → {action} → {goal}

Существующее правило (строка ~{N}):
  "{existing rule text}"

Предлагаю расширить до:
  "{refined rule text covering both cases}"

Применить? [да / нет / пропустить]
```

- **да** → apply the refinement, update Adapted in triad-index.md, add to removal list
- **нет** → skip, leave Adapted=— (will appear again next run)
- **пропустить** → mark Adapted: n/a in triad-index.md, add to removal list

### Cleanup

Remove all collected entries from reasoning-patterns.md in a single pass — find each entry by its `### {title}` header and delete it with surrounding blank lines.

## Phase 6: Quick-Ref Regeneration

After all changes for a skill are applied, regenerate that skill's quick-ref card:

File: `$AGENTS_HOME/skills/quick-learning/references/quick-ref-{skill-name}.md`

Collect all patterns from the target skill's write target (either SKILL.md "Learned Patterns" section or externalized references file — use `write_target` from agent result) + Promoted Patterns from SKILL.md, pick top 10 sorted by Seen desc, write:

```markdown
# Quick Reference — {Skill Name}

1. {one-line pattern} (Seen: N)
2. {one-line pattern} (Seen: N)
...
```

## Phase 6.5: Quality Check (post-embedding)

For each skill that received auto-applies — spawn one Agent in parallel.
Full checklist, agent prompt and output format: [references/quality-checklist.md](references/quality-checklist.md).

Two levels:
1. **General compliance** — each agent calls the existing `skill-checker` agent (size, structure, references, checkpoints, and the refinement patterns). Not duplicated here.
2. **Skill-trainer-specific** — items A1–A3 (size discipline) and B1–B6 (rule quality on the new rules).
3. **Dead-check gate (mechanical, not a judgement).** Run `node ~/.claude/hooks/checks-audit.mjs`. It parses every `## Checks against state` command in every skill and runs it against live project data. Any command named in its output that this pass wrote or touched is a **failed** item, not a warning: it never matched anything and never will.

The `observed` entries returned in Phase 3+4 join this report. They are findings about the skill,
not about the new rules, so they are shown to the owner rather than fixed silently — a pattern
violation predating this run may be deliberate.

Soft gate:
- All pass → silent, proceed to Phase 7
- Only warnings → one line in the final Report
- Any failed → show a summary and ask: fix / record in known-issues / ignore

## Phase 7: Commit

After all changes across all skills:

```
git add -A && git commit -m "skill-trainer: embed {N} triads into {skill list}"
```

## Force-Embed (manual)

User can say "force-embed pattern {N}" to embed a specific triad immediately, bypassing the ≥25 threshold. Run Phase 3–7 for that single triad only.

## Report

```
Skill Trainer: обработано {N} триад.
Применено автоматически: {N} правил → {skills list}
Споров решено: {resolved}/{total disputes}
Пропущено (уже покрыто): {N}
Отложено (нет/пропустить): {N}
```

## Checks against state

Read the counts off disk; do not recall them.

```bash
IDX="$AGENTS_HOME/skills/quick-learning/references/triad-index.md"

# 1. every triad reported as applied or skipped no longer shows Adapted: —
#    \s* before the anchor: the rows may carry CRLF, and "\| — \|$" then matches nothing
rg -c '\| — \|\s*$' "$IDX"

# 2. removal list and reasoning-patterns.md agree — count entry headers before and after
rg -c "^### " "$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md"

# 3. a quick-ref card exists for every skill that received auto-applies
rg -l . "$AGENTS_HOME/skills/quick-learning/references/quick-ref-{skill-name}.md"

# 4. the citations this pass wrote resolve — one row per cited id, and no id answers to two rows.
#    -L: most skills are symlinks into their source repos, and without it this reads ~2 of ~150.
rg -o '^\| [0-9]+ ' "$IDX" | sort | uniq -d
for id in $(rg -L --no-ignore -o 'triads? #[0-9]+' -N "$AGENTS_HOME/skills" \
            | grep -o '[0-9]\+' | sort -u); do
  n=$(rg -c "^\| $id \|" "$IDX" || echo 0)
  [ "$n" = 1 ] || echo "triad #$id resolves to $n rows"
done

# 5. no command this pass embedded is dead — it must match live data somewhere.
#    Exit code 1 means at least one check in some skill matches nothing at all.
node ~/.claude/hooks/checks-audit.mjs

# 6. the dead-check finder still tells a live check from a dead one
node ~/.claude/hooks/test/run-checks-audit-test.mjs
```

Count 1 must have dropped by the number of applied plus skipped triads; count 2 by the size of the removal list. A mismatch means a pass wrote fewer rows than it reported — reconcile before committing, do not re-run the phase blind.

Checks 1 and 2 count the columns this pass itself writes, so they answer whether the pass did what
it said, never whether the store still holds together — they cannot report the damage they cause.
Check 4 is the independent signal: it reads the id column and the skill bodies, neither of which is
the pass's selector. It must print nothing. **Nothing here is only evidence when the loop read
something** — drop the `|| echo` guard once and confirm ids print, because a traversal that silently
reaches no files prints nothing too, and that is indistinguishable from health. Measured 2026-08-14
on a state where checks 1–3 all passed: 54 ids carried two rows and 7 citations were ambiguous, 4 of
them pointing at the wrong row.
