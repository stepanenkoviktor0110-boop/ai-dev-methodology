---
name: skill-trainer
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

## Phase 3: Analyze Coverage

For each (triad, target_skill) pair:

1. Read `$AGENTS_HOME/skills/{target_skill}/SKILL.md`
2. Search for existing logic that handles the same trigger or addresses the same goal
3. Classify:

| Result | Condition | Action |
|--------|-----------|--------|
| **Auto-apply** | No step/rule addresses this trigger or goal | Add new rule in Phase 4 |
| **Dispute** | A step exists that partially covers this, but misses the specific case | Queue for Phase 5 |
| **Skip** | Logic already covers this fully | Mark Adapted, no changes |

> Checkpoint: all unprocessed triads classified (auto-apply / dispute / skip). Proceed to applying changes.

## Phase 4: Auto-Apply

For each triad classified as auto-apply:

1. Find the most relevant section in the target skill's SKILL.md (match by phase topic or category)
2. If no section fits — add to a `## Learned Patterns` section at the end (create if not exists)
3. Add 1-3 lines in imperative mood: "When {trigger} → {action} ({goal})"
4. Update `Adapted` in triad-index.md: set to `{skill-name}`
5. Collect the entry title for removal (do not delete yet — removals happen in Phase 5 after disputes)

> Checkpoint: all auto-apply triads written into target skill files and Adapted updated in triad-index.md. Proceed to disputes.

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
- [ ] Coverage analysis done per skill (not just category match)
- [ ] Auto-applies written before disputes presented
- [ ] Disputes shown one at a time, not as a batch
- [ ] Adapted field updated in triad-index.md for all processed triads
- [ ] reasoning-patterns.md entries removed in a single pass after all decisions, count verified
- [ ] Quick-ref cards regenerated for modified skills
- [ ] Final report shown
