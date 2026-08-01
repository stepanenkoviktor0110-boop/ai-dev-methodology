---
disable-model-invocation: true
name: methodology
description: |
  AI-First development methodology: spec-driven pipeline, project structure,
  skills/agents ecosystem, quality gates.

  Use when: "изучи методологию", "изучи глобальную папку", "как работает методология",
  "what is the pipeline", "покажи пайплайн", "расскажи о процессе разработки",
  "how does the methodology work", "explain the workflow"

  For infrastructure tasks, use infrastructure-setup or deploy-pipeline skills.
---

# AI-First Development Methodology

## What Is This

A structured development approach for AI agents. Every feature goes through a pipeline: idea → spec → architecture → tasks → implementation → documentation update. Each stage has automated validators and quality gates. QA and deploy are regular tasks in the tech-spec, not separate pipeline steps.

Core problems it solves:
- **Context loss between sessions** — distributed knowledge base persists across sessions
- **Quality without human review** — automated validators at every stage
- **Scope creep** — specs approved before coding starts
- **Outdated agent knowledge** — Context7 MCP fetches current library docs

---

## Development Pipeline

The full path from idea to production. Each step has a command, a skill behind it, and validators.

### Step 1: User Spec — `/new-user-spec`

**What:** Structured interview to capture requirements in human-readable form (Russian).

**Process:**
- Agent reads Project Knowledge files to understand the project
- Scans codebase for relevant code, patterns, integration points
- Runs 3 interview cycles with the user (general → code-informed → edge cases)
- `interview-completeness-checker` agent verifies coverage
- Creates `user-spec.md` from interview data → git commit draft
- 2 validators run in parallel (loop while each round reduces open findings):
  - `userspec-quality-validator` — document structure, acceptance criteria testability
  - `userspec-adequacy-validator` — solution feasibility, over/underengineering
- Git commit after each validation round
- User approves → git commit approval (status: approved)

**Output:** `work/{feature}/user-spec.md` (status: approved)

**Skill:** `user-spec-planning`

### Step 2: Tech Spec — `/new-tech-spec`

**What:** Technical architecture, decisions, testing strategy, implementation plan.

**Process:**
- Reads approved user-spec
- Researches codebase, checks dependencies, uses Context7 for external libraries
- Asks technical clarification questions
- Copies tech-spec template, edits sections in place → `tech-spec.md` with architecture (including Shared Resources for heavy objects like ML models, DB pools), decisions, testing strategy, brief Implementation Tasks (scope only — AC and TDD are added during task-decomposition) → git commit draft
- Implementation Tasks include Verify-smoke (executable checks: curl, python -c, docker) and Verify-user (manual UI/UX checks) fields where applicable
- Last two waves are always Audit Wave (3 parallel auditors: code, security, test) and Final Wave (QA + deploy)
- 5 validators run in parallel (loop while each round reduces open findings):
  - `skeptic` — detects non-existent files, functions, APIs (mirages)
  - `completeness-validator` — bidirectional requirements traceability, over/underengineering, solution depth
  - `security-auditor` — OWASP Top 10 review
  - `test-reviewer` — test plan adequacy
  - `tech-spec-validator` — template compliance, task quality, wave conflict detection
- Git commit after each validation round
- User approves → git commit approval (status: approved)

**Output:** `work/{feature}/tech-spec.md` (status: approved)

**Skill:** `tech-spec-planning`

**After completion:** run `/quick-learning` to extract lessons from the spec creation process.

### Step 3: Task Decomposition — `/decompose-tech-spec`

**What:** Break tech-spec into atomic task files.

**Process:**
- For each Implementation Task in tech-spec, `task-creator` agent copies task template and fills it (parallel)
- Each task file expands brief tech-spec scope into: acceptance criteria, TDD anchor (from Testing Strategy), context files, skills, reviewers, wave, dependencies → git commit draft
- 2 validators run in parallel (loop while each round reduces open findings):
  - `task-validator` — template compliance, content quality
  - `reality-checker` — validates against actual codebase (file existence, feasibility)
- Cross-task integration check: both validators re-run on all tasks together — catches shared resource conflicts, duplicate heavy resource init, hidden dependencies (max 2 extra iterations)
- Git commit after each validation round
- User approves → git commit approval
- **Session planning:** groups waves into sessions by LOC budget (~1200 lines per session). Generates `session-plan.md` with session boundaries, tasks per session, and context files. Audit Wave + Final Wave are always the last session.

