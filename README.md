# AI-First Development Methodology v2.0 — Claude Code

[Русская версия](README.ru.md)

Structured AI-First development methodology for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Every feature goes through a spec-driven pipeline with automated validators and quality gates at each stage.

## What It Does

A complete development framework where AI agents handle the full cycle: requirements → architecture → tasks → code → review → documentation. You guide the process, agents do the work.

**Problems it solves:**
- **Context loss between sessions** — distributed knowledge base persists across sessions
- **Quality without human review** — automated validators at every stage
- **Scope creep** — specs approved before coding starts
- **Outdated library knowledge** — Context7 MCP fetches current docs

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- [GitHub CLI](https://cli.github.com/) (`gh`) for project initialization
- Git

### Step 1: Clone the framework

The repository is laid out as an overlay for `~/.claude/`. Two install paths:

**Option A — merge into an existing config:**

```bash
git clone https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology.git /tmp/ai-dev-methodology
cp -r /tmp/ai-dev-methodology/{skills,agents,shared} ~/.claude/
cp /tmp/ai-dev-methodology/CLAUDE.md ~/.claude/CLAUDE.md   # review before overwriting
```

**Option B — fresh setup (empty `~/.claude/`):**

```bash
git clone https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology.git ~/.claude
```

### Step 2: Configure MCP (optional but recommended)

Add [Context7](https://github.com/upstash/context7) MCP server for up-to-date library documentation.

### Step 3: Verify installation

```bash
ls ~/.claude/skills/methodology/SKILL.md
```

Restart Claude Code and run `/methodology` — the skill should describe the full pipeline.

## Usage

### New Project (from scratch)

```
/init-project                  # Template + git + GitHub repo
/init-project-knowledge        # Interview → fill all project documentation
```

### New Feature (full pipeline)

```
/new-user-spec                 # Step 1: Interview → user-spec.md (requirements)
                               #   ⛔ user approves spec
/new-tech-spec                 # Step 2: Research → tech-spec.md (architecture)
                               #   ⛔ user approves spec
/decompose-tech-spec           # Step 3: Break into tasks → tasks/*.md
                               #   ⛔ GATE 1: user approves task decomposition
                               #   ⛔ GATE 2: user approves session plan (LOC budget)
                               #   ⛔ HARD STOP — no auto-transition to code
/do-feature                    # Step 4: Execute tasks by waves
                               #   ⛔ GATE 3: user confirms session scope + LOC before start
                               #   ⛔ GATE 4: session end → report + handoff prompt + STOP
/done                          # Step 5: Update project docs → archive feature
```

Each step has validators and **blocking gates** — no step proceeds without explicit user approval:

| Step | Command | Validators | Gates | Output |
|------|---------|-----------|-------|--------|
| Requirements | `/new-user-spec` | quality + adequacy (2) | user approves spec | `user-spec.md` |
| Architecture | `/new-tech-spec` | skeptic + completeness + security + test + template (5) | user approves spec | `tech-spec.md` |
| Tasks | `/decompose-tech-spec` | template + reality (2) | user approves tasks, then session plan | `tasks/*.md` + `session-plan.md` |
| Code | `/do-feature` | code + security + test reviewers (3) | session scope confirmed, STOP at session end | commits |
| Audit | (auto, last waves) | holistic code + security + test audit (3) | — | audit reports |
| QA | (auto, final wave) | pre-deploy + deploy + post-deploy | — | verified feature |

### Single Task (manual control)

```
/do-task                       # Execute one task with quality gates
```

### Ad-hoc Coding (no spec)

```
/write-code                    # TDD cycle: plan → tests → code → review
/sketch                        # Quick prototype: 3–5 questions → code → decide to develop or archive
```

### Session Management

```
/pause                         # Save session state → generate resume prompt
/quick-learning                # Extract lessons from current session → update reasoning patterns
```

### Design Pipeline

```
/design-system-init            # Create design system: tokens.json + components
/design-spec                   # Design specification through adaptive interview
/design-plan                   # Design plan with layout decisions
/design-task-decompose         # Decompose design plan into atomic task files
/design-generate               # Generate HTML/CSS pages from text descriptions
/photo-crop                    # Calculate object-position for photos in layouts
/design-review                 # Review UI code against design tokens
/design-retrospective          # Extract aesthetic lessons, build taste profile
```

### Other Commands

| Command | Purpose |
|---------|---------|
| `/infrastructure-setup` | Dev infrastructure: Docker, pre-commit hooks, testing setup |
| `/deploy-pipeline` | CI/CD pipeline and deployment configuration |
| `/documentation-writing` | Audit and update project knowledge base |
| `/pishi` | Edit Russian copy in Ilyahov infostyle |
| `/content-card` | Generate social media content cards (1080×1350) |
| `/safe-delete` | Pre-delete project audit (git sync, docs, VPS state) |
| `/done` | Finalize feature, update docs, archive |

## How It Works

### Project Structure

```
your-project/
├── .claude/
│   └── skills/
│       └── project-knowledge/      # Your project's knowledge base
│           ├── SKILL.md
│           └── references/
│               ├── project.md      # Purpose, audience, scope
│               ├── architecture.md # Tech stack, structure, data model
│               ├── patterns.md     # Code conventions, testing, business rules
│               └── deployment.md   # Platform, CI/CD, monitoring
├── work/                           # Feature work items
│   ├── my-feature/
│   │   ├── user-spec.md           # Requirements (human-readable)
│   │   ├── tech-spec.md           # Architecture (for agents)
│   │   ├── decisions.md           # Decisions made during implementation
│   │   ├── tasks/                 # Atomic task files
│   │   └── logs/                  # Session plans, checkpoints, review reports
│   └── completed/                 # Archived finished features
├── CLAUDE.md                      # Project instructions
└── README.md
```

### Global Framework (`~/.claude/`)

```
~/.claude/                         # This repository (overlay)
├── skills/                        # 45+ skills (methodology, execution, quality, design, utilities)
├── agents/                        # 20 specialized reviewer/validator subagents
├── shared/
│   ├── work-templates/            # Templates for specs, tasks, sessions
│   └── design-references/         # Cross-project design experience
├── CLAUDE.md
├── README.md
└── README.ru.md
```

### Key Principles

- **Spec-Driven** — write specs before code. Hierarchy: User Spec → Tech Spec → Tasks → Code
- **Blocking Gates** — 6 mandatory HARD STOPs in the pipeline. No step proceeds without explicit user approval
- **Multi-level Validation** — automated validators at every stage (2 → 5 → 2 → 3)
- **Session Planning** — waves grouped by ~1200 LOC budget per session
- **Session Handoff** — structured report + generated prompt for next session at each stop
- **Just-In-Time Context** — agents read only what's needed for current task
- **Unified Knowledge System** — triad-based reasoning-patterns.md buffer, pruning, promotion of patterns into skills
- **Continuous Learning** — quick-learning runs automatically at session end, skill-trainer embeds accumulated triads into skills

### Agent Architecture

Claude Code uses the built-in Agent tool with specialized subagent types for parallel work:

**How `/do-feature` orchestrates:**
- Spawns worker agents per task (parallel within wave)
- Spawns reviewer agents for code review (parallel)
- Max 3 review rounds per task
- Audit wave: 3 parallel auditors (code, security, test)
- Final wave: QA + deploy + post-deploy verification

**Subagent patterns:**
- `/decompose-tech-spec`: `task-creator` per task + `task-validator` + `reality-checker`
- `/new-tech-spec`: 5 validators in parallel
- `/new-user-spec`: 2 validators in parallel

### Skills & Agents

| Category | Skills |
|----------|--------|
| Planning | `user-spec-planning`, `tech-spec-planning`, `task-decomposition`, `project-planning` |
| Execution | `feature-execution`, `code-writing`, `do-task`, `pre-deploy-qa`, `post-deploy-qa`, `deploy-pipeline` |
| Quality | `code-reviewing`, `security-auditor`, `test-master` |
| Design | `design-system-init`, `design-spec`, `design-plan`, `design-plan-planning`, `design-task-decompose`, `design-generate`, `design-review`, `design-retrospective`, `photo-crop` |
| Content | `pishi` (Russian copy editing), `content-card`, `project-card`, `promoter` |
| Setup | `init-project`, `init-project-knowledge`, `infrastructure-setup` |
| Meta | `methodology`, `quick-learning`, `skill-trainer`, `documentation-writing`, `prompt-master` |
| Utilities | `sketch`, `pause`, `progress`, `done`, `safe-delete` |

For full details on any skill:
```
~/.claude/skills/{skill-name}/SKILL.md
```

## Differences from Codex Version

This repo and [ai-dev-methodology-codex](https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology-codex) share the same methodology but differ in platform integration:

| Aspect | Claude Code (this repo) | Codex |
|--------|------------------------|-------|
| Agent system | Claude Code Agent tool | `spawn_agent`/`wait_agent`/`close_agent` |
| Config location | `~/.claude/settings.json` | `~/.codex/config.toml` |
| Skills location | `~/.claude/skills/` | `~/.agents/` |
| Models | Claude (Opus/Sonnet/Haiku) | GPT-5.x tiers |
| Design pipeline | Full (9 skills) | Full (4 skills) |
| Agents directory | Yes (`agents/`) | Yes (`agents/`) |

## Based on

Evolved fork of [molyanov-ai-dev](https://github.com/pavel-molyanov/molyanov-ai-dev) by Pavel Molyanov (MIT License).

## Changelog

### v2.0 — Clean public release + localization (2026-04-17)

- **Repo cleanup** — personal workspace artifacts (`session-env/`, `paste-cache/`, `tasks/`, `.dashboard-events.jsonl`, `dashboard.json`) removed from the public repo and added to `.gitignore`. The public repo now contains only methodology content: skills, agents, shared templates, docs.
- **Russian localization** — full [README.ru.md](README.ru.md) in the repo root for Russian-speaking users.
- **Expanded skill set** — 45+ skills (up from 39+ in v1.6): added `content-card`, `project-card`, `promoter`, `progress`, `safe-delete`, `skill-trainer` categories; consolidated content/utility groups.
- **Compressed reasoning buffer** — `reasoning-patterns.md` reduced 282 KB → 197 KB (30%) through pruning and deduplication while preserving coverage.
- **Inline retrospective** — removed the separate `/retrospective` command; learning now runs inline via `quick-learning` at every session break, with auto-promotion to skill SKILL.md after 3+ sightings.

### v1.6 — Session tools + expanded design pipeline (2026-04-04)

- **sketch** — lightweight prototyping mode: 3–5 questions → code → decide to develop or archive. Closes the gap between "nothing" and "full pipeline"
- **pause** — session state management: saves checkpoint, task statuses, decisions.md, git status → generates resume prompt with full context
- **design pipeline expanded** — `design-spec`, `design-plan`, `design-plan-planning`, `design-task-decompose` added. Full 9-skill design system from specification to implementation
- **quick-learning** runs automatically at session end via `feature-execution` and `do-task` hooks; `/quick-learning` also available as manual command

### v1.5 — Skill Trainer: embedding triads into skills (2026-04-01)

- **skill-trainer** — new skill for batch embedding of accumulated triads into target skills. Reads all triads with `Adapted: —` from triad-index.md, analyzes each skill, auto-applies rules where no conflict exists, pauses for user decision on ambiguous cases. `force-embed pattern N` command forces embedding of a specific triad.
- **quick-learning** — responsibility refactor: skill no longer promotes patterns into skills at Seen ≥ 2. Collects triads only, notifies when unprocessed triads accumulate.
- **Adapted field** — new tracking field in triad-index.md and reasoning-patterns.md. Values: `—` (not yet embedded), `{skill-name}` (embedded), `n/a` (no matching skill found).

### v1.4 — Unified Knowledge System + Design Pipeline (2026-03-27)

- **Unified knowledge system** — single reasoning-patterns.md buffer with triad-based dedup instead of scattered lessons-learned.md
- **Pruning trigger** — automatic cleanup when >25 entries in triad-index
- **Mechanical pre-filter** — 3+ content words in Goal = Near match candidate
- **Design categories** — design-taste, design-process, design-iteration
- **Design pipeline** — 4 skills for UI/UX: design-system-init, design-generate, design-review, design-retrospective
