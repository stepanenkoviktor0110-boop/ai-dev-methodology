---
name: tech-spec-planning
description: |
  Creates tech-spec.md with architecture, decisions, testing strategy, and implementation plan.

  Use when: "сделай техспек", "составь техспек", "техническая спецификация",
  "tech spec", "создай тз", "составь тз", "new-tech-spec", "/new-tech-spec"

  Requires existing user-spec.md as input (create with user-spec-planning skill first if missing).
---

# Tech Spec Planning

> **Stop after each artifact.** Produce one artifact, then list its controversial points, explain them simply, and wait for the user's decision before starting the next one.

Create technical specification through code research, adaptive clarification, and multi-validator review.

**Input:** `work/{feature}/user-spec.md` + Project Knowledge
**Output:** `work/{feature}/tech-spec.md` (approved)
**Language:** Technical documentation in English, communication in Russian

Before starting, read [quick-ref-tech-spec-planning.md](../quick-learning/references/quick-ref-tech-spec-planning.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Load Context

1. Ask user for feature name if not provided. Check `work/{feature}/` exists, create if needed.
2. Read `work/{feature}/user-spec.md`. Missing → ask user to describe task or create user-spec first. Extract `size: S|M|L` from frontmatter.
3. Read all files in `.claude/skills/project-knowledge/references/` (missing files are fine).
4. user-spec.md is the single input source — interview.yml and code research are already consolidated there.

## Phase 2: Code Research

Launch `code-researcher` subagent with feature path and user-spec path. It reads existing `code-research.md` (from user-spec phase) and deepens for implementation.

After completion — read `{feature_path}/code-research.md`. If gap discovered later — re-launch with specific question.

## Phase 3: Clarification (Adaptive)

**Think before designing.**
Before writing any architecture, list every assumption you are making about the system — explicitly, as a numbered list. Ask the user about each assumption that user-spec or code research does not confirm. When several architectural interpretations fit, present them all and let the user pick, rather than choosing silently. When something stays unclear, stop and name it before proceeding.

Analyze if additional information is needed based on user-spec and code research.
- Ask technical questions if gaps exist (no limit on count). Focus: constraints, integration points, data sources, external deps.
- Gaps in user-spec requirements → discuss with user and update user-spec too.
- Fundamentally unclear → suggest creating user-spec first.

## Phase 3.5: Stack Research Gate (deep)

Before writing Architecture / Decisions / Shared Resources in Phase 4, collect every stack element that will be used or touched: external APIs, third-party services, new libraries not already covered in the existing `stack-research.md` registry, and libraries whose usage pattern differs from what's documented there.

Classify each candidate:

**Critical** (BLOCK — must be researched at `depth=deep`):
- External APIs (AI, payments, messaging, data providers)
- External services (deploy platforms, auth providers, queues)
- Libraries NOT in the whitelist (`~/.claude/skills/stack-research/references/stable-libraries-whitelist.md`)
- Library with major version < 1.0
- Niche tools (Paged.js, remark/rehype plugins, MCP servers, etc.)
- Any element where the tech-spec will rely on specific endpoints, rate limits, auth flow, or edge-case behavior

**Familiar** (PROMPT — may skip):
- Whitelisted libraries used in a standard way

**Action by class:**

- **Critical candidates present** → STOP. Output:
  > "Перед формулировкой архитектуры и решений требуется deep-ресёрч критичных элементов: [candidate list]. Вызови `/stack-research` с параметрами:
  > - decision_context: {one-sentence, what this tech-spec uses the element for}
  > - candidates: [list with type]
  > - depth: deep
  > - project_context: {2-3 sentences including user-spec constraints}
  > - feature_path: {work/{feature}}
  >
  > Скажи 'продолжаем' после завершения — прочитаю отчёты и продолжу."
  >
  > Do not write Architecture / Decisions / Shared Resources sections for critical candidates without a fresh deep entry in `stack-research.md` or a report under `{feature_path}/logs/stack-research/`.

- **Only familiar candidates** → Output:
  > "Новые/изменённые элементы стека — только из whitelist: [list]. Deep-ресёрч опционален: `/stack-research`. Вызывать? (да / пропускаем)"
  >
  > Wait for answer. Proceed either way.

After the gate passes, read the fresh report(s) and the registry. In Phase 4, when writing Decisions, cite report paths as the source of non-trivial technical claims. Do NOT mix memory-based claims with researched facts.

## Phase 4: Create tech-spec

**Simplicity first.**
Design the minimum architecture that solves today's problem. Include a component when user-spec requires it; leave out anything added "for future flexibility". Introduce an abstraction once at least 2 concrete use cases in this spec need it. Before adding any architectural element ask: "Is this required by user-spec, or am I speculating?" — add it only on the first answer. A spec that grows beyond 15 tasks reads as overengineering rather than scope: propose an MVP split before continuing.

1. Copy template and edit sections one by one:
   ```bash
   cp ~/.claude/shared/work-templates/tech-spec.md.template work/{feature}/tech-spec.md
   ```

2. Fill frontmatter: `created` (today), `status: draft`, `size` (from user-spec), `branch`: `dev` (simple) or `feature/{name}` (multi-component).

3. Fill all template sections. Architecture → Shared Resources: list heavy resources (ML models, DB pools, API clients) with owner, consumers, instance count.

4. Fill Implementation Tasks by waves. For each task: Description (2-3 sentences, WHAT+WHY not HOW), Skill, Reviewers, Verify-smoke (optional), Verify-user (optional), Files to modify, Files to read. Select skill and reviewers from [skills-and-reviewers.md](references/skills-and-reviewers.md).

   `Verify-smoke:` — when task involves external API, library init, Docker/infra, LLM/prompt, MCP-verifiable UI. Write concrete command + expected response.
   `Verify-user:` — when user should check UI/behavior on localhost.
   Omit both if purely internal logic covered by unit tests.

   **Task brevity:** tasks are brief scope descriptions. Detailed steps, AC, TDD anchors, `estimated_loc` come from task-decomposition phase. All technical decisions belong in Decisions section, not tasks.

5. Last two waves always **Audit Wave** + **Final Wave**:

   **Audit Wave** — 3 parallel tasks, `reviewers: none`:
   - Code Audit (`code-reviewing`), Security Audit (`security-auditor`), Test Audit (`test-master`)
   Auditors read all feature files, write reports. Issues found → feature-execution spawns fixer.

   **Final Wave:**
   - QA (`pre-deploy-qa`) — mandatory. Acceptance testing against user-spec + tech-spec.
   - Deploy (`deploy-pipeline`) — if needed.
   - Post-deploy verification (`post-deploy-qa`) — if live-environment checks needed.

6. >15 tasks → propose splitting into MVP + Extension. Wait for user decision.

7. Git commit: `draft(techspec): create tech-spec for {feature}`

## Phase 5: Validation

### Run 5 validators in parallel

Each writes JSON report to `logs/techspec/{name}-review.json`:

| Validator | Agent | Checks |
|-----------|-------|--------|
| Mirage detector | `skeptic` | Non-existent files, APIs, functions, dependencies |
| Completeness | `completeness-validator` | Traceability, scope creep, over/underengineering |
| Security | `security-auditor` | OWASP, input validation, auth, sensitive data |
| Testing strategy | `test-reviewer` | Test plan adequacy for size S/M/L |
| Template + waves | `tech-spec-validator` | Sections, frontmatter, skills/reviewers, wave conflicts |

Pass to each: `work/{feature}/tech-spec.md` + `work/{feature}/user-spec.md`.

### Process findings

Read all 5 reports. Fix if valid, reject with reasoning if disagree, discuss with user if controversial.

After fixes → commit `chore(techspec): validation round {N} — {summary}` → re-run the validators that raised findings, while each round leaves strictly fewer open findings than the one before. The first round that does not reduce them, escalate to the user.

## Phase 6: User Approval

1. Show tech-spec.md + validation summary (iterations, issues resolved).
2. Wait for explicit approval. Comments → fix, re-validate, show again.
3. Set `status: approved`, commit `chore(techspec): approve tech-spec for {feature}`.
4. Suggest `/decompose-tech-spec` as next step.

## Promoted Patterns

- **Verify the target files before describing the operation** (Seen: 2): when a spec says "remove X from N files" or "replace Y", grep every one of them before fixing the operation type. A file that does not contain X needs an add, not a replace.
- **Verify API response shapes with a live call** (Seen: 2): before carrying response shapes from code-research into the spec, make a live API call and copy over every status code, the format and the edge cases. One call is cheaper than a mirage travelling through the whole pipeline. The same applies to a shape inherited from someone's verbal description (counts, format, schema, retention): get ONE live sample from the source before fixing claims in the user-spec or tech-spec — an informant remembers UI behaviour, not the shape of a data dump, and abstractions then get built for variability that may not exist (spec-shape inheritance bias, triad #377).
- **Verify file paths and call sites with ls/grep** (Seen: 2): paths in a tech-spec come from ls/glob, never from memory or docs. Before writing "call sites of function X in file Y", let grep confirm the calls exist.

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during spec planning.
