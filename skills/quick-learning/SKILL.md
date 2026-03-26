---
name: quick-learning
description: |
  Owner of the unified methodology knowledge system: format, triad structure,
  similarity check, 4-tier graduation, promotion, and pruning rules.

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

**Format owner** for the unified methodology knowledge system. Defines triad structure, similarity check, promotion pipeline, and pruning rules. Both quick-learning and retrospective follow these rules when writing entries.

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
- Max 2 entries per session (retrospective allows max 3 per feature — larger scope).
- **Every entry MUST have a Triad field** — this is the key for similarity matching.

### Step 3.5: Pruning Check (5 sec)

After writing, count rows in `triad-index.md`. If more than 25 rows:

1. Remove `Seen: 1` entries with date older than 30 days — from both `triad-index.md` and `reasoning-patterns.md`.
2. Merge similar entries (same goal, different wording) — combine triggers, keep most actionable wording.
3. Remove entries contradicted by later experience.

This step is **mandatory** for both quick-learning and retrospective. It is the only mechanism that keeps the buffer bounded.

### Step 4: Summary (5 sec)

Show user ONE line:

```
Quick Learning: {1 sentence summary, or "Clean session, no signals detected."}
```

Move on to session end protocol.

## Three-Tier Knowledge System

Patterns live in three tiers. Each tier is smaller, cheaper, and more permanent than the previous.

```
Tier 0: Triad Index                 Tier 1: Transit Buffer         Tier 2: Skill Instructions     Tier 3: Quick Reference Card
triad-index.md                      reasoning-patterns.md          {skill}/SKILL.md               quick-ref.md
━━━━━━━━━━━━━━━━━━━━━               ━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━
1-line summaries of all triads      Full entries with context       Promoted patterns (Seen ≥ 3)   Top 5-7 one-liners
~1 line per pattern (max 30)        Seen counter, scope, category   Permanent, loaded by skill     Loaded at session START
Read: ALWAYS (for similarity)       Read: only on merge/promote     Read: by skill itself          Read: 7 lines max
Writers: quick-learning + retro     Writers: quick-learning + retro Written: at promotion          Auto-generated
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
- When a pattern is promoted (Seen ≥ 3) — remove its row from the index.
- The subagent reads triad-index.md (~30 lines) instead of the full reasoning-patterns.md for similarity matching.
- After finding a match in the index, the subagent locates the corresponding entry in reasoning-patterns.md by matching its title (`### date feature: title`).

### Tier 1 → Tier 2: Promotion (when Seen reaches 3)

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
3. **Remove the entry from reasoning-patterns.md.**
4. Update quick-ref.md if the pattern is universal.
5. Log: `Quick Learning: promoted "{pattern}" → {skill} SKILL.md`

### Tier 2 → Tier 3: Quick Reference Card

File: `$AGENTS_HOME/skills/quick-learning/references/quick-ref.md`

Auto-generated from the strongest promoted universal patterns. Max 7 entries. Format:

```markdown
# Quick Reference — Reasoning Patterns

1. {one-line pattern}
2. {one-line pattern}
...
```

This file is loaded by feature-execution at **session start** (Phase 1). Cost: ~7 lines of context. Benefit: accumulated wisdom applied immediately.

**When to regenerate:** every time a universal pattern is promoted to Tier 2. Read all promoted universal patterns from skill SKILL.md files, pick top 7 by impact, rewrite quick-ref.md.

### Pruning

Pruning is executed by Step 3.5 (above) after every write. Trigger: triad-index exceeds 25 rows. Rules:

1. Merge similar patterns (same insight, different wording).
2. Remove `Seen: 1` entries older than 30 days — they didn't recur, noise.
3. Remove patterns contradicted by later experience.

## Self-Verification

- [ ] Signal gate checked — clean sessions skipped
- [ ] Extracted patterns are about reasoning LOGIC, not specific technical decisions
- [ ] Scope correctly classified (universal vs situational)
- [ ] No duplicates — existing patterns got Seen++ instead
- [ ] Max 2 entries written
- [ ] Promotions executed if any pattern reached Seen: 3
- [ ] Summary shown to user
