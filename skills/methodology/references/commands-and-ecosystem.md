# Commands and Skills/Agents Ecosystem

Reference catalog extracted from the methodology SKILL.md to keep the main file focused on workflow narrative.

## Skills Ecosystem

**Planning:** `project-planning`, `user-spec-planning`, `tech-spec-planning`, `task-decomposition`, `stack-research` (explicit-call gate)
**Execution:** `code-writing` (TDD), `feature-execution` (team lead), `prompt-master`, `pre-deploy-qa`, `post-deploy-qa`
**Quality:** `code-reviewing` (11 dimensions), `security-auditor` (OWASP), `test-master`
**Problem solving:** `triz-synergy` (contradiction resolution), `triz-combinatorics` (minimal covering set of moves)
**Orchestration:** `parallel-tracks` (feature isolation by worktree + integration train)
**Meta:** `methodology`, `quick-learning`, `documentation-writing`, `skill-trainer`, `recalibrate-all`, `infrastructure-setup`, `deploy-pipeline`

## Agents

Isolated subprocesses with fresh context. Each receives input, does one job, returns structured output. Self-describing when invoked.

22 agents ship in `agents/`.

**Validators (8):** userspec-quality-validator, userspec-adequacy-validator, interview-completeness-checker, tech-spec-validator, skeptic, completeness-validator, task-validator, reality-checker
**Generators (1):** task-creator
**Reviewers (7):** code-reviewer, test-reviewer, security-auditor, prompt-reviewer, documentation-reviewer, deploy-reviewer, infrastructure-reviewer
**Research (3):** code-researcher, stack-researcher, stack-aggregator
**QA (2):** pre-deploy-qa, post-deploy-qa
**Meta (1):** skill-checker

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/new-user-spec` | Interview → user-spec.md |
| `/new-tech-spec` | Research → tech-spec.md |
| `/decompose-tech-spec` | Tech-spec → task files |
| `/do-task` | Execute single task with quality gates |
| `/do-feature` | Execute all tasks via agent teams |
| `/quick-learning` | Fast reasoning analysis — auto at session breaks, manual anytime |
| `/stack-research` | Research stack elements against official docs (gate before stack decisions) |
| `/done` | Update PK, archive feature |
| `/write-code` | Ad-hoc coding with TDD and reviews |
| `/init-project` | Initialize new project with template, git, GitHub |
| `/init-project-knowledge` | Fill all project documentation via project-planning skill |
| `/triz-synergy` | Resolve a contradiction — invoke when fixing A breaks B, or a defect class returns |
| `/parallel-tracks` | Isolate a feature into its own track, or run the integration train |
| `/sketch` | Lightweight prototype: 3–5 questions → code, no validators |
| `/pause` | Save session state → generate resume prompt |
| `/safe-delete` | Pre-delete audit: git sync, docs, VPS state, local processes |
| `/recalibrate-all` | Audit and recalibrate the skill set itself |

## Workflow Quick Start

**New project:**
`/init-project` → `/init-project-knowledge` (interview + fill all docs) → start features

**New feature:**
`/new-user-spec` → `/new-tech-spec` → `/decompose-tech-spec` → `/do-feature` or `/do-task` → `/done`
Learning runs inline via `quick-learning` at each session break — there is no separate retrospective step.

**Ad-hoc coding (no spec):**
`/write-code`

To understand how a specific skill works internally, read its SKILL.md directly.
