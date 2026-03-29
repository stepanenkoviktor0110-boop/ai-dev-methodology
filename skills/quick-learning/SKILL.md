---
name: quick-learning
description: |
  Owner of the unified methodology knowledge system: format, triad structure,
  similarity check, 4-tier graduation, and promotion rules.

  Two writers feed this system:
  - quick-learning (this skill) — reasoning patterns from sessions (HOW decisions were made)
  - retrospective — operational lessons from features (WHAT went wrong and why)

  Both write to the same buffer (reasoning-patterns.md) using the same triad format.
  Signal-gated: skips clean sessions automatically (zero cost).

  Automatic trigger: called by feature-execution, do-task, design-generate (context exhaustion),
  and design-retrospective (before next-session prompt).
  Manual trigger: "quick learning", "быстрый анализ", "что улучшить в процессе"
---

# Quick Learning

**Format owner** for the unified methodology knowledge system. Defines triad structure, similarity check, and promotion pipeline. Both quick-learning and retrospective follow these rules when writing entries.

**Time budget:** Under 60 seconds. This is NOT a full retrospective.
**Input:** `work/{feature}/decisions.md` + git log of current session
**Output:** entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`
**Language:** Entries in Russian (they serve the user community), communication in Russian.

## What This Is NOT

- NOT a retrospective (that's `/retrospective` — runs after full feature, analyzes WHAT went wrong)
- NOT a code review (that's done per-task by reviewers)
- quick-learning focuses on HOW decisions were reached; retrospective focuses on WHAT problems occurred
- Both write to the same buffer using the same format defined here

## Design: TRIZ-Optimized

Four contradictions resolved via TRIZ principles:

1. **Signal gate** (TRIZ-15: Dynamicity) — don't analyze by schedule, analyze by signal. No signals = skip immediately, zero token cost.
2. **Write-only subagent** (TRIZ-2: Extraction) — the subagent ONLY writes patterns. It never reads the full buffer. Reads triad-index.md (~30 lines) for dedup only. Application of patterns happens through promoted instructions already in skills.
3. **Three-tier graduation** (TRIZ-1: Segmentation + TRIZ-10: Prior action) — raw buffer → skill instructions → quick reference card. Each tier is smaller and cheaper to read than the previous.
4. **Scope segmentation** (TRIZ-1: Segmentation) — universal patterns (always apply) vs situational (context-matched). Different read cost, different application rules.

## Procedure

### Step 1: Signal Gate (5 sec)

Check 3 binary signals. If ALL are zero — **skip entirely** with summary "Clean session, no new patterns." and move on.

| Signal | How to check | Meaning |
|--------|-------------|---------|
| Fix rounds | `git log --oneline -20` — count `fix:` commits | Something went wrong and was corrected |
| Scope change | `decisions.md` — any deviation, unplanned work, changed approach | Plan didn't survive contact with reality |
| Recovery event | `git log` — rollbacks, retries, blocked→unblocked | A non-obvious recovery path was found |

**For design sessions** (called from design-generate or design-retrospective), use design-specific signals:

| Signal | How to check | Meaning |
|--------|-------------|---------|
| Iteration rounds | Count user feedback cycles in session | Multiple rounds = initial approach missed the mark |
| Taste correction | User changed color/font/spacing after proposal | Proposal didn't match user's aesthetic sense |
| Layout rework | User rejected layout and asked for different one | Wrong layout pattern selected for the content |

**If at least 1 signal is present → proceed to Step 2.**

### Step 2: Analyze (15 sec)

For each detected signal, ask:

1. **Was the first approach the right one?** If not — what signal should have told us to try something different earlier?
2. **What was the actual cost of the detour?** (fix rounds, wasted review cycles, rework)
3. **Is this transferable?** Would this insight help someone on a DIFFERENT project?

If analysis produces nothing non-obvious — **skip writing**. Don't force lessons.

### Step 3: Write (20 sec)

If insights found, append to the appropriate section of `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`.

**Before writing — run the Similarity Check (mandatory).**

#### Similarity Check

Each pattern is decomposed into a **trigger → action → goal** triad. Two patterns are the SAME if they share the same action+goal, even with different wording or trigger.

1. Formulate your new insight as a triad:
   - **Trigger:** what situation or signal initiates the action (e.g. "before spawning reviewers")
   - **Action:** what to DO (the verb, e.g. "run smoke test")
   - **Goal:** what outcome this achieves (e.g. "avoid wasting review rounds on broken code")

2. Read `$AGENTS_HOME/skills/quick-learning/references/triad-index.md` (~20 lines max). For each existing row, compare triads:

| Match level | Criteria | What to do |
|-------------|----------|-----------|
| **Exact** | Same action AND same goal | Increment `Seen` counter. Do NOT add new entry. |
| **Near** | Same goal, different action (or same action, different goal) | **Merge**: keep the more actionable wording, combine triggers, increment `Seen`. |
| **Distinct** | Different goal | Add as new entry. |

**Mechanical pre-filter:** if the Goal of a new triad shares 3+ content words (nouns/verbs, ignoring stop-words) with an existing Goal — treat it as a Near match candidate and verify manually. This reduces reliance on subjective judgment.

**Examples of SAME (exact or near):**

```
Existing:  trigger: "before review"      → action: "run smoke test"   → goal: "don't waste review on broken code"
New:       trigger: "before code review"  → action: "verify it builds" → goal: "avoid review cycles on non-working code"
Verdict:   NEAR — same goal, similar action. Merge, Seen++.
```

```
Existing:  trigger: "multi-task feature"  → action: "define shared types in task 1" → goal: "avoid type drift"
New:       trigger: "shared data model"   → action: "centralize types early"        → goal: "prevent inconsistency across tasks"
Verdict:   NEAR — same goal. Merge, Seen++.
```

**Example of DISTINCT:**

```
Existing:  trigger: "before review"  → action: "run smoke test"       → goal: "don't waste review rounds"
New:       trigger: "before review"  → action: "check test coverage"  → goal: "ensure tests exist for new code"
Verdict:   DISTINCT — same trigger, but different goal. Add as new.
```

When merging, keep the **most general trigger** and the **most actionable wording**. Update the date to the latest occurrence.

#### Entry format

```markdown
### {YYYY-MM-DD} {feature-name} / session {N}: {pattern title}

