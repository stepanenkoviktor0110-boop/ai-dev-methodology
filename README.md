# AI-First Development Methodology v2.0

A structured methodology for building software with AI coding agents (Claude Code). Instead of ad-hoc prompting, every feature follows a disciplined pipeline: requirements interview, technical specification, task decomposition, automated implementation with reviews, and retrospective learning.

**Based on:** Evolved fork of [molyanov-ai-dev](https://github.com/pavel-molyanov/molyanov-ai-dev) by Pavel Molyanov.

**Русская версия:** [README.ru.md](./README.ru.md)

## Core Principles

1. **Spec before code.** No implementation starts until requirements and architecture are explicitly approved. This prevents the #1 failure mode of AI coding: building the wrong thing fast.

2. **Validation at every stage.** Automated validators check each artifact (user spec, tech spec, tasks) before the pipeline advances. Problems caught in specs cost 10x less than problems caught in code.

3. **Session-aware execution.** Work is split into sessions (~1200 LOC each) that fit within a single context window. Each session ends with a handoff prompt so a fresh context can continue without lost knowledge.

4. **Self-improving process.** The methodology learns from every session. Quick-learning captures reasoning patterns at session breaks; retrospective embeds specific lessons into skills after feature completion. All improvements flow back into the shared methodology.

5. **Quality through structure, not hope.** Every task gets code review, security audit, and test review automatically. Max 3 fix rounds per review cycle — if it can't be fixed, escalate.

## Pipeline

Every feature flows through 5 stages with hard stops between them. No stage auto-advances — the user explicitly starts each one.

```
/new-user-spec  -->  /new-tech-spec  -->  /decompose-tech-spec  -->  /do-feature  -->  /done
   Interview          Architecture          Tasks + Sessions          Build + Review       Archive
```

Retrospective learning runs **inline** at every session break via `quick-learning` (background subagent) — no separate manual stage needed.

### Stage 1: User Spec — `/new-user-spec`

Adaptive interview with the user to capture requirements. The agent scans the codebase first, then asks targeted questions (not a generic form). Output: `user-spec.md` with acceptance criteria, edge cases, constraints.

**Validators:** quality (document completeness) + adequacy (solution feasibility)

### Stage 2: Tech Spec — `/new-tech-spec`

Research the codebase, design architecture, document decisions. Reads actual source files — no hallucinated APIs. Output: `tech-spec.md` with data model, API contracts, testing strategy, implementation tasks.

**Validators:** template compliance, skeptic (detects references to non-existent code), completeness (bidirectional requirements traceability), security review, test strategy review

### Stage 3: Task Decomposition — `/decompose-tech-spec`

Split the tech spec into atomic tasks, group into waves (parallel batches), assign to sessions. Each task has: what to do, files to modify, acceptance criteria, required skills, reviewers.

**Output:** `tasks/*.md` + `session-plan.md`
**Validators:** template compliance, reality check (file/function existence)

### Stage 4: Implementation — `/do-feature` or `/do-task`

Execute tasks via agent teams. For each task: implement with TDD, run reviewers (code + security + tests), fix findings (max 3 rounds), commit. After all code waves: audit wave (holistic review of entire feature), then QA wave.

**At every session break:** `quick-learning` runs as a background subagent — extracts transferable reasoning patterns and writes them to the shared knowledge base.

**Reviewers per task:** code-reviewer, security-auditor, test-reviewer
**Audit wave:** same 3 reviewers on the full feature diff

### Stage 5: Done — `/done`

Detect documentation drift from git changes, update project knowledge, and archive the feature directory to `work/completed/`. Session-break retrospective has already run inline via `quick-learning` during Stage 4.

## Self-Improvement Loop

The methodology has two learning mechanisms that work at different scales:

| | Quick Learning | Auto-promotion |
|---|---|---|
| **When** | Every session break (automatic) | When a pattern is seen 3+ times across features |
| **Focus** | HOW decisions were made (reasoning patterns) | Mature patterns that survived multiple features |
| **Output** | `quick-learning/references/reasoning-patterns.md` (transit buffer) | `skills/{skill}/SKILL.md` (permanent instruction) |
| **Scope** | Cross-project transferable insights | Skill-specific permanent rules |
| **Cost** | Background subagent, ~0 main context tokens | Zero — promotion happens inside quick-learning |

Both feed back into the methodology repo, so all users benefit from accumulated experience.

## Structure

```
skills/               # 45+ skills — methodology knowledge (WHAT to do)
  quick-learning/     #   Session reasoning analysis
  feature-execution/  #   Team lead orchestration
  code-writing/       #   TDD implementation workflow
  done/               #   Session finalization and archive
  design-*/           #   Design pipeline: spec, plan, generate, retrospective
  pishi/              #   Russian copy editing (Ilyahov infostyle)
  content-card/       #   Social media content cards
  sketch/             #   Rapid prototyping mode
  ...
agents/               # 20 agents — isolated subprocesses (HOW to deliver)
  code-reviewer.md    #   11-dimension code review
  skeptic.md          #   Detects hallucinated code references
  ...
shared/
  work-templates/     # Templates for specs, tasks, sessions
  templates/          # New project scaffolding
  interview-templates/  # Interview plans (YAML)
CLAUDE.md             # Global agent preferences
```

## Validation Matrix

| Stage | Validators | What they catch |
|-------|-----------|----------------|
| User Spec | quality + adequacy | Incomplete requirements, infeasible solutions |
| Tech Spec | skeptic + completeness + security + test + template | Hallucinated code, missing requirements, OWASP issues |
| Tasks | template + reality | Non-existent files/functions, missing acceptance criteria |
| Code | code-reviewer + security-auditor + test-reviewer | Code quality, vulnerabilities, test coverage |
| Audit | same 3 reviewers (holistic) | Cross-task inconsistencies, integration issues |
| QA | pre-deploy + post-deploy | Acceptance criteria verification |

## What's New in v2.0

### Clean public release

- **Repo cleanup** — personal workspace artifacts (session-env, paste-cache, tasks, dashboard telemetry) removed from the public repo and added to `.gitignore`. The public repo now contains only methodology content: skills, agents, shared templates.
- **Russian localization** — full [README.ru.md](./README.ru.md) for Russian-speaking users.

### Expanded skill set

- **45+ skills** (up from 25+ in v1.4), including `pishi` (Russian copy editing), `photo-crop`, `content-card`, `design-*` pipeline (spec → plan → generate → task-decompose → retrospective), `sketch` (rapid prototyping), `safe-delete`, `skill-trainer`, `project-card`, `promoter`, `pause`/`progress`.
- **Design pipeline** promoted to first-class: own interview, planning, task decomposition, review, and retrospective skills.

### Mature knowledge loop

- **Compressed reasoning buffer** — `reasoning-patterns.md` reduced 282 KB → 197 KB (30%) through pruning and deduplication, while preserving coverage.
- **Triad-based knowledge** system unified across quick-learning (session breaks) and retrospective (post-feature), writing to a single buffer with `trigger → action → goal` structure.
- **Auto-promotion** from buffer to skill SKILL.md when a pattern is seen 3+ times across features.

<details>
<summary>What was new in v1.4</summary>

### Pruning & quality improvements

- **Auto-pruning** — added Step 3.5 (quick-learning) and Step 3.6 (retrospective) pruning checks that trigger when the knowledge buffer exceeds 25 entries, preventing unbounded growth.
- **Mechanical pre-filter** — similarity matching now uses a 3+ content word overlap heuristic before semantic comparison, reducing false positives.
- **Design categories** — retrospective now recognizes `design-taste`, `design-process`, and `design-iteration` categories alongside existing engineering ones.
- **Cross-reference by title** — triad-index references entries by matching title instead of fragile row numbers.

</details>

<details>
<summary>What was new in v1.3</summary>

### Unified knowledge system

The biggest architectural change since v1.2: all learning outputs now flow through a single pipeline.

- **One buffer** — merged 4 separate `lessons-learned.md` files (from feature-execution, code-writing, task-decomposition, user-spec-planning) into a single `reasoning-patterns.md` using the triad format.
- **One format** — both quick-learning (session reasoning) and retrospective (feature post-mortem) write to the same buffer using the same `trigger → action → goal` triad structure.
- **RULE #1: Single Source of Truth** — `~/.claude/skills/` is the only location for methodology knowledge. No copies, no forks. After retrospective/quick-learning writes, changes are committed and pushed to origin.
- **Triad index expanded** — from 5 fragmented entries to 12 unified entries with proper dedup.

</details>

<details>
<summary>What was new in v1.2</summary>

### Quick Learning — self-improving methodology

A TRIZ-optimized skill that extracts **reasoning patterns** (not specific decisions) from every session.

**How to use:**
- **Automatic:** runs before every session break in `/do-feature` and `/do-task` — no action needed.
- **Manual:** `/quick-learning` or say "быстрый анализ", "что улучшить в процессе".

**How it works:**

1. **Signal gate** — checks 3 binary signals (fix rounds, scope changes, recovery events). Clean session = skip entirely, zero cost.
2. **Triad decomposition** — each insight is split into `trigger → action → goal`. This enables precise similarity matching: exact match (Seen++), near match (merge best wording), or distinct (new entry).
3. **4-tier knowledge system:**

```
Tier 0: Triad Index          Tier 1: Transit Buffer       Tier 2: Skill Instructions    Tier 3: Quick Ref Card
triad-index.md               reasoning-patterns.md        {skill}/SKILL.md              quick-ref.md
~20 lines, read for dedup    Full entries, max 20         Promoted (Seen ≥ 3)           Top 7 one-liners
                              universal / situational      Permanent                     Loaded at session start
```

4. **Scope segmentation** — patterns classified as `universal` (always apply) or `situational` (context-matched, with explicit `Situation` field).
5. **Auto-promotion** — when a pattern is seen 3+ times across different features, it graduates into the relevant skill's SKILL.md as a permanent instruction and is removed from the buffer.

**Token cost:** background subagent (~5-7K tokens in isolated context). Main session cost: ~50 tokens (spawn + one-line summary). Signal gate skips clean sessions for zero cost.

</details>

<details>
<summary>What was new in v1.1</summary>

- Fixed deploy task skill reference (`infrastructure` -> `deploy-pipeline`)
- Fixed dimension count (10 -> 11), validator count (6 -> 5)
- Added `name: do-task`, `Bash` to code-reviewer agent tools
- Replaced documentation-writing reviewer (`code-reviewer` -> `documentation-reviewer`)
- Removed TypeScript/JavaScript bias from code-reviewer (now language-agnostic)
- Added LOC budget rationale, `estimated_loc` documentation, wave-conflicts in validator

</details>

## Quick Start

### New project
```
/init-project  -->  /init-project-knowledge  -->  start features
```

### New feature
```
/new-user-spec  -->  /new-tech-spec  -->  /decompose-tech-spec  -->  /do-feature  -->  /done
```

### Ad-hoc coding (no spec)
```
/write-code
```

### Quick session analysis (manual)
```
/quick-learning
```

## Installation

The repo is laid out as a drop-in overlay for your Claude Code config directory (`~/.claude/`). Contents to copy over: `skills/`, `agents/`, `shared/`, `CLAUDE.md`, `.gitignore`.

**Option 1 — merge into an existing config:**

```bash
git clone https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology.git /tmp/ai-dev-methodology
cp -r /tmp/ai-dev-methodology/{skills,agents,shared} ~/.claude/
cp /tmp/ai-dev-methodology/CLAUDE.md ~/.claude/CLAUDE.md   # review before overwriting
```

**Option 2 — fresh setup (empty `~/.claude/`):**

```bash
git clone https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology.git ~/.claude
```

After install, restart Claude Code to pick up new skills and agents. Verify with `/methodology` inside Claude Code — the skill should describe the full pipeline.

## License

Based on [molyanov-ai-dev](https://github.com/pavel-molyanov/molyanov-ai-dev) (MIT License).
