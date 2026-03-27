---
name: skeleton-pipe
description: |
  Creates a domain-specific pipeline from skeleton-pipe.md through adaptive interview.
  Clarifies execution environment, domain mechanics, roles, validators, templates.
  Generates all pipeline artifacts: skills, agents, templates, configuration.

  Use when: "создай пайплайн", "инстанцируй пайплайн", "instantiate pipeline",
  "новый пайплайн", "create pipeline", "пайплайн для", "pipeline for",
  "skeleton-pipe", "skeleton pipe", "скелет пайп"
---

# Instantiate Pipeline

Create a domain-specific pipeline from the universal skeleton through structured interview and artifact generation.

## Input

- Pipeline skeleton: `skeleton-pipe.md` in current project directory
- If not found: check `~/.claude/shared/templates/` or ask user for path

## Output

All artifacts are generated in the current project directory:

```
{project}/
├── pipeline.md                    # Main pipeline document (instantiated skeleton)
├── .claude/
│   ├── skills/
│   │   ├── {domain-skill-1}/SKILL.md
│   │   ├── {domain-skill-2}/SKILL.md
│   │   └── pipeline-knowledge/
│   │       └── references/
│   │           ├── domain.md          # Domain overview, terminology, constraints
│   │           ├── roles.md           # All roles and their responsibilities
│   │           ├── quality.md         # Quality dimensions, severity definitions
│   │           └── environment.md     # Execution environment, tools, constraints
│   ├── agents/
│   │   ├── {validator-1}.md
│   │   ├── {validator-2}.md
│   │   └── {reviewer-1}.md
│   └── shared/
│       └── templates/
│           ├── {spec-template}.md
│           ├── {task-template}.md
│           ├── {decision-log-template}.md
│           └── {checkpoint-template}.yml
└── work/                          # Working directory for pipeline execution
```

## Process

### Phase 0: Locate Skeleton

1. Search for `skeleton-pipe.md` in project directory
2. If not found — copy from skill references: `~/.claude/skills/instantiate-pipeline/references/skeleton-pipe.md` to project root
3. If references copy also missing — ask user for path
4. Read skeleton, confirm it contains all 12 mechanics + instantiation checklist
5. Read Section 13 (Instantiation Checklist) — this drives the interview

### Phase 1: Domain Discovery (Interview)

Conduct adaptive interview following Section 13 steps 1-2. One question at a time.

#### 1.1 Execution Environment (ask FIRST)

Before diving into domain, clarify WHERE and HOW the pipeline will run:

**Ask:**
- What is the execution environment? Options:
  - **AI agent runtime** (Claude Code, Cursor, Windsurf, custom agent framework)
  - **Human team** (project managers, analysts — pipeline as methodology guide)
  - **Hybrid** (humans + AI agents collaborate)
  - **Automation platform** (n8n, Zapier, Make, custom scripts)
  - **Other** (describe)

**Based on answer, follow up:**

For AI agent runtime:
- Which platform specifically? (Claude Code, Cursor, etc.)
- Are MCP tools available? Which ones?
- Context window constraints? (affects session budget)
- Can agents spawn subagents? (affects orchestration model)
- File system access? (affects artifact storage)

For human team:
- How many people? Roles?
- What tools do they use? (Jira, Notion, Google Docs, etc.)
- How do they communicate? (Slack, email, meetings)
- Pipeline as strict process or flexible guidelines?

For hybrid:
- Which stages are human, which are AI?
- Handoff mechanism between human and AI?
- Who approves gates — human always, or AI can auto-approve some?

For automation platform:
- Which platform?
- What integrations are available?
- Trigger mechanisms (webhook, schedule, manual)?
- State persistence (where to store checkpoints)?

**Record answers in environment profile:**
```yaml
environment:
  type: ai-agent | human-team | hybrid | automation
  platform: {specific platform}
  capabilities:
    subagent_spawning: true | false
    parallel_execution: true | false
    file_system: true | false
    persistent_state: true | false
    mcp_tools: [list]
  constraints:
    context_window: {size or "unlimited" for humans}
    session_duration: {typical duration}
    concurrency_limit: {max parallel workers}
  communication:
    channel: {how workers communicate}
    gate_approval: {who approves, how}
```

#### 1.2 Domain Definition

**Ask (one at a time, build on answers):**
- What domain is this pipeline for? Describe in one sentence.
- What is the unit of work? (What flows through the pipeline start to finish?)
- Who are the stakeholders? (Who requests work, who executes, who approves?)
- What does "quality" mean in this domain? (What makes output good vs bad?)
- What are the biggest risks? (What goes wrong most often?)

**Confirm understanding after 3-5 answers.**

#### 1.3 Pipeline Stages

**Ask:**
- What stages does work go through from request to completion?
- For each stage: what is the input and output?
- Which transitions require human approval (gates)?
- Are there stages that can run in parallel?

**Help when stuck:** Propose default 6-stage pipeline from skeleton, ask what to rename/add/remove.

#### 1.4 Effort & Capacity

**Ask:**
- What effort unit makes sense? (hours, story points, pages, items, tokens)
- How much can one executor handle in a single session?
- What is a typical "atomic task" size?

**If unsure:** Use defaults from skeleton (session: ~1200 units, task: ~300 units) and adapt unit name.

#### Checkpoint 1

Summarize to user:
- Domain: {one line}
- Environment: {type + platform}
- Unit of work: {name}
- Stages: {list with gates marked}
- Effort unit: {name}, session budget: {N}, task budget: {N}