**Output:** `work/{feature}/tasks/*.md` (validated) + `work/{feature}/logs/session-plan.md`

**Skill:** `task-decomposition`

### Step 4: Implementation

**Choose `/do-task` when:** single task, manual control, debugging, iterating on one piece.
**Choose `/do-feature` when:** multiple tasks ready, standard feature work, want parallel execution.

Two modes:

#### Mode A: Single Task — `/do-task`

One task per session. Suited for manual, controlled execution.

**Process:**
- Reads task file and all its Context Files
- Loads skills specified in task (e.g. `code-writing`, `pre-deploy-qa`, `infrastructure-setup`)
- Follows loaded skill workflow (TDD for code tasks, verification for QA tasks, etc.)
- Git commit implementation (code + tests pass)
- Runs reviewers specified in task (if any), up to 3 review iterations
- Git commit after each round of review fixes (tests pass)
- Writes entry to `decisions.md`, updates task status → done
- Git commit status + decisions

**Skill:** Loaded from task file (typically `code-writing` for code tasks)

#### Mode B: Full Feature — `/do-feature`

All tasks via agent teams. Team lead orchestrates waves of parallel work.

**Process:**
- Team lead reads tech-spec and all task files, builds execution plan
- Checks `checkpoint.yml` — if resuming after context compaction or new session, skips completed waves (uses decisions.md as source of truth for what actually completed)
- Reads `session-plan.md` for session boundaries — stops at session boundary, generates prompt for next session
- Creates team via TeamCreate
- Executes tasks wave by wave:
  - Spawns one agent per task (parallel within wave)
  - Each teammate: follows loaded skill workflow, runs smoke verification if task has Verify-smoke (before reviews), commits code (tests pass), sends diff to reviewers, fixes findings with commits per round, while each round leaves strictly fewer open findings, commits review reports
  - Each teammate writes `decisions.md` entry
  - Lead commits status updates (task frontmatter + decisions.md) after wave completes, updates `checkpoint.yml`
- **Audit Wave** (always present): 3 auditors run in parallel (code-reviewer, security-auditor, test-reviewer) — review all feature code holistically. Issues found → lead spawns fixer agent, auditors become reviewers, same converge-or-escalate rule
- **Ad-hoc agents**: when lead needs work outside planned tasks (fixing audit findings, escalations), assigns matching skill + reviewers based on work type
- **Final Wave**: QA (always), deploy + post-deploy (if applicable)
- **Escalation**: after 3 failed fix rounds — stop, report to user, write decisions.md entry, wait for decision
- User reviews results, team shuts down, `checkpoint.yml` deleted

Tasks can be code, user-action, deploy, config, or verification. Task nature is determined by its skill + description, not a separate type field.

**Skill:** `feature-execution`

**After completion:** run `/quick-learning` to extract lessons from the implementation process.

**Note:** At every session break within `/do-feature` and `/do-task`, the `quick-learning` skill runs automatically as a background subagent. It extracts meta-level reasoning patterns — not specific technical decisions, but transferable insights about HOW problems were approached. These accumulate in `~/.claude/skills/quick-learning/references/reasoning-patterns.md` and benefit all methodology users.

### Step 5: Lessons — `/quick-learning`

**What:** Extract lessons learned from problems encountered during tech-spec creation and implementation. Runs automatically as a background subagent at session breaks; invoke it by hand to capture a session that ended outside one.

**Process:**
- Reads `decisions.md` and git log of the feature
- Identifies process problems: multiple validation rounds, review fix cycles, scope changes, wrong technical choices
- Writes lessons as triad entries in `~/.claude/skills/quick-learning/references/reasoning-patterns.md`
- Uses triad-based dedup via `triad-index.md`
- Each entry: Triad (trigger → action → goal) + Context + Pattern + Scope + Category

**Output:** entries in `~/.claude/skills/quick-learning/references/reasoning-patterns.md`

**Skill:** `quick-learning`. Once 25 unadapted triads accumulate, it prompts for `/skill-trainer`, which embeds them into the skills themselves.

### Step 6: Done — `/done`

**What:** Finalize feature, update project knowledge, archive.

