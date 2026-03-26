---
name: quick-learning
description: |
  Fast meta-analysis of session reasoning patterns. Runs automatically before
  every session break. Focuses NOT on specific decisions made, but on the LOGIC
  of decision-making — what reasoning approaches worked, what didn't, and what
  patterns can improve future work on similar projects.

  Three-tier knowledge system: transit buffer → skill instructions → quick reference card.
  Signal-gated: skips clean sessions automatically (zero cost).

  Automatic trigger: called by feature-execution and do-task before SESSION END PROTOCOL.
  Manual trigger: "quick learning", "быстрый анализ", "что улучшить в процессе"
---

# Quick Learning

Fast session analysis — extract reasoning patterns, not specific decisions.

**Time budget:** Under 60 seconds. This is NOT a full retrospective.
**Input:** `work/{feature}/decisions.md` + git log of current session
**Output:** entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`
**Language:** Entries in Russian (they serve the user community), communication in Russian.

## What This Is NOT

- NOT a retrospective (that's `/retrospective` — runs after full feature, maps problems to skills)
- NOT a code review (that's done per-task by reviewers)
- NOT about WHAT was decided — it's about HOW decisions were reached

## Design: TRIZ-Optimized

Four contradictions resolved via TRIZ principles:

1. **Signal gate** (TRIZ-15: Dynamicity) — don't analyze by schedule, analyze by signal. No signals = skip immediately, zero token cost.
2. **Write-only subagent** (TRIZ-2: Extraction) — the subagent ONLY writes patterns. It never reads the full buffer. Reads last 30 lines for dedup only. Application of patterns happens through promoted instructions already in skills.
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

**If at least 1 signal is present → proceed to Step 2.**

### Step 2: Analyze (15 sec)

For each detected signal, ask:

1. **Was the first approach the right one?** If not — what signal should have told us to try something different earlier?
2. **What was the actual cost of the detour?** (fix rounds, wasted review cycles, rework)
3. **Is this transferable?** Would this insight help someone on a DIFFERENT project?

If analysis produces nothing non-obvious — **skip writing**. Don't force lessons.

### Step 3: Write (20 sec)

If insights found, append to the appropriate section of `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`.

Before writing — **read last 30 lines** of the file. If the same insight exists, **increment its `Seen` counter** instead of adding a duplicate.

Entry format:

```markdown
### {YYYY-MM-DD} {feature-name} / session {N}: {pattern title}

**Seen:** 1 (this feature/session)
**Context:** {what situation triggered this insight — 1 sentence}
**Pattern:** {the transferable reasoning approach — 1-2 sentences, imperative}
**Scope:** {universal | situational}
**Situation:** {only for situational — when this applies, e.g. "CRUD with role-based access", "multi-session features with shared types"}
**Category:** {sequencing | information-gathering | problem-decomposition | scope-management | recovery | communication | tool-selection}
```

**Scope rules:**
- **universal** — any project, any stack, any domain. Goes to `## Universal` section.
- **situational** — specific context required. Goes to `## Situational` section. Must have `Situation` field.

**Writing rules:**
- Must be actionable — a concrete instruction, not vague advice.
- Must be non-obvious — "write tests" is obvious. "Run smoke before spawning reviewers" is not.
- Max 2 entries per session.

### Step 4: Summary (5 sec)

Show user ONE line:

```
Quick Learning: {1 sentence summary, or "Clean session, no signals detected."}
```

Move on to session end protocol.

## Three-Tier Knowledge System

Patterns live in three tiers. Each tier is smaller, cheaper, and more permanent than the previous.

```
Tier 1: Transit Buffer              Tier 2: Skill Instructions        Tier 3: Quick Reference Card
reasoning-patterns.md               {skill}/SKILL.md                  quick-ref.md
━━━━━━━━━━━━━━━━━━━━━               ━━━━━━━━━━━━━━━━━━━━━             ━━━━━━━━━━━━━━━━━━━━━
Raw observations                    Promoted patterns (Seen ≥ 3)      Top 5-7 one-liners
Seen counter tracks recurrence      Permanent, always loaded by       Loaded by feature-execution
Max 20 entries, auto-pruned         skill at execution time           at session START
Written by quick-learning           Written at promotion time         Auto-generated at promotion
Read: last 30 lines (dedup only)    Read: by skill itself             Read: 7 lines max
```

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

### Pruning (when buffer exceeds 20 entries)

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