Get confirmation before Phase 2.

### Phase 2: Quality System (Interview)

Walk through Section 13 steps 3-5.

#### 2.1 Quality Dimensions & Validators

**Ask:**
- What quality dimensions matter for your outputs? (correctness, compliance, safety, clarity, completeness, etc.)
- For each dimension: what would be a critical failure vs minor issue?
- At which stage should each dimension be checked?

**Propose validation matrix** based on answers. Show as table. Iterate.

#### 2.2 Reviewer Roles

**Ask:**
- What reviewer roles are needed? (Who checks what?)
- Are reviewers domain-specific or generic? (e.g., "safety reviewer" vs "general quality reviewer")
- What does a reviewer need to see to do their job? (full output, diff, summary?)

**Map reviewers to work types.** Show mapping. Iterate.

#### 2.3 Interview & Discovery

**Ask:**
- When gathering requirements for a new unit of work, what must be covered?
- What are the coverage areas? (e.g., for legal: jurisdiction, precedent, risk exposure, timeline)
- What context sources exist to scan before asking questions? (databases, prior work, templates)

#### Checkpoint 2

Show updated pipeline configuration:
- Validation matrix (table)
- Reviewer assignments (table)
- Interview coverage areas (list)

Get confirmation before Phase 3.

### Phase 3: Knowledge & Improvement (Interview)

Walk through Section 13 steps 6-7.

#### 3.1 Session Management

**Adapt to environment:**
- AI agent: checkpoint files, handoff prompts, context window management
- Human team: meeting notes, task boards, shift handoff protocols
- Hybrid: mixed — checkpoints for AI, summaries for humans
- Automation: state persistence, retry logic, webhook callbacks

**Ask:**
- What information does the next session need to resume seamlessly?
- How are session breaks triggered? (capacity limit, time, natural breakpoint)

#### 3.2 Self-Improvement Categories

**Ask:**
- What types of problems occur in your domain? Group them into categories.
- Where should lessons be stored? (Which role's instructions improve?)

**Propose category → role mapping.** Iterate.

#### Checkpoint 3

Show:
- Session management approach
- Pattern categories (list)
- Category → role mapping (table)

Get confirmation before Phase 4.

### Phase 4: Generate Artifacts

Generate all pipeline artifacts based on interview results.

#### 4.1 Pipeline Document

Create `pipeline.md` — instantiated version of `skeleton-pipe.md`:
- Replace all placeholders with domain-specific terms
- Fill validation matrix with concrete validators
- Fill review assignments with concrete reviewers
- Set concrete thresholds (effort units, session budget, etc.)
- Remove CUSTOMIZE sections (they're now filled)
- Keep HOW sections with domain-specific details

#### 4.2 Pipeline Knowledge

Create `pipeline-knowledge/references/`:

**domain.md:**
- Domain overview, terminology glossary
- Unit of work definition
- Stakeholder roles
- Quality definitions (what good/bad means)

**roles.md:**
- All executor roles with responsibilities
- All reviewer roles with review dimensions
- All validator roles with check criteria
- Role → skill mapping

**quality.md:**
- Quality dimensions with severity definitions (critical/major/minor)
- Validation matrix (full table)
- Gate-blocking rules
- Review round limits

**environment.md:**
- Execution environment profile (from Phase 1.1)
- Tool availability and constraints
- Communication channels
- State persistence mechanism

#### 4.3 Templates

Generate templates for each artifact type:

**Spec template** — requirements document structure with domain-specific sections
**Task template** — atomic task with frontmatter (status, wave, dependencies, skills, reviewers)
**Decision log template** — append-only log with Planned/Actual/Deviation structure
**Checkpoint template** — session state for resume

Adapt frontmatter fields to environment:
- AI agent: YAML frontmatter in markdown files
- Human team: structured sections in Google Docs / Notion
- Automation: JSON/YAML config files

#### 4.4 Skills (if AI agent environment)

For each domain-specific methodology, create a skill:
- SKILL.md with frontmatter (name, description, trigger phrases)
- Workflow steps adapted from skeleton mechanics
- Domain-specific instructions

Minimum skills to generate:
- `{domain}-spec-planning` — requirements gathering for this domain
- `{domain}-execution` — task execution methodology
- `{domain}-review` — review methodology and dimensions

#### 4.5 Agents (if AI agent environment)

For each validator and reviewer role, create agent definition:
- YAML frontmatter (name, description, skills, allowed-tools, model)
- Input/Output contract
- Process steps

#### 4.6 Escalation & Completion Config

Create escalation protocol adapted to environment:
- Escalation triggers (domain-specific)
- Escalation channels (Slack, email, in-tool message)
- Completion checklist (domain-specific "done" criteria)
- Archive structure

### Phase 5: Review & Commit

#### 5.1 Self-Verify

Before showing to user:
- All templates have no remaining `{placeholder}` tokens
- Validation matrix references only defined validators
- Reviewer assignments reference only defined reviewers
- Category → role mapping references only defined roles
- Environment profile matches generated artifacts

#### 5.2 Show Results

Present to user:
- List of all generated files with brief description of each
- Pipeline summary (stages, gates, validators, reviewers)
- Environment configuration summary

#### 5.3 Iterate

Changes requested → edit → show updated list → repeat until approved.

#### 5.4 Commit

After approval, commit all generated artifacts.

Final message: "Pipeline for {domain} created. Run a test pass with a sample unit of work to verify the flow."
