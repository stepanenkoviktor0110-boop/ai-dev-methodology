# AI-First Development Methodology v1.4 — Claude Code

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

```bash
git clone https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology.git ~/.claude/skills
```

This places all skills and templates where Claude Code expects them (`~/.claude/skills/`).

### Step 2: Configure Claude Code

Add to `~/.claude/CLAUDE.md`:

```markdown
# Global Preferences

## Communication
- Общаться с пользователем по-русски. Код и команды — на английском.
```

### Step 3: Configure MCP (optional but recommended)

Add [Context7](https://github.com/upstash/context7) MCP server for up-to-date library documentation.

### Step 4: Verify installation

```bash
ls ~/.claude/skills/methodology/SKILL.md
```

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
/retrospective                 # Step 5: Extract lessons → update skills
/done                          # Step 6: Update project docs → archive feature
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
```

### Design Pipeline

```
/design-system-init            # Create design system: tokens.json + components
/design-generate               # Generate HTML/CSS pages from text descriptions
/design-review                 # Review UI code against design tokens
/design-retrospective          # Extract aesthetic lessons, build taste profile
```

### Other Commands

| Command | Purpose |
|---------|---------|
| `/init-project-knowledge` | Fill project documentation via interview |
| `/retrospective` | Extract lessons learned, update skills |
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

### Global Framework (`~/.claude/skills/`)

```
~/.claude/skills/                   # This repository
├── skills/                        # 25+ skills (methodology, execution, quality, design)
├── shared/
│   ├── work-templates/            # Templates for specs, tasks, sessions
│   └── design-references/         # Cross-project design experience
└── README.md
```

### Key Principles

- **Spec-Driven** — write specs before code. Hierarchy: User Spec → Tech Spec → Tasks → Code
- **Blocking Gates** — 6 mandatory HARD STOPs in the pipeline. No step proceeds without explicit user approval
- **Multi-level Validation** — automated validators at every stage (2 → 5 → 2 → 3)
- **Session Planning** — waves grouped by ~1200 LOC budget per session
- **Session Handoff** — structured report + generated prompt for next session at each stop
- **Just-In-Time Context** — agents read only what's needed for current task
- **Unified Knowledge System** — triad-based reasoning-patterns.md buffer, pruning, promotion of patterns into skills
- **Retrospective** — lessons embedded back into skills after each feature

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
| Planning | user-spec-planning, tech-spec-planning, task-decomposition, project-planning |
| Execution | code-writing, feature-execution, pre-deploy-qa, post-deploy-qa |
| Quality | code-reviewing, security-auditor, test-master, prompt-master |
| Design | design-system-init, design-generate, design-review, design-retrospective |
| Meta | methodology, retrospective, quick-learning, documentation-writing, skill-master |

For full details on any skill:
```
# Read the skill's SKILL.md
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
| Design pipeline | Full (4 skills) | Full (4 skills) |
| Agents directory | No (validators via Agent tool) | Yes (`agents/`) |

## Based on

Evolved fork of [molyanov-ai-dev](https://github.com/pavel-molyanov/molyanov-ai-dev) by Pavel Molyanov (MIT License).

## Changelog

### v1.4 — Unified Knowledge System + Design Pipeline (2026-03-27)

- **Unified knowledge system** — single reasoning-patterns.md buffer with triad-based dedup instead of scattered lessons-learned.md
- **Pruning trigger** — automatic cleanup when >25 entries in triad-index
- **Mechanical pre-filter** — 3+ content words in Goal = Near match candidate
- **Design categories** — design-taste, design-process, design-iteration
- **Design pipeline** — 4 skills for UI/UX: design-system-init, design-generate, design-review, design-retrospective