**Process:**
- Reads user-spec, tech-spec, decisions.md
- Updates affected Project Knowledge files (architecture.md, patterns.md, deployment.md, etc.)
- Moves `work/{feature}/` → `work/completed/{feature}/`
- Commits changes

**Skill:** Loads `documentation-writing` skill for PK update rules

---

## Project Structure

### Project Knowledge — the Knowledge Base

All project documentation lives in `.claude/skills/project-knowledge/references/`. This is the single source of truth for everything about the project.

**4 core + optional files:**

| File | Content |
|------|---------|
| `project.md` | Purpose, audience, core features, scope |
| `architecture.md` | Tech stack, structure, dependencies, data model |
| `patterns.md` | Code conventions, git workflow, testing, business rules |
| `deployment.md` | Platform, env vars, CI/CD, monitoring |
| `ux-guidelines.md` | UI language, tone, domain glossary (optional) |

Features and roadmap live in the project backlog (external to PK).

**CLAUDE.md is minimal.** It contains only the project name, a reference to project-knowledge skill, methodology overview, and default branch. All real information lives in Project Knowledge files.

**`project-planning` skill** creates PK from scratch in new projects via interview (`/init-project-knowledge`).

**`documentation-writing` skill** manages existing PK: audits, updates, checks consistency. `/done` command uses it to update PK after feature completion.

### Work Items

```
work/{feature}/
├── user-spec.md          # Requirements (Russian, for human)
├── tech-spec.md          # Architecture (English, for agent)
├── decisions.md          # Decisions made during implementation
├── tasks/
│   ├── 1.md              # Atomic task files
│   ├── 2.md
│   └── 3.md
└── logs/                 # Working logs (interview, research, reviews)
```

Completed features are archived to `work/completed/{feature}/`.

### Global Structure `~/.claude/`

```
~/.claude/
├── skills/               # Skills (methodology, workflow, quality)
├── agents/               # Agents (validators, reviewers, creators)
├── commands/             # Slash commands
├── shared/               # Templates, scripts, interview plans
├── hooks/                # Automation hooks
└── CLAUDE.md             # Global instructions
```

---

## Key Principles

- **Spec before code.** User Spec → Tech Spec → Tasks → Code.
- **Research stack before deciding.** Before stack decisions in `project-planning` (shallow, comparing candidates) and `tech-spec-planning` (deep, chosen element), a BLOCKING gate requires `/stack-research` for critical elements — external APIs, services, non-whitelisted libraries. No memory-based decisions on critical stack.
- **Validate at every stage.** User spec (2), tech spec (5), tasks (2), code (reviewers selected by what the diff contains, plus smoke), audit wave (3 holistic auditors), QA (pre-deploy + post-deploy). Every fix loop runs while it converges and escalates the moment it stops — no fixed round count.
- **Commit after each result.** Planning: draft → validation rounds → approval. Execution: code (tests pass) → review fixes → status. Not after every action.
- **PK = single source of truth.** All project docs in `.claude/skills/project-knowledge/references/`. CLAUDE.md is minimal. `/done` updates PK. `documentation-writing` audits quality.
- **Just-in-time context.** Read only what's needed. Task files list Context Files explicitly. Context7 MCP for library docs.
- **Session planning.** Waves grouped into sessions by ~1200 LOC budget. At boundary → stop, generate next-session prompt. Audit + Final wave = last session.
- **Checkpoint recovery.** `checkpoint.yml` persists after each wave. On context compaction → resume from next pending wave via checkpoint + decisions.md.
- **Parallel features without breaking prod.** When 2-3 features run in parallel across
  independent sessions, the `parallel-tracks` skill adds a cross-feature layer on top of the
  per-feature pipeline: each feature is isolated on its own branch+worktree (one session =
  one track), sessions coordinate only through shared repo files (`work/_train/`, not
  memory), and tracks converge into `dev` **one at a time** through an integration train
  (rebase → migration-head merge → PR/CI → merge → per-service deploy). feature-execution
  auto-invokes it at feature start (isolation) and end (integration). This is what stops the
  "race of commits" and the live-service breakage when parallel work is merged.

---

## Reference catalog

For the full Skills Ecosystem map, Agents catalog (validators/reviewers/research/QA/meta), Commands Reference table, and Workflow Quick Start cheat-sheet, read [commands-and-ecosystem.md](references/commands-and-ecosystem.md).

To understand how a specific skill works internally, read its SKILL.md directly.
