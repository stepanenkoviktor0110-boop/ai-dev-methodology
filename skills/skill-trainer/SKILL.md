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
| design-taste | design-system-init |
| design-process | design-generate |
| design-iteration | design-retrospective |

## Phase 1: Check

1. Count rows with `Adapted: —` in `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`
2. If count < 25 → report: "Skill Trainer: {count}/25 триад накоплено. Запуск при ≥25." and exit.
3. If count ≥ 25 → proceed.

## Phase 2: Load Triads

1. Read `triad-index.md` — collect all rows where `Adapted = —`
2. For each row, load the full entry from `reasoning-patterns.md` by matching the title `### {date} {feature}: {title}`
3. Group triads by target skill using the Category → Skill mapping above

Secondary mapping: if the triad's Pattern field explicitly describes a workflow step present in another skill — add that skill to the list (max 2 target skills per triad).

## Phase 3+4: Analyze and Apply (delegated to Agents)

For each target skill that has ≥1 triad assigned — spawn one Agent in parallel.

Agent prompt template:
```
You are processing skill-trainer triads for skill: {skill-name}
SKILL.md path: $AGENTS_HOME/skills/{skill-name}/SKILL.md

Triads to process (id | trigger | action | goal | scope):
{paste each triad row as-is from triad-index.md}

Task:
1. Read SKILL.md
2. For each triad, search for existing logic covering the same trigger or goal
3. Classify each triad:
   - auto-apply: no coverage → add rule to Learned Patterns section:
     "When {trigger} → {action}, to {goal}"
     (create ## Learned Patterns section at end of file if not exists)
   - dispute: partial coverage exists → do NOT edit file, return existing rule + proposed refinement
   - skip: already fully covered → no changes

4. Apply all auto-apply edits to SKILL.md (Edit tool)
5. Do NOT touch triad-index.md — main context will update it

Return ONLY this JSON (no extra text):
{
  "skill": "{skill-name}",
  "applied": [{"id": N, "rule": "one-line rule added"}],
  "disputes": [{"id": N, "existing": "...", "proposed": "..."}],
  "skipped": [N, N]
}
```

Run all skill agents **in parallel**. Collect all JSON results before proceeding.

> Checkpoint: all agents completed. Main context now holds applied/disputes/skipped lists for all skills.

### Update triad-index.md (single pass)

After collecting all agent results — update `Adapted` in triad-index.md in one edit:
- applied triads → set `Adapted` to `{skill-name}`
- skipped triads → set `Adapted` to `{skill-name}`
- disputed triads → leave `Adapted: —` (will be resolved in Phase 5)

> Checkpoint: triad-index.md updated. Proceed to disputes.

## Phase 5: Disputes

Present each dispute to the user one at a time:

```
Dispute: "{pattern title}" → {skill-name}

Триада: {trigger} → {action} → {goal}

Существующее правило (строка ~{N}):
  "{existing rule text}"

Предлагаю расширить до:
  "{refined rule text covering both cases}"

Применить? [да / нет / пропустить]
```

Wait for user decision before showing the next dispute.

- **да** → apply the refinement, update Adapted in triad-index.md, add to removal list
- **нет** → skip, leave Adapted=— (will appear again next run)
- **пропустить** → mark Adapted: n/a in triad-index.md, add to removal list

> Checkpoint: all disputes resolved. Removal list complete (auto-applies + да/пропустить decisions). Proceed to cleanup.

### Cleanup

Remove all collected entries from reasoning-patterns.md in a single pass — find each entry by its `### {title}` header and delete it with surrounding blank lines. Verify count matches removal list before writing.

## Phase 6: Quick-Ref Regeneration

After all changes for a skill are applied, regenerate that skill's quick-ref card:

File: `$AGENTS_HOME/skills/quick-learning/references/quick-ref-{skill-name}.md`

Collect all patterns embedded in the target skill (from its SKILL.md "Learned Patterns" section + other promoted rules), pick top 10 sorted by Seen desc, write:

```markdown
# Quick Reference — {Skill Name}

1. {one-line pattern} (Seen: N)
2. {one-line pattern} (Seen: N)
...
```

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

## Self-Verification

- [ ] Only triads with Adapted=— processed
- [ ] One Agent spawned per skill, all run in parallel
- [ ] Agents do NOT touch triad-index.md — only main context writes it
- [ ] triad-index.md updated in a single pass after all agents complete
- [ ] Auto-applies written before disputes presented
- [ ] Disputes shown one at a time, not as a batch
- [ ] reasoning-patterns.md entries removed in a single pass after all decisions, count verified
- [ ] Quick-ref cards regenerated for modified skills
- [ ] Final report shown
