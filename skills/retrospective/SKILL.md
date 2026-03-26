---
name: retrospective
description: |
  Evaluate completed stage for process problems, extract lessons learned,
  and write them as triad entries into the unified knowledge buffer.

  Use when: "ретроспектива", "retrospective", "что пошло не так",
  "извлеки уроки", "lessons learned", "обнови best practices"

  Runs after /new-tech-spec or /do-feature (/do-task) completion.
  Reads decisions.md + git log, writes to unified reasoning-patterns.md via triad-based dedup.
---

# Retrospective

Evaluate the completed stage, extract lessons from problems encountered, embed them into the unified knowledge system.

**Input:** `work/{feature}/decisions.md` + git log of the feature
**Output:** triad entries in `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`
**Language:** Lessons in Russian (they are for the user), communication in Russian

**Knowledge system owner:** `quick-learning` skill defines the format, triad structure, similarity check rules, and promotion pipeline. Retrospective is a **writer** — it follows the same rules as quick-learning when writing entries.

## Phase 1: Collect Evidence

1. Ask user for feature name if not provided.
2. Read `work/{feature}/decisions.md`. If missing — use `git log --oneline` for feature commits.
3. Run `git log --oneline --all` scoped to the feature timeframe (use dates from decisions.md or tech-spec frontmatter).
4. Count fix rounds: look for commits like `fix: address review round`, `fix: validation`, repeated attempts.
5. Note the completed stage:
   - If tech-spec just approved → analyze spec creation process
   - If feature just completed → analyze implementation process

**Checkpoint:** decisions.md read, git history collected, stage identified.

## Phase 2: Identify Problems

Analyze evidence for these signals:

| Signal | Where to look |
|--------|--------------|
| Multiple validation rounds (>1) | git log: repeated `fix:` commits after validation |
| Review fix rounds (>1) | decisions.md: review findings, git log: `fix: address review` |
| Scope changes mid-work | decisions.md: deviations from plan |
| Blocked by missing info | decisions.md: clarifications needed, assumptions made |
| Wrong technical choice | decisions.md: approach changed, rollback commits |
| Repeated code pattern | git log: similar fixes across multiple tasks |
| Tasks done with concerns | decisions.md: status "Done with concerns" + Concerns field |

For each problem found, extract:
- **What happened** (1 sentence)
- **Root cause** (why it happened)
- **How it was resolved**
- **Target category** (for triad classification)

Category mapping:

| Problem area | Category |
|-------------|----------|
| Problems during spec writing | information-gathering |
| Problems during user spec | scope-management |
| Problems during task decomposition | problem-decomposition |
| Problems during coding | tool-selection |
| Problems during feature orchestration | sequencing / communication |
| Problems during reviews | tool-selection |
| Problems during testing | tool-selection |
| Problems during QA | sequencing |
| Problems during deploy | sequencing |
| Problems during design (taste/aesthetics) | design-taste |
| Problems during design (process/workflow) | design-process |
| Problems during design (iteration/feedback) | design-iteration |

If no problems found (single validation pass, no fix rounds, no deviations) → tell user "Clean run, no lessons to extract." and stop.

**Checkpoint:** problems listed with root causes and categories, or clean run confirmed.

## Phase 3: Write Lessons (Triad-Based)

For each problem, convert to a triad entry and write to the unified buffer. **Follow the same rules as quick-learning:**

### Step 3.1: Formulate Triad

For each lesson, formulate:
- **Trigger:** what situation or signal initiates the action
- **Action:** what to DO (the verb — concrete, actionable)
- **Goal:** what outcome this achieves

### Step 3.2: Similarity Check (mandatory)

Read `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`. For each existing row, compare triads:

| Match level | Criteria | What to do |
|-------------|----------|-----------|
| **Exact** | Same action AND same goal | Increment `Seen` counter in both triad-index and reasoning-patterns. Do NOT add new entry. |
| **Near** | Same goal, different action (or same action, different goal) | **Merge**: keep the more actionable wording, combine triggers, increment `Seen`. |
| **Distinct** | Different goal | Add as new entry. |

### Step 3.3: Write Entry

If distinct — append to the appropriate section of `$AGENTS_HOME/skills/quick-learning/references/reasoning-patterns.md`:

```markdown
### {YYYY-MM-DD} {feature-name}: {pattern title}

**Seen:** 1
**Triad:** {trigger} → {action} → {goal}
**Context:** {what situation triggered this insight — 1 sentence}
**Pattern:** {the transferable instruction — 1-2 sentences, imperative}
**Scope:** {universal | situational}
**Situation:** {only for situational — when this applies}
**Category:** {sequencing | information-gathering | problem-decomposition | scope-management | recovery | communication | tool-selection | design-taste | design-process | design-iteration}
```

### Step 3.4: Update Triad Index

Add/update the entry in `$AGENTS_HOME/skills/quick-learning/references/triad-index.md`.

### Step 3.5: Promote (if Seen reaches 3)

If any entry reaches Seen: 3 — follow the promotion pipeline from quick-learning SKILL.md:
1. Identify target skill by category
2. Add pattern as permanent instruction in target skill's SKILL.md
3. Remove entry from reasoning-patterns.md
4. Remove row from triad-index.md
5. Update quick-ref.md if universal

### Step 3.6: Pruning Check

After writing, count rows in `triad-index.md`. If more than 25 rows — run pruning as defined in quick-learning SKILL.md Step 3.5:
1. Remove `Seen: 1` entries older than 30 days from both `triad-index.md` and `reasoning-patterns.md`.
2. Merge similar entries.
3. Remove contradicted entries.

**Writing rules (same as quick-learning):**
- Must be actionable — a concrete instruction, not vague advice
- Must be non-obvious — "write tests" is obvious, "run smoke before spawning reviewers" is not
- Max 3 entries per retrospective (quick-learning allows max 2 — smaller scope)
- Every entry MUST have a Triad field
- **Mechanical pre-filter for similarity:** if Goal shares 3+ content words with existing Goal — treat as Near match candidate

**Checkpoint:** entries written, triad-index updated, pruning executed if needed, promotions executed if any.

## Phase 4: Report

Show user a summary table:

| # | Problem | Triad (short) | Action taken |
|---|---------|---------------|-------------|
| 1 | {brief problem} | {trigger} → {action} → {goal} | New / Merged (Seen: N) / Promoted → {skill} |

After the table, add a "Next step" block:
- What is the next logical step per `session-plan` or feature plan.
- Whether user confirmation is needed before the next session.

**Checkpoint:** summary table shown to user, next step stated.

## Self-Verification

Before finishing, verify:
- [ ] Only real problems extracted (backed by evidence in decisions.md or git log)
- [ ] Each lesson has Triad + Context + Pattern fields
- [ ] Rules are actionable (not vague advice)
- [ ] Similarity check performed against triad-index
- [ ] No duplicates — existing patterns got Seen++ instead
- [ ] Triad-index updated
- [ ] Promotions executed if any pattern reached Seen: 3
- [ ] Summary shown to user
