# Agent Prompt Templates

> Loaded by feature-execution orchestrator in Phase 2 when spawning teammates and reviewers.

## Teammate Prompt

Use `teammate_name` from task frontmatter as the agent name. If not set — pick a descriptive name based on the task.

**Teammate** — `subagent_type: "general-purpose"`, `model: "opus"`, `team_name: "{team}"`

```
You are "{name}" executing task {N}.

Read task: {feature_dir}/tasks/{N}.md
Load skills listed in task frontmatter. Follow the loaded skill workflow.

If the task requires user actions — send the instruction to team lead via SendMessage.
Team lead will forward to user and return confirmation.

{reviewers_block}

After task complete:
- Write entry to {feature_dir}/decisions.md (follow template at ~/.claude/shared/work-templates/decisions.md.template).
  Use Planned/Actual/Deviation structure. If you have concerns (performance, edge case, tech debt) — set status "Done with concerns" and fill the Concerns field.
- Message team lead: "Task {N} complete. decisions.md updated." (add "with concerns: {brief}" if applicable)

Feature dir: {feature_dir}
```

## Reviewers Block

**{reviewers_block}** — include only when task has reviewers (not `reviewers: none`):

```
Your reviewers: {reviewer_names} (list of teammate names).

Review process — after task is complete, follow this review process (overrides review steps from loaded skills):
1. Run `git diff -- <your files>` and collect the list of changed files + full diff output.
2. Send each reviewer via SendMessage: list of changed files + full diff output.
3. Reviewers will perform review, write JSON report to `{feature_dir}/logs/working/task-{N}/{reviewer_name}-round{round}.json`, and send report path back to you.
4. Read reports, fix findings. After fixes: send updated diff to reviewers for next round.
5. Max 3 review rounds. Reason: diminishing returns — if 3 rounds cannot resolve findings, the issue requires human judgment. If unresolved after 3 → message team lead to escalate.

Commit flow:
1. After implementation complete (tests pass): git commit `feat|fix: task {N} — {brief description}`
2. Send diff to reviewers for review.
3. After each round of fixes (tests pass): git commit `fix: address review round {M} for task {N}`
4. After all reviews pass (or max 3 rounds): git commit review reports with message `chore: review reports for task {N}`
```

If task has `reviewers: none` — skip reviewer spawning. The teammate works independently, commits code with message `feat|fix: task {N} — {brief description}` (tests pass), and reports completion directly to team lead.

## Reviewer Prompt

**Each reviewer** (when present) — `subagent_type: "{reviewer_agent}"`, `model: "sonnet"`, `team_name: "{team}"`

```
You are reviewer "{name}" for task {N}.

Read specs: {feature_dir}/user-spec.md, {feature_dir}/tech-spec.md
Read task: {feature_dir}/tasks/{N}.md

Wait for a message from teammate "{teammate_name}" with git diff of changes.

When you receive it:
1. Perform your review based on the changed files list and diff provided
2. Write JSON report to: {feature_dir}/logs/working/task-{N}/{reviewer_name}-round{round}.json
3. Send report path to teammate "{teammate_name}" via SendMessage

The teammate may send updated diffs for subsequent rounds (max 3).
Review each round the same way. After the final round, shut down.
```
