---
name: quick-learning
description: |
  Fast meta-analysis of session reasoning patterns. Runs automatically before
  every session break. Focuses NOT on specific decisions made, but on the LOGIC
  of decision-making — what reasoning approaches worked, what didn't, and what
  patterns can improve future work on similar projects.

  Writes learnings to $AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md
  so all methodology users benefit from accumulated insights.

  Automatic trigger: called by feature-execution and do-task before SESSION END PROTOCOL.
  Manual trigger: "quick learning", "быстрый анализ", "что улучшить в процессе"
---

# Quick Learning

Fast session analysis — extract reasoning patterns, not specific decisions.

**Time budget:** Under 60 seconds. This is NOT a full retrospective.
**Input:** `work/{feature}/decisions.md` + git log of current session
**Output:** entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`
**Language:** Entries in Russian (they serve the user community), communication in Russian.

Before starting, check [reasoning-patterns.md](references/reasoning-patterns.md) for existing patterns (if file exists). **Read only the last 30 lines** — enough to check for duplicates without wasting context on the full history.

## What This Is NOT

- NOT a retrospective (that's `/retrospective` — runs after full feature, maps problems to skills)
- NOT a code review (that's done per-task by reviewers)
- NOT about WHAT was decided — it's about HOW decisions were reached

## What to Extract

Focus on **meta-level reasoning patterns** — things that are transferable across projects:

| Category | Question to ask | Example pattern |
|----------|----------------|-----------------|
| **Sequencing** | Did the order of steps help or hurt? | "Starting with the riskiest integration first saved 2 rework cycles" |
| **Information gathering** | Was enough context collected before acting? | "Reading all task files before starting wave revealed shared dependencies" |
| **Problem decomposition** | How were complex problems broken down? | "Splitting DB migration from API layer let parallel work on wave 2" |
| **Scope management** | Were scope creep or underscoping caught early? | "Tech-spec was too vague on edge cases — reviewers caught it late" |
| **Recovery** | How were errors/blockers handled? | "When test OOMed, reducing parallelism to 1 worker fixed it immediately vs. 3 retry attempts" |
| **Communication** | Did session handoffs lose context? | "Session prompt missed the pending reviewer finding — next session re-investigated" |
| **Tool/approach selection** | Was the right tool/approach chosen first? | "Using vitest --reporter=verbose revealed the actual assertion failure vs. silent pass" |

## Procedure

### Step 1: Collect (15 sec)

1. Read `work/{feature}/decisions.md` — scan for this session's entries only.
2. Quick `git log --oneline -20` — see commit flow pattern (fix rounds, reworks, clean progression).
3. Note: How many fix rounds? Any rollbacks? Any scope changes mid-session?

### Step 2: Analyze (15 sec)

Ask yourself these questions about the session:

1. **What reasoning approach was tried first, and was it the right one?**
   - Did the agent/user go straight to the right solution, or were there detours?
   - What would have been a faster path?

2. **Where was time spent vs. where was value created?**
   - Was there unnecessary investigation? Over-validation? Under-validation?
   - What checks saved time? What checks were pure overhead?

3. **What pattern would help someone working on a similar project?**
   - Not "use TypeScript enums" (that's a code pattern) but "validate enum consistency across related tasks before starting wave" (that's a reasoning pattern).

If nothing non-obvious happened — **skip writing**. Clean sessions with no insights are fine. Don't force lessons.

### Step 3: Write (20 sec)

If insights found, append to `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`:

```markdown
### {YYYY-MM-DD} {feature-name} / session {N}: {pattern title}

**Context:** {what situation triggered this insight — 1 sentence}
**Pattern:** {the transferable reasoning approach — 1-2 sentences, imperative}
**Category:** {one of: sequencing | information-gathering | problem-decomposition | scope-management | recovery | communication | tool-selection}
```

Rules for writing:
- **Must be transferable** — useful for ANY project, not just the current one.
- **Must be actionable** — a concrete instruction, not vague advice.
- **Must be non-obvious** — "write tests" is obvious. "Run the smoke test BEFORE spawning reviewers to avoid wasting review rounds on broken code" is not.
- **No duplicates** — read existing patterns first. If the same insight exists, skip or refine the existing one.
- **Max 2 entries per session** — if you found more, keep only the most impactful.

### Step 4: Quick summary (10 sec)

Show user ONE line:

```
Quick Learning: {1 sentence summary of what was learned, or "Clean session, no new patterns."}
```

That's it. Move on to session end protocol.

## Pattern Lifecycle

Patterns in `reasoning-patterns.md` accumulate over time. When the file grows past 30 entries:
1. Review for duplicates and merge similar patterns.
2. Patterns that proved wrong (contradicted by later experience) — remove or mark as `**Revised:** {new understanding}`.
3. Patterns that appear 3+ times across different features — these are strong. Consider promoting them into the relevant skill's SKILL.md as a permanent instruction.

## Self-Verification

- [ ] Analysis took under 60 seconds
- [ ] Extracted patterns are about reasoning LOGIC, not specific technical decisions
- [ ] Each pattern is transferable to other projects
- [ ] No duplicates with existing patterns
- [ ] Max 2 entries written
- [ ] Summary shown to user before proceeding to session end
