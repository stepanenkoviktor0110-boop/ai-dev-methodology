---
name: tech-spec-planning
description: |
  Creates tech-spec.md with architecture, decisions, testing strategy, and implementation plan.

  Use when: "сделай техспек", "составь техспек", "техническая спецификация",
  "tech spec", "создай тз", "составь тз", "new-tech-spec", "/new-tech-spec"

  Requires existing user-spec.md as input (create with user-spec-planning skill first if missing).
---

# Tech Spec Planning

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Create technical specification through code research, adaptive clarification, and multi-validator review.

**Input:** `work/{feature}/user-spec.md` + Project Knowledge
**Output:** `work/{feature}/tech-spec.md` (approved)
**Language:** Technical documentation in English, communication in Russian

Before starting, read [quick-ref-tech-spec-planning.md](../quick-learning/references/quick-ref-tech-spec-planning.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Load Context

1. Ask user for feature name if not provided. Check `work/{feature}/` exists, create if needed.

2. Read `work/{feature}/user-spec.md`. If missing — ask user to describe the task or create user-spec first.
   Extract `size: S|M|L` from user-spec frontmatter — it determines testing strategy depth in tech-spec.

3. Read all files in `.claude/skills/project-knowledge/references/` (project.md, architecture.md, patterns.md, deployment.md, ux-guidelines.md, and any custom domain files). Missing files are fine — not all projects have all guides.

4. user-spec.md is the single input source — all information from interview.yml and code research is already consolidated there.

**Checkpoint:**
- [ ] Feature folder exists
- [ ] user-spec.md read, size extracted
- [ ] Project Knowledge read

## Phase 2: Code Research

Launch `code-researcher` subagent (Task tool, opus) with feature path and user-spec path. The agent reads existing `code-research.md` (from user-spec phase if available) and deepens analysis for implementation.

After subagent completes — read `{feature_path}/code-research.md`. Use in Phase 3 clarification and Phase 4 spec writing.

If during later phases a gap is discovered — launch `code-researcher` again with the specific question.

**Checkpoint:**
- [ ] code-research.md created/updated with implementation-level analysis
- [ ] Research file read by orchestrator

**PROMOTED PATTERN:** При интеграции с внешним API — перенести в спек ВСЕ коды ответа, формат данных (JSON/XML/plain text), и edge cases. Перед включением response shapes из code-research — сделать live API call для проверки. Один вызов дешевле propagation миража через весь pipeline.

**PROMOTED PATTERN:** Перед написанием файловых путей в tech-spec — верифицировать через ls/glob, не из памяти или architecture docs. Docs описывают намерение, а не реальность файловой системы. Особенно: пути к shared-ресурсам, шаблонам, скриптам — они часто лежат не там, где написано в docs.

## Phase 3: Clarification (Adaptive)

Analyze if additional information is needed based on user-spec and code research.

- Ask technical questions if gaps exist. No limit on question count — ask as many as needed.
- Focus: technical constraints, integration points, data sources, external dependencies.
- If gaps found in user-spec requirements — discuss with user and update user-spec too (via subagent or directly).
- If requirements are fundamentally unclear — suggest creating user-spec first.

**Checkpoint:**
- [ ] All technical gaps clarified (or none existed)

## Phase 4: Create tech-spec

1. Copy template to feature folder:
   ```bash
   cp ~/.claude/shared/work-templates/tech-spec.md.template work/{feature}/tech-spec.md
   ```
   Then edit sections one by one using Edit tool. This keeps template structure and examples visible while you work.

2. Fill frontmatter:
   - `created`: today's date
   - `status`: draft
   - `size`: copy from user-spec (S|M|L)
   - `branch`: `dev` (simple change, single component) or `feature/{name}` (multiple components, architectural changes)

3. Fill all template sections. The template defines section structure — follow it directly.
   In Architecture → Shared Resources: list heavy resources (ML models, DB pools, browser instances, API clients) shared across components. Specify owner (who creates), consumers, instance count. If none — write "None".

4. Fill Implementation Tasks by waves. For each task provide: Description, Skill, Reviewers, Verify-smoke (optional), Verify-user (optional), Files to modify, Files to read. Select skill and reviewers from [skills-and-reviewers.md](references/skills-and-reviewers.md) (execution skills catalog, reviewer agents, default mappings).

   For each task, write `Verify-smoke:` when the task involves:
   - External API integration → curl/httpie command to real endpoint with expected response
   - Library/model initialization → `python -c` or import check that verifies setup
   - Docker/infrastructure → `docker compose build`, `docker run` commands
   - LLM/prompt work → spawn agent with prompt + test question, check response
   - External service API (OpenRouter, Stripe, etc.) → test API call with expected response
   - MCP-verifiable UI/frontend → use Playwright MCP or similar to check rendered page
   Write `Verify-user:` when user should check something: UI on localhost, behavior, UX.
   Omit both if task is purely internal logic covered by unit tests.

   **Task brevity rules:**
   - Tasks are brief scope descriptions (2-3 sentences). Detailed steps, AC, TDD anchors, and `estimated_loc` are created during task-decomposition phase (Phase 0 estimates LOC, task-creator carries it to task files).
   - Task Description answers WHAT and WHY, not HOW. No step-by-step instructions, no line numbers, no implementation details.
   - All technical decisions belong in the Decisions section, not in task descriptions. If you're writing a decision rationale inside a task — move it to Decisions.

5. The last two waves are always **Audit Wave** and **Final Wave**, in that order:

   **Audit Wave** (always present) — 3 tasks running in parallel, `reviewers: none`:
   - **Code Audit** (skill: `code-reviewing`) — holistic code quality review of all feature code
   - **Security Audit** (skill: `security-auditor`) — OWASP Top 10 across all components
   - **Test Audit** (skill: `test-master`) — test quality and coverage across all components

   Auditors read all source files from the feature and write reports (analysis only). If issues found — feature-execution lead spawns a fixer agent, auditors become reviewers for the fix.

   **Final Wave:**
   - **QA** (skill: `pre-deploy-qa`) — always present. Acceptance testing: run all tests, verify acceptance criteria from user-spec and tech-spec.
   - **Deploy** (skill: `deploy-pipeline`) — only if deploy is needed for this feature.
   - **Post-deploy verification** (skill: `post-deploy-qa`) — only if live-environment checks are needed (MCP tools listed in Agent Verification Plan → Tools required).
   QA is mandatory. Deploy and post-deploy — if applicable.

6. Task Count Check: if >15 tasks — propose splitting into MVP + Extension phases. Wait for user decision.

7. Git commit: `draft(techspec): create tech-spec for {feature}`

**Checkpoint:**
- [ ] tech-spec.md created in work/{feature}/ with all sections
- [ ] Implementation Tasks include Description (2-3 sentences), skill, reviewers for each task
- [ ] No AC or TDD anchors in tasks (those come from task-decomposition phase)
- [ ] Technical decisions are in Decisions section, not in task descriptions
- [ ] Final Wave present with QA (mandatory) + Deploy/Post-deploy (if applicable)
- [ ] Task count ≤15 (or user approved larger scope)

## Phase 5: Validation

### Run 5 validators in parallel

Launch all as subagents, each writes JSON report to `logs/techspec/{name}-review.json`:

| Validator | Agent | Checks |
|-----------|-------|--------|
| Mirage detector | `skeptic` | Non-existent files, APIs, functions, dependencies |
| Completeness + adequacy | `completeness-validator` | Bidirectional traceability, scope creep, overengineering, underengineering, solution depth |
| Security | `security-auditor` | OWASP, input validation, auth, sensitive data |
| Testing strategy | `test-reviewer` | Test plan adequacy for feature size S/M/L |
| Template + wave conflicts | `tech-spec-validator` | All sections filled, frontmatter, format, skills/reviewers, wave conflict detection |

Pass to each validator: `work/{feature}/tech-spec.md` + `work/{feature}/user-spec.md`.

### Process findings

Read all 5 reports. For each finding:
- Fix if clearly valid
- Reject with reasoning if disagree
- Discuss with user if controversial

### Iterate if needed (up to 3 iterations)

If fixes were made:
1. Apply targeted fixes directly in `work/{feature}/tech-spec.md`.
2. Git commit: `chore(techspec): validation round {N} — {summary of fixes}`
3. Re-run validators on updated tech-spec.
4. Repeat up to 3 iterations.

If problems remain after 3 iterations — show user: "Validation didn't pass in 3 iterations. Here's what remains — let's resolve together."

**Checkpoint:**
- [ ] All 5 validators ran
- [ ] Findings processed (fixed / rejected / discussed)
- [ ] Final tech-spec.md placed in work/{feature}/

## Phase 6: User Approval

1. Show user the full tech-spec.md.
2. Show validation summary: iterations count, issues found and resolved.
3. Wait for explicit approval.
4. If user has comments — fix, re-validate, show again.
5. After approval: update `status: draft` → `status: approved` in tech-spec frontmatter.
6. Git commit: `chore(techspec): approve tech-spec for {feature}`
7. Tell user next step: run `/decompose-tech-spec` to create task files.

**Checkpoint:**
- [ ] User explicitly approved tech-spec
- [ ] status = approved

## Final Check

- [ ] tech-spec.md created with all sections (Implementation Tasks are brief scope descriptions)
- [ ] Validation passed (5 validators)
- [ ] User approved tech-spec
- [ ] status = approved in frontmatter

## Promoted Patterns

**Верифицируй целевые файлы перед описанием операции (Seen: 2):** Когда spec описывает трансформацию "удалить X из N файлов" или "заменить Y" — grep по каждому файлу перед тем как зафиксировать тип операции. Файл без X требует add, не replace. Ошибка типа операции обнаруживается только при выполнении задачи.

## Learned Patterns

- When adding auth flow to imported data -> verify credentials existence AND isActive flag explicitly in the integration spec, to avoid missing auth discovered at user verification
- When an external service returns an unexpected result during research -> run escalating diagnostics (parameters -> curl -> re-read docs) before declaring a blocker
- When output format requirements arrive iteratively -> agree on complete output structure with a mockup before writing code, to avoid rewriting implementation on each clarification
- When an external system returns empty results -> enumerate and check all available channels/endpoints before concluding data is absent
- When speccing a complex project with server-side actions -> include performance timing baseline in the MVP scope to detect degradation before it reaches production
- When diagnosing performance problems on a low-traffic server -> check default timeout/connection pool/cache limits in configuration before optimizing code
- When planning file sync between two repo versions -> launch code-research to classify diff depth before writing scope, to avoid describing a mechanical sync that requires manual review
- When a feature combines client-only storage with server-side automation -> verify data-access layer compatibility before making architecture decisions, to avoid a storage-layer conflict mid-spec
- When spec narrows a criterion discussed in the interview (A or B -> only A) -> add to Technical Decisions: decided NOT to include B, because... to avoid extra validation rounds
- When adding a metric to a dashboard without explicit time horizon -> clarify with user: launch / daily / all-time, before writing spec
- When proposing hosting/stack for a new project -> clarify deployment region and regulatory constraints BEFORE proposing solutions, to avoid rewriting the architectural stack after discussion
- When completing the Implementation Tasks section -> check for Files-to-modify overlap within each wave, to prevent merge conflicts during parallel execution
- When designing a feature with user file uploads to disk -> explicitly describe the file delivery mechanism (protected API, not static) in Architecture, to prevent IDOR through unauthorized direct file access
- When a feature reads methodology files via GitHub Contents API -> verify whether those files are committed in the target repositories BEFORE writing AC, to avoid data unavailable for all projects due to .gitignore
- When writing curl commands in AVP for authenticated endpoints -> include auth header AND add a test without-key -> 401 to avoid false QA pass with broken authorization
- When config contains a whitelist/filter for limiting processing -> clarify at which pipeline stage the filter is applied and move it before the resource-intensive operation
- When asked to remove X from repository -> clarify: git untrack only (git rm --cached + .gitignore) or physical deletion from disk, to avoid destroying local files with a git operation
- When needing to obtain configuration from a provider (DNS, settings) -> ask the client first whether they have access to the provider's control panel, to avoid waiting for support response when the client can get the data themselves
- When a tech-spec decision narrows or defers a requirement from user-spec -> check whether that requirement appears in the user-spec AC BEFORE writing the Decision, to avoid introducing scope reduction without explicit user agreement
- When a user rejects a proposed architectural simplification -> ask 'what distinction is lost by the simplification?' before continuing, to surface the missing key abstraction before implementation (triad #137)