**Seen:** 1 (this feature/session)
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
- **Must capture REASONING LOGIC, not implementation specifics.** The pattern should be transferable to any project. Bad: "удалять Лист1 в Google Sheets по имени". Good: "при программном создании документа — зачищать дефолтные артефакты по имени, не по содержимому". If you can't remove the technology name from the pattern and it still makes sense — it's too specific.
- Max 2 entries per session (retrospective allows max 3 per feature — larger scope).
- **Every entry MUST have a Triad field** — this is the key for similarity matching.

### Step 4: Summary (5 sec)

Show user ONE line:

```
Quick Learning: {1 sentence summary, or "Clean session, no signals detected."}
```

Move on to session end protocol.

## Three-Tier Knowledge System

Patterns live in three tiers. Each tier is smaller, cheaper, and more permanent than the previous.

```
Tier 0: Triad Index                 Tier 1: Transit Buffer         Tier 2: Skill Instructions     Tier 3: Quick Reference Cards
triad-index.md                      reasoning-patterns.md          {skill}/SKILL.md               quick-ref-{skill-name}.md
━━━━━━━━━━━━━━━━━━━━━               ━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━
1-line summaries of all triads      Full entries with context       Promoted patterns (Seen ≥ 2)   Top 10 one-liners per skill
~1 line per pattern                 Seen counter, scope, category   Permanent, loaded by skill     Loaded at session START
Read: ALWAYS (for similarity)       Read: only on merge/promote     Read: by skill itself          Read: max 10 lines per file
Writers: quick-learning + retro     Writers: quick-learning + retro Written: at promotion          Auto-generated per skill
```

