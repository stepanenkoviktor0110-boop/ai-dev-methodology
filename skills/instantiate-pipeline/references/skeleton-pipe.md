# Skeleton Pipe v1.0

A domain-agnostic framework for building spec-driven pipelines with automated quality gates, parallel execution, and continuous self-improvement. Extracted from a battle-tested AI-First Development Methodology.

**How to read this document:** Each mechanic is described with WHAT (definition), WHY (rationale), HOW (implementation), and CUSTOMIZE (domain adaptation points). Placeholders like `{domain-term}` indicate where you insert domain-specific concepts.

**Key terms used throughout:**
- *Feature* — a placeholder for the unit of work your pipeline processes. Replace with your domain equivalent: brief, project, report, case, experiment, etc.
- *Executor* — the agent (human or automated) responsible for completing a task.
- *Effort units* — your domain's measure of work volume: hours, story points, pages, items, etc.

---

## Table of Contents

1. [Pipeline Stages & Gates](#1-pipeline-stages--gates)
2. [Adaptive Interview](#2-adaptive-interview)
3. [Spec - Decomposition - Execution](#3-spec--decomposition--execution)
4. [Validation Matrix](#4-validation-matrix)
5. [Review Cycles](#5-review-cycles)
6. [Session Management](#6-session-management)
7. [Self-Improvement Loop](#7-self-improvement-loop)
8. [4-Tier Knowledge System](#8-4-tier-knowledge-system)
9. [Agent Orchestration](#9-agent-orchestration)
10. [Template System](#10-template-system)
11. [Escalation Pattern](#11-escalation-pattern)
12. [Archive & Completion](#12-archive--completion)
13. [Instantiation Checklist](#13-instantiation-checklist)

---

## 1. Pipeline Stages & Gates

### WHAT

A sequence of mandatory stages where each stage produces a well-defined artifact, and a **hard stop (gate)** prevents progression until the artifact meets quality criteria and receives explicit human approval.

### WHY

- Prevents garbage-in-garbage-out propagation across stages
- Makes quality non-negotiable — you cannot skip validation
- Creates clear accountability: each stage has an owner and a verifiable output
- Enables resume and handoff — anyone can pick up from the last approved gate

### HOW

The pipeline consists of 6 stages with 3 explicit human gates (more can be added per domain):

```
Stage 1: Requirements Gathering
  ├── Adaptive interview (see Mechanic #2)
  ├── Validators: {requirements-quality-validator}, {requirements-feasibility-validator}
  ├── Max 3 validation rounds
  └── GATE 1: Human approves requirements spec
          ↓
Stage 2: Solution Design
  ├── Research existing context / constraints
  ├── Create solution spec (architecture, decisions, plan)
  ├── Validators: {mirage-detector}, {completeness-validator}, {risk-validator},
  │               {domain-quality-validator}, {template-validator}
  ├── Max 3 validation rounds
  └── GATE 2: Human approves solution spec
          ↓
Stage 3: Task Decomposition
  ├── Break solution into atomic tasks
  ├── Estimate effort per task
  ├── Validators: {task-template-validator}, {reality-checker}
  ├── Cross-task integration check
  ├── Group tasks into sessions (by capacity budget)
  └── GATE 3: Human approves task breakdown + session plan
          ↓
Stage 4: Execution
  ├── Execute tasks in parallel waves (see Mechanic #9)
  ├── Per-task review cycles (see Mechanic #5)
  ├── Session boundary checkpoints (see Mechanic #6)
  ├── Audit wave: holistic quality review of all outputs
  └── Final wave: acceptance testing + delivery
          ↓
Stage 5: Retrospective
  ├── Extract lessons from problems encountered
  ├── Write to knowledge buffer (see Mechanic #7)
  └── Promote confirmed patterns to permanent instructions
          ↓
Stage 6: Completion
  ├── Update domain knowledge base
  ├── Archive all artifacts
  └── Report summary to human
```

**Gate rules:**
- Gate = explicit human approval (not automatic)
- Work on next stage CANNOT begin until gate passes
- If validation fails after 3 rounds → escalate to human (see Mechanic #11)
- Each gate produces a versioned, immutable artifact

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Stage names | Rename to match your domain (e.g., "Brief → Blueprint → Sprint") |
| Gate criteria | What constitutes "approved" in your domain |
| Validators per stage | Which quality checks matter for your artifacts |
| Artifact format | Document type, structure, required sections |
| Number of stages | You may merge or split stages (minimum 3: spec → tasks → execution) |

---

## 2. Adaptive Interview

### WHAT

A structured discovery process that gathers requirements through contextually-aware questions rather than static forms. Questions adapt based on previous answers, available context, and detected complexity.

### WHY

- Static forms miss domain-specific nuances
- Follow-up questions reveal hidden requirements
- Scaling depth by complexity prevents over-engineering small tasks and under-specifying large ones
- Completeness checks catch gaps before they become expensive downstream

### HOW

**Three-cycle structure:**

```
Cycle 1: General Understanding
  "What is this? Who is it for? What problem does it solve?"
  → Broad strokes, establish scope

Cycle 2: Context-Informed Deep Dive
  Scan existing context (codebase, documents, prior work)
  → Ask targeted questions based on what you found
  "How does this relate to {existing-thing}? What about {detected-pattern}?"

Cycle 3: Edge Cases & Boundaries
  → Stress-test requirements
  "What happens when {failure-scenario}? What about {boundary-condition}?"
```

**Questioning rules:**
- One question at a time — wait for answer before forming next question
- Build on answers — use response to inform follow-up
- Confirm understanding every 3-5 questions (brief summary)
- When user says "not sure": offer 2-3 common approaches, ask which is closer
- If still uncertain and optional → mark TBD, move on
- If still uncertain and required → break into simpler sub-questions
- On scope expansion → stop, recount, confirm updated scope

**Completeness check:**
- After cycles complete, run `{completeness-checker}` against coverage areas
- Coverage areas: purpose, workflows, data requirements, error scenarios, integration points, edge cases
- If any area < 70% covered → ask additional targeted questions
- If all areas ≥ 70% → proceed to spec drafting

**Complexity scaling (S/M/L):**

| Size | Indicators | Interview depth |
|------|-----------|----------------|
| S (small) | Single concern, clear scope, no integrations | 1 cycle, 3-5 questions |
| M (medium) | Multiple concerns, some integrations, known patterns | 2 cycles, 8-12 questions |
| L (large) | Cross-cutting concerns, multiple integrations, unknowns | 3 full cycles, 15-25 questions, completeness check mandatory |

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Coverage areas | What must be covered in your domain (e.g., regulatory, safety, budget) |
| Context sources | What to scan before Cycle 2 (existing docs, databases, prior reports) |
| Complexity indicators | How to determine S/M/L in your domain |
| Completeness threshold | 70% is default — adjust based on domain risk tolerance |
| Domain-specific cycles | Add cycles for your domain (e.g., "Regulatory Compliance" cycle) |

---

## 3. Spec - Decomposition - Execution

### WHAT

A three-phase cycle that transforms requirements into deliverables: (1) Specification defines WHAT and HOW at a high level, (2) Decomposition breaks it into atomic executable tasks, (3) Execution processes tasks in parallel waves with quality gates.

### WHY

- Specifications capture intent and architectural decisions before execution begins
- Decomposition creates tasks small enough to execute, validate, and review independently
- Wave-based execution maximizes parallelism while respecting dependencies
- Each phase has its own validation, preventing errors from compounding

### HOW

**Phase 1: Specification**

Two-tier spec system:
- **Requirements Spec** — human-readable, captures WHAT and WHY
  - Problem statement, audience, key features, acceptance criteria, scope boundaries
- **Solution Spec** — executor-readable, captures HOW
  - Architecture, key decisions (with rationale), resource management, implementation plan
  - Each decision: problem → options considered → chosen option → why
  - Implementation plan: ordered list of tasks (brief descriptions, not full tasks yet)

**Phase 2: Decomposition**

Step 0: Scope estimation
- Estimate total effort for the feature
- Break into blocks of ~1200 effort units (configurable, see Appendix) per session
- Break blocks into steps of ~300 effort units (configurable) per task
- Present plan as table, get human confirmation

Step 1: Create tasks (parallel)
- For each planned task → create task file from template
- Each task includes: description, acceptance criteria, verification method, dependencies, wave assignment, required skills, assigned reviewers

Step 2: Validate tasks
- Run `{task-template-validator}` (batch: 5 tasks per call)
- Run `{reality-checker}` (batch: 3 tasks per call)
- Cross-task integration check: shared resource conflicts, hidden dependencies, duplicate work
- Max 3 individual rounds + 2 cross-task rounds

Step 3: Session planning
- Group waves into sessions by capacity budget
- Never split a wave across sessions
- Audit + Final waves → always last session
- Generate session plan with handoff context

**Phase 3: Execution**

See Mechanics #5 (Review Cycles), #6 (Session Management), #9 (Agent Orchestration) for details.

Core flow:
1. Initialize: read specs, build wave plan, set up team
2. Execute wave: process all tasks in wave in parallel
3. Wave transition: verify outputs, update checkpoint, check session boundary
4. Repeat until all waves complete
5. Audit wave: holistic quality review of all outputs
6. Final wave: acceptance testing + delivery
7. Human review: present results, iterate on feedback (max 3 rounds)

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Spec sections | What sections does each spec type need in your domain |
| Task granularity | What constitutes an "atomic task" (default: ~300 effort units (configurable) effort units) |
| Wave criteria | How to group tasks into parallel waves |
| Capacity budget | Effort limit per session (default: ~1200 units) |
| Acceptance criteria format | How to express verifiable success conditions |

---

## 4. Validation Matrix

### WHAT

A configuration matrix that defines which validators run at which pipeline stage, how many rounds are allowed, and what happens when validation fails.

### WHY

- Different stages need different quality checks
- Parallel validators maximize coverage without sequential bottleneck
- Round limits (max 3) prevent infinite fix loops
- Escalation path ensures nothing gets stuck silently

### HOW

**Matrix structure:**

| Stage | Validators | Count | Parallel? | Max Rounds | On failure |
|-------|-----------|-------|-----------|------------|-----------|
| Requirements | {quality}, {feasibility} | 2 | Yes | 3 | Escalate |
| Solution Design | {mirage}, {completeness}, {risk}, {domain}, {template} | 5 | Yes | 3 | Escalate |
| Task Decomposition | {task-template}, {reality} + cross-task | 2+1 | Yes | 3+2 | Escalate |
| Per-task Execution | {output-reviewer}, {risk-reviewer}, {coverage-reviewer} | 1-3 | Yes | 3 | Escalate |
| Audit Wave | {holistic-output}, {holistic-risk}, {holistic-coverage} | 3 | Yes | 3 (fix) | Escalate |
| Acceptance | {pre-delivery}, {post-delivery} | 2 | Sequential | — | Fix & retest |

**Validation cycle:**

```
Run all validators in parallel
         ↓
Collect findings (severity: critical / major / minor)
         ↓
Fix findings
         ↓
Re-run validators (round N+1)
         ↓
If round > max_rounds AND findings remain → ESCALATE to human
If all findings resolved → PASS
```

**Severity-based behavior:**
- **Critical:** Must fix before proceeding. Blocks gate.
- **Major:** Should fix. Multiple majors block gate.
- **Minor:** Fix or acknowledge. Does not block gate alone.

**Validator output contract** (structured report format ensuring uniform processing by the orchestrator):
```
{
  "status": "approved" | "changes_required",
  "findings": [
    {
      "severity": "critical | major | minor",
      "title": "...",
      "description": "...",
      "location": "...",
      "suggestion": "..."
    }
  ],
  "summary": "..."
}
```

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Validators per stage | Which quality dimensions matter at each stage |
| Severity definitions | What is critical/major/minor in your domain |
| Max rounds | 3 is default; increase for high-stakes domains, decrease for speed |
| Batch sizes | How many items per validator call |
| Gate-blocking rules | Which severity combinations block progression |

---

## 5. Review Cycles

### WHAT

A structured process where completed work is reviewed by one or more independent reviewers in parallel, with severity-based decisions and a bounded number of fix-and-resubmit rounds.

### WHY

- Independent review catches blind spots the executor cannot see
- Parallel reviewers cover different quality dimensions simultaneously
- Bounded rounds (max 3) prevent review ping-pong
- Severity-based decisions make fix/skip decisions objective

### HOW

**Review process (per task):**

```
Step 1: Executor completes work (passes own verification)
         ↓
Step 2: Executor prepares review package
        (changed artifacts, context, specs for reference)
         ↓
Step 3: Each reviewer receives package in parallel
         ↓
Step 4: Each reviewer produces structured report
        {status, findings[], summary}
         ↓
Step 5: Executor reads all reports, fixes findings
         ↓
Step 6: Executor sends updated package to reviewers (round N+1)
         ↓
Step 7: If round > 3 AND findings remain → ESCALATE
        If all reviewers approve → DONE
```

**Finding evaluation:**
- Each finding evaluated on merit — severity is metadata, not a filter
- A valid minor improvement still improves quality → apply it
- Rule: if finding is valid AND improves output → apply (any severity)

**Review dimensions (adapt to domain):**
1. Structural integrity (is the output well-organized?)
2. Correctness (does it produce the right result?)
3. Completeness (does it cover all requirements?)
4. Risk exposure (are there unmitigated risks?)
5. Maintainability (can someone else understand and modify this?)
6. Standards compliance (does it follow domain conventions?)

**Audit review (holistic, after all tasks complete):**
- Separate from per-task reviews
- 3 auditors review ALL outputs holistically (not just diffs)
- Each auditor focuses on different quality dimension
- If issues found → spawn fixer, auditors become reviewers
- Standard 3-round protocol applies

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Review dimensions | Which quality aspects matter in your domain |
| Reviewer roles | Who reviews what (e.g., "safety reviewer", "compliance reviewer") |
| Review package contents | What information reviewers need |
| Report format | Fields in the structured review report |
| Round limit | 3 is default; adjust for domain risk level |

---

## 6. Session Management

### WHAT

A system for dividing large work into bounded sessions, checkpointing progress, and enabling seamless resume across session breaks.

### WHY

- Executors have bounded capacity (context window, attention span, shift length)
- Checkpoints enable resume without re-reading everything
- Session handoff prompts ensure continuity across breaks
- Capacity budgets prevent overload and quality degradation

### HOW

**Capacity budgeting:**

```
Total effort estimate for feature: E units
Session budget: ~B units (±25%)
Number of sessions: ceil(E / B)

Grouping rules:
- Walk waves in order, accumulate task effort into current session
- If adding next wave exceeds budget → start new session
- NEVER split a wave across sessions (parallel tasks must stay together)
- Audit + Final waves → always last session (fixed, no budget)
- Single wave > budget → warn human, it gets own session
```

**Checkpoint structure:**

Written after each wave completes. Contains:
```yaml
pipeline: {pipeline-name}
work_item: {work-item-name}       # "feature", "brief", "case" — your domain term
work_item_location: {path}        # where artifacts live

last_completed_wave: N             # 0 = fresh start
total_waves: N
next_wave: N

units:                             # individual work units (tasks, steps, actions)
  1: done
  2: done
  3: in_progress

current_session: N                 # 1-indexed
total_sessions: N
```

**Resume protocol (after break or context loss):**
1. Read checkpoint
2. If `last_completed_wave > 0` → resume scenario
3. Read decision log to confirm what actually completed
4. For each task: has decision log entry → mark done, skip; no entry → re-execute
5. Check team state: alive → continue; dead → recreate
6. Skip to next wave execution

**Session handoff:**

When current session's last wave completes:
1. Generate next-session prompt (template with filled variables)
2. Include: feature name, completed work, next session scope, context files
3. Save prompt to file (overwrite each time)
4. Present to human with instruction to start new session
5. **STOP execution** — do not proceed to next wave

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Capacity unit | What you measure (LOC, story points, hours, token count) |
| Session budget | How much fits in one session (default: ~1200 units) |
| Checkpoint fields | What state to save for resume |
| Handoff template | What information the next session needs |
| Break triggers | What triggers a session boundary (end of wave + over budget) |

---

## 7. Self-Improvement Loop

### WHAT

A dual-writer system that continuously extracts lessons from work and feeds them back into the pipeline's instructions. Two types of learning operate at different granularities: session-level pattern extraction and feature-level operational lessons.

### WHY

- Mistakes repeat if not captured and fed back
- Two granularities catch different signals: tactical (session) and strategic (feature)
- Signal gating (skip if nothing went wrong) prevents noise accumulation
- Similarity deduplication prevents knowledge bloat
- Automatic promotion of confirmed patterns makes improvement permanent

### HOW

**Dual writers:**

| Writer | Granularity | Trigger | Focus | Max entries |
|--------|------------|---------|-------|-------------|
| Quick-learning | Session | Automatic at session breaks | HOW decisions were made (reasoning patterns) | 2 per session |
| Retrospective | Feature | After feature completion | WHAT went wrong and why (operational lessons) | 3 per feature |

**Both writers use the same process:**

```
Step 1: Signal Gate (fast check)
  Check binary signals:
  - Fix rounds detected? (something went wrong and was corrected)
  - Scope change detected? (plan didn't survive contact with reality)
  - Recovery event detected? (non-obvious recovery path found)

  ALL signals = zero → SKIP entirely ("Clean session, no new patterns")
  ≥ 1 signal → proceed to analysis

Step 2: Analyze
  For each signal:
  - Was the first approach correct? What signal should have changed it?
  - What was the cost of the detour? (wasted rounds, rework)
  - Is this transferable? Would help on a DIFFERENT project?

  Nothing non-obvious → skip writing. Don't force lessons.

Step 3: Write (Triad-Based)
  Formulate insight as: Trigger → Action → Goal

  Before writing, run Similarity Check:
  - Read triad index (~30 rows max)
  - For each existing entry, compare:
    - EXACT match (same action AND goal) → increment Seen counter, do NOT add
    - NEAR match (same goal, different action) → merge, keep more actionable, increment Seen
    - DISTINCT (different goal) → add as new entry
  - Pre-filter: if Goal shares 3+ content words with existing → Near candidate

Step 4: Promotion Check
  If any entry reaches Seen ≥ 3 → promote to permanent instructions
  (See Mechanic #8: 4-Tier Knowledge System)
```

**Entry format:**
```markdown
### {date} {feature} / session {N}: {title}

**Seen:** 1
**Triad:** {trigger} → {action} → {goal}
**Context:** {what situation triggered this — 1 sentence}
**Pattern:** {transferable instruction — 1-2 sentences, imperative}
**Scope:** universal | situational
**Situation:** {only for situational — when this applies}
**Category:** {domain-category}
```

**Scope rules:**
- **Universal** — applies to any project/domain → stored in Universal section
- **Situational** — requires specific context → stored in Situational section + Situation field

**Writing rules:**
- Actionable — concrete instruction, not vague advice
- Non-obvious — don't capture what everyone already knows
- Must have Triad field (Trigger → Action → Goal)

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Signal types | What binary signals indicate problems in your domain |
| Categories | Domain-specific pattern categories (e.g., "safety", "compliance", "logistics") |
| Category → skill mapping | Where promoted patterns land |
| Max entries | 2/session + 3/feature is default; adjust for domain noise level |
| Scope definitions | What "universal" vs "situational" means in your domain |

---

## 8. 4-Tier Knowledge System

### WHAT

A graduated knowledge management system with four tiers: raw pattern index → transit buffer → permanent skill instructions → quick-reference card. Patterns automatically flow upward as they prove their value through repeated observation.

### WHY

- Raw observations need validation before becoming permanent instructions
- Tier separation prevents noise from polluting stable knowledge
- Automatic promotion (Seen ≥ 3) ensures only confirmed patterns persist
- Quick-ref card gives immediate access to highest-value patterns
- Pruning prevents unbounded growth

### HOW

```
Tier 0: Triad Index
  ├── One-line-per-pattern lookup table (~30 rows max)
  ├── Used for similarity check (dedup) by both writers
  ├── Updated on every write (add/merge/remove)
  └── Source of truth for Seen counters

Tier 1: Transit Buffer
  ├── Full pattern entries (triad + context + category)
  ├── Two sections: Universal and Situational
  ├── Written by: quick-learning + retrospective
  ├── Read by: writers (for merging), promotion process
  └── Pruned when index > 25 rows

Tier 2: Permanent Instructions
  ├── Promoted patterns (Seen ≥ 3) embedded in skill/role instructions
  ├── 1-2 lines, imperative, integrated into existing workflow
  ├── Effect: becomes standard practice for that role
  └── Trigger: automatic when Seen counter hits 3

Tier 3: Quick Reference Card
  ├── Top 5-7 universal promoted patterns
  ├── Loaded at session start (minimal context cost)
  ├── Regenerated on each promotion
  └── Immediate applicability across all work
```

**Promotion process (Seen ≥ 3):**
1. Identify target skill/role by pattern category
2. Add pattern as permanent instruction in role's playbook
3. Remove entry from transit buffer
4. Remove row from triad index
5. If universal → update quick-ref card

**Pruning rules (when index > 25 rows):**
1. Remove entries with Seen: 1 older than 30 days
2. Merge similar entries (same insight, different wording)
3. Remove contradicted entries (newer entry invalidates older)

**Key thresholds:**

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Max index rows | 25 | Buffer growth limit |
| Promotion trigger | Seen ≥ 3 | Pattern confirmed across 3+ sessions |
| Pruning: stale entries | Seen: 1, older than 30 days | Remove unconfirmed noise |
| Quick-ref max | 7 entries | Minimal context cost at session start |
| Similarity pre-filter | 3+ shared content words in Goal | Mechanical heuristic for Near matches |

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Category → role mapping | Which role receives promoted patterns for each category |
| Index size limit | 25 is default; increase for high-volume domains |
| Promotion threshold | Seen ≥ 3 is default; increase for high-stakes domains |
| Stale entry age | 30 days is default; for low-frequency domains (monthly cycles) consider 90+ days; for high-frequency (daily cycles) consider 7 days |
| Quick-ref size | 7 is default; adjust for context cost constraints |

---

## 9. Agent Orchestration

### WHAT

A system for dividing work between roles (skills) and workers (agents), enabling parallel execution through wave-based team coordination with a single level of orchestration.

### WHY

- Skills (WHAT to do) and agents (WHO does it) have different lifecycles
- One skill can power multiple agents; agents cannot call other agents
- Single orchestration level keeps coordination tractable
- Wave-based parallelism maximizes throughput while respecting dependencies
- Team abstraction enables persistent coordination across session breaks

### HOW

**Skill vs Agent distinction:**

| Concept | Skill (Role) | Agent (Worker) |
|---------|-------------|----------------|
| Contains | Methodology, knowledge, instructions | Isolated process with defined inputs/outputs |
| Lifecycle | Persistent, evolves with promotions | Created per task, disposable |
| Usage | Loaded inline or by agents | Spawned by orchestrator |
| Nesting | Can reference other skills | CANNOT spawn other agents |
| Analogy | Job description | Contractor hired for the job |

**Orchestration rules:**
- **One level only:** Orchestrator → agents. Agents cannot spawn sub-agents.
- If an agent needs more work done → returns to orchestrator → orchestrator spawns new agent
- Each agent receives: task description, context files, skill to load, output contract

**Wave-based parallel execution:**

```
Wave 1: [Task A, Task B, Task C]  ← no dependencies between them
  All execute in parallel, each with own agent + reviewers
  Wait for ALL to complete
         ↓
Wave 2: [Task D, Task E]  ← depend on Wave 1 tasks
  All execute in parallel
  Wait for ALL to complete
         ↓
Wave N-1: Audit Wave  ← holistic review
  3 auditors review ALL outputs in parallel
  Fix cycle if issues found
         ↓
Wave N: Final Wave  ← acceptance + delivery
  Sequential: test → deliver → verify
```

**Team structure per task:**

```
Orchestrator (lead)
  ├── Executor agent (does the work)
  │     ├── Loads required skill
  │     ├── Produces output
  │     └── Sends to reviewers
  ├── Reviewer agent 1 (checks dimension A)
  ├── Reviewer agent 2 (checks dimension B)
  └── Reviewer agent 3 (checks dimension C)
```

**Agent output contract** (structured result format so the orchestrator can process all agent outputs uniformly):
```json
{
  "status": "success | partial | failed",
  "outputs": ["list of produced artifacts"],
  "summary": "what was done",
  "issues": ["unresolved items, if any"]
}
```

**Ad-hoc agent assignment (outside original plan):**
1. Identify work type
2. Assign matching skill + reviewers
3. Standard review protocol (max 3 rounds)
4. Log decision

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Roles (skills) | Domain-specific methodologies (e.g., "safety-analysis", "compliance-check") |
| Agent types | Worker types for your domain (e.g., "analyst", "auditor", "drafter") |
| Reviewer assignments | Which reviewers for which work type |
| Wave structure | How to determine task dependencies and grouping |
| Output contracts | What each agent type must return |
| Team naming | Convention for team identification |

---

## 10. Template System

### WHAT

A copy-first pattern where all artifacts are created by copying a template and editing sections in place, with frontmatter-driven status tracking for pipeline state management.

### WHY

- Copy-first ensures no sections are accidentally skipped
- Templates enforce consistent structure across all artifacts
- Frontmatter enables automated status tracking and pipeline state queries
- Validation can check template completeness mechanically

### HOW

**Copy-first pattern:**

```
Step 1: Read template file from template library
Step 2: Copy to target location (e.g., work/{feature}/spec.md)
Step 3: Edit each section in place — fill with real content
Step 4: No sections removed or renamed (validators check this)
```

**Frontmatter structure:**

Every artifact has YAML frontmatter tracking its pipeline state:

```yaml
---
status: planned              # planned → in_progress → done | done_with_concerns
depends_on: [1, 2]          # IDs of prerequisite artifacts
wave: 1                      # parallel execution group
skills: [skill-name]         # required methodologies
reviewers: [reviewer-a]      # assigned reviewers (or "none")
assigned_to: worker-name     # who is executing this
estimated_effort: 300        # effort units for capacity planning
concerns:                    # only when done_with_concerns
---
```

**Status transitions:**
```
planned → in_progress → done
                      → done_with_concerns (has unresolved worries)
                      → escalated (blocked, needs human input)
```

**Template library contents (adapt to domain):**
- Requirements spec template
- Solution spec template
- Task template
- Decision log template
- Checkpoint template
- Execution plan template
- Session plan template
- Session handoff prompt template

**Validation of completeness:**
- All required sections present (structural check)
- All frontmatter fields valid (type check, value constraints)
- Content in each section non-empty and sensible (semantic check)

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Template types | Which artifact types need templates in your domain |
| Frontmatter fields | Status tracking fields relevant to your pipeline |
| Status values | Valid status transitions |
| Template location | Where templates live in your project structure |
| Required sections | Which sections must be present per template type |

---

## 11. Escalation Pattern

### WHAT

A defined protocol for when and how to escalate unresolvable issues to the human operator, including what to report, how to preserve state, and how to resume after resolution.

### WHY

- Bounded iteration (max 3 rounds) means some issues WILL need human input
- Without a protocol, agents either loop forever or silently drop issues
- Structured escalation reports help humans make informed decisions quickly
- State preservation ensures work isn't lost during the pause

### HOW

**Escalation triggers:**

| Trigger | When |
|---------|------|
| Validation impasse | 3 validation rounds exhausted, findings remain |
| Review impasse | 3 review rounds exhausted, findings remain |
| Blocker | Worker encounters ambiguous requirement or missing information |
| External dependency | Task requires unavailable tool, service, or resource |
| Conflicting requirements | Spec contradicts itself or domain constraints |

**Escalation protocol:**

```
Step 1: STOP all work on blocked item
  (other items in other waves may continue)

Step 2: Report to human:
  - What failed (brief title)
  - What was tried (all N attempts, summarized)
  - What remains unresolved (specific findings)
  - Recommendation (if any)

Step 3: Log the escalation:
  - Write decision log entry with status "escalated"
  - Include: attempts summary + unresolved findings

Step 4: Save checkpoint
  - Persist current state so work can resume

Step 5: Wait for human decision
  - Do NOT continue on blocked item
  - Do NOT attempt creative workarounds
  - Present options if applicable
```

**Escalation report template:**
```markdown
## Escalation: {title}

**Blocked:** {what is blocked — task, validation, review}
**Attempts:**
1. {what was tried first} — {result}
2. {what was tried second} — {result}
3. {what was tried third} — {result}
**Unresolved:** {specific remaining issue}
**Recommendation:** {suggested path forward, or "needs human judgment"}
```

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Escalation triggers | Domain-specific blockers (e.g., "regulatory ambiguity", "safety concern") |
| Escalation channels | How to reach the human (message, ticket, alert) |
| Max attempts before escalation | 3 is default; adjust for domain |
| Report format | Fields relevant to your decision-makers |
| Priority levels | Urgency classification for escalations |

---

## 12. Archive & Completion

### WHAT

A finalization process that verifies completeness, extracts lessons, updates the domain knowledge base, and archives all artifacts for future reference.

### WHY

- Completion checklist prevents premature closure
- Lesson extraction feeds the self-improvement loop
- Knowledge base updates ensure future work benefits from past decisions
- Archiving preserves full audit trail without cluttering active workspace

### HOW

**Completion checklist (verify before closing):**
- [ ] All tasks status = `done` (or `done_with_concerns`)
- [ ] All acceptance criteria verified
- [ ] All spec checkboxes updated
- [ ] Decision log complete with all entries
- [ ] Acceptance testing passed
- [ ] Post-delivery verification passed (if applicable)

**Completion workflow:**

```
Step 1: Verify completeness (checklist above)
  If incomplete → warn human, list gaps

Step 2: Run retrospective (Mechanic #7)
  Extract operational lessons (WHAT went wrong)
  Write to knowledge buffer
  Promote confirmed patterns (Seen ≥ 3)

Step 3: Update domain knowledge base
  Review current knowledge files
  Update only files affected by this feature:
  - Architecture/structure changes
  - New patterns discovered
  - Process/workflow changes
  - Deployment/operational changes
  Quality rules: no raw artifacts, no obvious content, only domain-specific insights

Step 4: Archive
  Move feature directory → completed archive
  Preserve: specs, decision log, task files, logs, review reports

Step 5: Commit & report
  Save all changes
  Report to human:
  - Summary of what was delivered
  - Knowledge base updates made
  - Archive location
  - Lessons extracted (if any)
```

**Archived feature structure:**
```
completed/{feature}/
├── requirements-spec      # original requirements
├── solution-spec          # original architecture/decisions
├── decision-log           # all decisions + outcomes
├── tasks/                 # completed task files
└── logs/                  # execution logs, review reports, QA results
```

### CUSTOMIZE

| Element | What to define |
|---------|---------------|
| Completion criteria | What "done" means in your domain |
| Knowledge base files | Which domain knowledge files to update |
| Archive location | Where completed features go |
| Retention policy | How long archives are kept |
| Report format | What stakeholders need to see in the completion report |

---

## 13. Instantiation Checklist

Use this checklist to create a pipeline for your specific domain.

### Step 1: Define Your Domain

- [ ] Name your pipeline (e.g., "Legal Brief Pipeline", "Research Paper Pipeline")
- [ ] Define what a "feature" is in your domain (the unit of work the pipeline processes)
- [ ] Define your effort unit (hours, story points, pages, items)
- [ ] Set capacity budget per session (default: ~1200 units)
- [ ] Set task budget (default: ~300 units, ¼ of session budget)

### Step 2: Define Pipeline Stages

- [ ] List your stages (minimum 3: spec → tasks → execution)
- [ ] For each stage: define the output artifact and its format
- [ ] For each gate: define what "approved" means
- [ ] Create artifact templates for each stage (copy-first pattern)
- [ ] Define frontmatter fields for status tracking

### Step 3: Define Validators & Reviewers

- [ ] List quality dimensions that matter in your domain
- [ ] Map validators to stages (fill the validation matrix)
- [ ] Define severity levels (critical/major/minor) for your domain
- [ ] Define reviewer roles and what each reviews
- [ ] Set max validation/review rounds (default: 3)
- [ ] Define gate-blocking rules (which severities block progression)

### Step 4: Define Roles (Skills) & Workers (Agents)

- [ ] List domain-specific skills (methodologies, checklists, standards)
- [ ] List agent types (executor, reviewer, auditor)
- [ ] Map: which skills are loaded by which agents
- [ ] Map: which reviewers are assigned to which work types
- [ ] Define agent output contracts (JSON structure)

### Step 5: Configure Interview & Discovery

- [ ] Define coverage areas for your domain
- [ ] Define complexity indicators (S/M/L)
- [ ] List context sources to scan before deep-dive questions
- [ ] Set completeness threshold (default: 70%)
- [ ] Add domain-specific interview cycles if needed

### Step 6: Configure Session Management

- [ ] Define checkpoint fields for your domain
- [ ] Create session handoff prompt template
- [ ] Define session boundary triggers
- [ ] Define resume protocol for your context

### Step 7: Configure Self-Improvement

- [ ] Define signal types (what indicates problems in your domain)
- [ ] Define pattern categories (8-12 domain categories)
- [ ] Map categories to target skills (where promoted patterns land)
- [ ] Set up 4-tier knowledge files:
  - [ ] Triad index (lookup table)
  - [ ] Transit buffer (full entries)
  - [ ] Skill instruction files (promotion targets)
  - [ ] Quick-ref card (top 5-7 patterns)

### Step 8: Configure Escalation & Completion

- [ ] Define escalation triggers for your domain
- [ ] Define escalation channels (how to reach the human)
- [ ] Define completion checklist items
- [ ] Define which knowledge base files to update on completion
- [ ] Define archive structure and retention policy

### Step 9: Verify

- [ ] Walk through the full pipeline with a sample feature
- [ ] Verify every gate has clear approval criteria
- [ ] Verify every stage has at least one validator
- [ ] Verify escalation path works (simulate a 3-round failure)
- [ ] Verify session handoff preserves enough context to resume
- [ ] Verify interview coverage areas are defined and completeness threshold is set
- [ ] Verify knowledge promotion pipeline flows end-to-end

---

## Appendix: Key Thresholds Reference

| Parameter | Default | Unit | Rationale |
|-----------|---------|------|-----------|
| Session capacity budget | ~1200 | effort units | Empirically sized to fit executor capacity |
| Task effort budget | ~300 | effort units | ¼ of session, atomic enough to validate independently |
| Max validation rounds | 3 | rounds | Diminishing returns; escalate after |
| Max review rounds | 3 | rounds | Same rationale |
| Max cross-task rounds | 2 | rounds (extra) | Integration issues have fewer rounds |
| Interview completeness threshold | 70% | per area | Below this, gaps become expensive downstream |
| Triad index max rows | 25 | entries | Buffer growth limit |
| Stale entry age | 30 | days | Remove unconfirmed Seen: 1 entries |
| Promotion threshold | Seen ≥ 3 | observations | Pattern confirmed across 3+ sessions |
| Quick-ref max entries | 7 | entries | Minimal context cost at session start |
| Similarity pre-filter | 3+ | shared words | Mechanical heuristic for Near match detection |
| Audit wave auditors | 3 | parallel | Minimum for holistic coverage |
| Validator batch: template | 5 | tasks/call | Batch efficiency without context loss |
| Validator batch: reality | 3 | tasks/call | Reality checks need more context per item |

---

## Appendix: Glossary

| Term | Definition |
|------|-----------|
| **Gate** | A hard stop between stages requiring explicit human approval before proceeding |
| **Wave** | A group of tasks with no mutual dependencies, executed in parallel |
| **Triad** | A pattern expressed as Trigger → Action → Goal |
| **Seen counter** | Number of times a pattern has been independently observed |
| **Promotion** | Moving a confirmed pattern (Seen ≥ 3) from transit buffer to permanent instructions |
| **Escalation** | Routing an unresolvable issue to the human operator after max attempts |
| **Checkpoint** | A saved state enabling resume after breaks or context loss |
| **Capacity budget** | Maximum effort allowed per session before mandatory break |
| **Skill** | A reusable methodology (WHAT to do) that can be loaded by agents |
| **Agent** | An isolated worker process (WHO does it) that executes tasks and returns structured output |
| **Transit buffer** | Temporary storage for unconfirmed patterns awaiting promotion or pruning |
| **Copy-first** | Template pattern: copy whole template, then edit sections in place |
| **Frontmatter** | YAML metadata at the top of an artifact file for status tracking |
| **Decision log** | Append-only record of decisions, deviations, and outcomes during execution |
| **Audit wave** | A dedicated wave where auditors review all outputs holistically (not diffs) |
| **Signal gate** | A fast binary check that determines whether analysis is worth performing |
