---
name: retrospective
description: |
  Evaluate completed stage for process problems, extract lessons learned,
  and embed best practices into relevant skills as references.

  Use when: "ретроспектива", "retrospective", "что пошло не так",
  "извлеки уроки", "lessons learned", "обнови best practices"

  Runs after /new-tech-spec or /do-feature (/do-task) completion.
  Reads decisions.md + git log, writes to {skill}/references/lessons-learned.md.
---

# Retrospective

Evaluate the completed stage, extract lessons from problems encountered, embed them into methodology.

**Input:** `work/{feature}/decisions.md` + git log of the feature
**Output:** entries in `~/.claude/skills/{skill}/references/lessons-learned.md`
**Language:** Lessons in Russian (they are for the user), communication in Russian

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
| Tasks done with concerns | decisions.md: status "Done with concerns" + Concerns field; task frontmatter: `status: done_with_concerns` |

For each problem found, extract:
- **What happened** (1 sentence)
- **Root cause** (why it happened)
- **How it was resolved**
- **Which skill should know about this** (map to skill name)

Skill mapping:
- Problems during spec writing → `tech-spec-planning`
- Problems during task decomposition → `task-decomposition`
- Problems during coding → `code-writing`
- Problems during feature orchestration → `feature-execution`
- Problems during reviews → `code-reviewing`
- Problems during testing → `test-master`
- Problems during QA → `pre-deploy-qa` or `post-deploy-qa`
- Problems during deploy → `deploy-pipeline`

If no problems found (single validation pass, no fix rounds, no deviations) → tell user "Clean run, no lessons to extract." and stop.

**Checkpoint:** problems listed with root causes and target skills, or clean run confirmed.

## Phase 3: Write Lessons

For each target skill:

1. Check if `~/.claude/skills/{skill}/references/lessons-learned.md` exists.
   - If yes → read it, append new entry
   - If no → create with header

2. Add entry in this format:

```markdown
### {YYYY-MM-DD} {feature-name}: {problem title}

**Problem:** {what happened — 1 sentence}
**Cause:** {root cause — 1 sentence}
**Solution:** {how resolved — 1 sentence}
**Rule:** {what to do in the future — actionable instruction}
```

3. Check if the target skill's SKILL.md already links `lessons-learned.md`.
   - If no → add one line at the appropriate place in SKILL.md:
     `Before starting, check [lessons-learned.md](references/lessons-learned.md) for known pitfalls from past {skill-name} work (if file exists).`
   - If yes → skip, link already exists

**Checkpoint:** entries written, skills linked.

## Phase 4: Report

Show user a summary table:

| Skill | Problem | Rule added |
|-------|---------|------------|
| {skill} | {brief problem} | {brief rule} |

**Checkpoint:** summary table shown to user.

## Self-Verification

Before finishing, verify:
- [ ] Only real problems extracted (backed by evidence in decisions.md or git log)
- [ ] Each lesson has all 4 fields (Problem, Cause, Solution, Rule)
- [ ] Rules are actionable (not vague advice)
- [ ] Target skill's SKILL.md links lessons-learned.md
- [ ] No duplicate entries (same problem already recorded → skip)