### Tier 0: Triad Index (the similarity engine)

File: `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`

Compact index of all patterns — one line per entry. The subagent reads ONLY this file for similarity check (~20 lines max). This is what makes dedup cheap.

Format:
```markdown
# Triad Index
| # | Trigger | Action | Goal | Scope | Seen | Section |
|---|---------|--------|------|-------|------|---------|
| 1 | before review | run smoke test | avoid wasted review rounds | universal | 2 | Universal |
| 2 | multi-task feature | define shared types in task 1 | prevent type drift | situational | 1 | Situational |
```

**Rules:**
- Updated on every write, merge, or promotion.
- When a pattern is promoted (Seen ≥ 2) — remove its row from the index.
- The subagent reads triad-index.md (~30 lines) instead of the full reasoning-patterns.md for similarity matching.
- After finding a match in the index, the subagent locates the corresponding entry in reasoning-patterns.md by matching its title (`### date feature: title`).

### Tier 1 → Tier 2: Promotion (when Seen reaches 2)

1. Identify target skill by category:

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

2. Add the pattern as a permanent instruction in the target skill's SKILL.md (1-2 lines, imperative).
3. Remove the entry from reasoning-patterns.md.
4. Regenerate `quick-ref-{skill-name}.md` for the target skill (see Tier 3 below).
5. Log: `Quick Learning: promoted "{pattern}" → {skill} SKILL.md`

#### Guard-triggered Seen increment

When a guard (smoke test, reviewer, self-verification) catches an error that matches an existing pattern's trigger, increment that pattern's Seen counter in `triad-index.md` — even outside the quick-learning flow. This creates a feedback loop: patterns that keep catching real issues get promoted faster.

#### Manual promote

User can say "promote pattern {N}" (where N is the row number in triad-index.md) to force-promote any pattern to its target skill regardless of Seen count. Follow the same promotion steps 1-5 above.

### Tier 2 → Tier 3: Quick Reference Cards (per-skill)

Files: `$AGENTS_HOME/skills/quick-learning/references/quick-ref-{skill-name}.md`

Auto-generated per skill from promoted patterns filtered by category. Max 10 entries per file, sorted by Seen desc. Each pipeline skill reads its own file at session start.

Category-to-file mapping (derived from category-to-skill table above):

| File | Categories |
|------|-----------|
| `quick-ref-feature-execution.md` | sequencing, recovery, communication |
| `quick-ref-tech-spec-planning.md` | information-gathering |
| `quick-ref-task-decomposition.md` | problem-decomposition |
| `quick-ref-user-spec-planning.md` | scope-management |
| `quick-ref-code-writing.md` | tool-selection |
| `quick-ref-do-task.md` | orchestration-level patterns (cross-cutting, not covered by categories above) |
| `quick-ref-design-system-init.md` | design-taste |
| `quick-ref-design-generate.md` | design-process |
| `quick-ref-design-retrospective.md` | design-iteration |

Format per file:

```markdown
# Quick Reference — {Skill Name}

1. {one-line pattern} (Seen: N)
2. {one-line pattern} (Seen: N)
...
```

Cost: max 10 lines of context per skill. Benefit: only relevant patterns loaded.

**When to regenerate:** when a pattern is promoted to a specific skill, regenerate that skill's `quick-ref-{skill-name}.md`. Read all promoted patterns from the target skill's SKILL.md, pick top 10 sorted by Seen desc, rewrite the file.

## Self-Verification

- [ ] Signal gate checked — clean sessions skipped
- [ ] Extracted patterns are about reasoning LOGIC, not specific technical decisions
- [ ] Scope correctly classified (universal vs situational)
- [ ] No duplicates — existing patterns got Seen++ instead
- [ ] Max 2 entries written
- [ ] Promotions executed if any pattern reached Seen: 2
- [ ] Summary shown to user
