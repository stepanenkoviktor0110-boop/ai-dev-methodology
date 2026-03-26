---
name: do-task
description: |
  Execute task from tasks/*.md with quality gates.

  Use when: "выполни задачу", "сделай таску", "do task", "execute task", "запусти задачу"
---

# Do Task

Execute a spec-driven task with validation and status tracking.

## Step 1: Read Task

1. Read task file (user provides path or task number)
   - If user didn't specify → ask: "Which task to execute?"
2. Verify task status is `planned` (if not → ask user before proceeding)
3. Update task frontmatter: `status: planned` → `status: in_progress`
4. Read every file listed in the task's "Context Files" section

## Step 2: Execute

1. Load each skill listed in the task (frontmatter `skills: [...]` and "Required Skills" section)
   - If a skill is not found → warn user, continue with remaining skills
   - If task has no skill (frontmatter `skills: []` or absent) → read the task, execute "What to do" and "Verification Steps" directly. For tasks with user instructions → show the instruction to user, wait for confirmation.
2. Follow loaded skill workflow
3. Git commit implementation (code + tests pass): `feat|fix|refactor: task {N} — {brief description}`
4. For each reviewer from the task's "Reviewers" section (if present):
   1. Spawn subagent via Task tool (subagent_type = reviewer name, e.g. `code-reviewer`)
   2. Pass: git diff of changes, path to task file, path to tech-spec, path to user-spec
   3. Reviewer loads its own skill automatically (via agent frontmatter `skills:`)
   4. Report is written to the path specified in the task's "Reviewers" section
   5. Read report. If findings exist → fix, re-run tests, git commit: `fix: address review round {N} for task {N}`, repeat (max 3 rounds)

## Step 3: Verify

1. Check each acceptance criterion from task file
2. If task has "Verification Steps → Smoke" → execute each smoke command, record results in decisions.md Verification section
3. If task has "Verification Steps → User" → ask user to verify, wait for confirmation
4. If any verification fails → fix → re-run tests → re-run reviewers (new round) → re-verify
   - After 3 failed rounds → stop, report failures to user, keep status `in_progress`
   - Tool unavailable → document, suggest manual check

## Step 4: Complete

1. Read template `~/.claude/shared/work-templates/decisions.md.template` and write a concise execution report to `work/{feature}/decisions.md`. Follow template format strictly — no extra sections. Use Planned/Actual/Deviation structure.
2. Update task frontmatter: `status: in_progress` → `status: done` (or `done_with_concerns` + fill `concerns:` field if something worries you — performance risk, edge case not covered, code smell that passed review, tech debt introduced). Use `done_with_concerns` when the task works but you have reservations. Retrospective will prioritize these.
3. Update tech-spec: `- [ ] Task N` → `- [x] Task N`
4. Git commit: `chore: complete task {N} — update status and decisions`
5. **Session boundary check** (skip if `work/{feature}/logs/session-plan.md` does not exist):
   Read session-plan.md. Find which session this task belongs to.
   - If this task is the **last task of current session** (all session's tasks are now `done`):
     **Quick Learning (subagent, background).** Spawn a subagent to run [quick-learning](../quick-learning/SKILL.md). Pass it: feature path, current session number, path to decisions.md. The subagent runs in the **background** while you proceed. When it finishes, show the user its one-line summary. Do NOT read the quick-learning SKILL.md yourself — the subagent loads it independently.
     Generate next-session prompt from `~/.claude/shared/work-templates/session-prompt.md.template`.
     Save to `work/{feature}/logs/next-session-prompt.md`.
     Present to user:
     ```
     Сессия {N} из {total} завершена.

     Рекомендую начать новую сессию Claude Code и вставить этот промт:

     ---
     {generated prompt content}
     ---
     ```
   - If tasks remain in current session: inform user which tasks are left in this session.

## Self-Verification

- [ ] Task status is `done`
- [ ] Tech-spec checkbox updated
- [ ] decisions.md entry written with reviews and verification results
- [ ] Git commit created with task reference
- [ ] Every acceptance criterion from task file is met
