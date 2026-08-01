# Agent Prompt Templates

> Loaded by feature-execution orchestrator in Phase 2 when spawning teammates and reviewers.

---

## Orchestrator Pre-Read Protocol (A+B optimization)

**Before spawning each teammate**, the orchestrator reads files and inlines content directly into the prompt.
Agents must NOT be told to "read task file" or "load skill" — that doubles token cost.

### A — What to pre-read and inline

For each task N, read and inline these into the teammate prompt:

| What to read | What to inline |
|---|---|
| `tasks/{N}.md` | Description, What to do, TDD Anchor, Files section, Acceptance Criteria, Verification Steps → Smoke |
| Each **existing** source file from task's "Files" section | Full file if <150 lines; otherwise relevant function/class excerpts the agent will modify or must not break |
| `decisions.md` | Only entries for task numbers listed in `depends_on` — 2–3 sentences each max |
| Any single file explicitly called out in task's "CRITICAL: read X" context | Inline it fully |

**Do NOT inline:** tech-spec.md, user-spec.md, project-knowledge .md files, context task files (e.g. "see task 11") — extract only the specific fact needed and state it directly in the prompt.

### B — Replace skill loading with inline rules

Do NOT write "Load skill: code-writing/SKILL.md" in agent prompts.
Instead, paste the "Coding rules" block below directly into the prompt.

---

## Teammate Prompt (A+B optimized)

Use `teammate_name` from task frontmatter as the agent name. If not set — pick a descriptive name.

**Teammate** — `subagent_type: "general-purpose"`

```
You are "{name}" implementing task {N}.

## Task
{inline: Description section from task file — 3–6 sentences}

## What to do
{inline: full "What to do" section from task file}

## TDD Anchor
{inline: TDD Anchor section from task file}

## Files
{inline: Files/Details section listing what to create/modify}

## Existing code (read before writing)
{inline: content of each existing file that must be modified or not broken — full file if <150 LOC, else the relevant functions}

## Key decisions from prior tasks
{inline: 2–3 sentence summary of each depends_on task entry from decisions.md — only facts this task needs}

## Acceptance Criteria
{inline: Acceptance Criteria checklist from task file}

## Coding rules
- Write tests first (TDD Anchor above), watch them fail, then implement to make them pass.
- No comments unless WHY is non-obvious. No abstractions beyond what the task requires.
- Validate only at system boundaries (user input, external APIs). Trust internal guarantees.
- Use env vars for secrets. Never log secrets.
- All HTTP calls must have timeouts.
- Run `{project linter/formatter}` after implementation.

## Smoke verification
{inline: Verification Steps → Smoke commands from task file}
Run these after tests pass. Fix before committing if they fail.

## Post-generation guard
Before committing, grep your changed files for:
- secrets inside logging calls → remove
- `fetch()`/`requests.*()` without timeout → add 30s default
Report what you checked.

{reviewers_block}

## Commit flow
1. After implementation complete (tests pass): git commit `feat|fix: task {N} — {brief description}`
2. After each round of fixes (tests pass): git commit `fix: address review round {M} for task {N}`
3. After all reviews pass: git commit review reports `chore: review reports for task {N}`

## After task complete
- Write entry to {feature_dir}/decisions.md (Planned/Actual/Deviation structure, template at ~/.claude/shared/work-templates/decisions.md.template).
- Report: "Task {N} complete. decisions.md updated." (add "with concerns: {brief}" if applicable)

Feature dir: {feature_dir}
```

---

## Reviewers Block

**{reviewers_block}** — include only when task has reviewers (not `reviewers: none`):

```
## Review process
Your reviewers: {reviewer_names}.

After task is complete:
1. Run `git diff -- <your files>` and collect changed files + full diff.
2. Write self-review JSON to `{feature_dir}/logs/working/task-{N}/self-review-round{round}.json`:
   {"round": 1, "reviewer": "self", "findings": [...], "status": "approved"|"needs_fixes"}
   For each finding: {"severity": "high|medium|low|info", "file": "...", "line": N, "issue": "...", "fix": "..."}
3. Fix high/medium findings. After fixes: re-run tests, commit fix, increment round.
4. Repeat while each round leaves strictly fewer open findings than the one before. The first round that does not reduce them → message team lead to escalate.
```

If task has `reviewers: none` — omit the review block. Teammate commits code and reports directly.

---

## Reviewer Prompt

**Each reviewer** (when spawned as separate agent) — `subagent_type: "{reviewer_agent}"`

```
You are reviewer "{name}" for task {N}.

Specs summary:
{inline: 3–5 sentence summary of what task {N} builds, from task Description}

Wait for a message from teammate "{teammate_name}" with git diff of changes.

When you receive it:
1. Perform your review based on the changed files list and diff provided.
2. Write JSON report to: {feature_dir}/logs/working/task-{N}/{reviewer_name}-round{round}.json
3. Send report path to teammate "{teammate_name}" via SendMessage.

The teammate may send updated diffs for subsequent rounds.
Review each round the same way. After the final round, shut down.
```

---

## Orchestrator Checklist Before Spawning

- [ ] Task file read; Description/What-to-do/TDD Anchor/Files/AC inlined
- [ ] Existing source files read and inlined (files that exist already)
- [ ] decisions.md entries for depends_on tasks summarized and inlined
- [ ] Skill loading removed; inline coding rules present
- [ ] Smoke commands inlined
- [ ] Reviewers block present (or omitted if reviewers: none)
