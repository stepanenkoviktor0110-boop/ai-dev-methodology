---
name: user-spec-planning
description: |
  Creates user-spec.md through adaptive interview with codebase scanning and dual validation.

  Use when: "сделай юзер спек", "проведи интервью для юзер спека",
  "создай юзерспек", "user spec", "detailed planning", "хочу продумать фичу",
  "опиши требования к фиче", "сделай описание фичи", "/new-user-spec"

  For tech planning use tech-spec-planning. For project planning use project-planning.
---

# User Spec Planning

Thorough adaptive interview → codebase scan → user-spec.md → dual validation → user approval.
Output: `work/{feature}/user-spec.md` with status `approved`.

## Interview Style

Conduct in Russian. Be an engaged co-thinker — propose solutions from Project Knowledge, challenge with concrete counterexamples and code references.

- 3-4 questions per batch, as many batches as needed until cycle items fully covered
- Challenge with substance once, accept answer, move on. "Не знаю" → help think through (examples, patterns); optional → TBD, required → simpler questions
- Depth by size: **S** (1-3 files) → focused, core behavior; **M** (several components) → moderate, integration; **L** (new architecture) → deep, edge cases + risks

## Process

### Phase 0: Init

0. **Sketch offer:** "Хочешь начать со скетча? `/sketch` — быстрый прототип за 3-5 вопросов, без спеков и валидаторов." If declined → proceed.
1. Check for existing interview in `work/*/logs/userspec/interview.yml` (status: in_progress). Found → load, show summary, resume.
2. Get task description, determine work_type (feature/bug/refactoring), propose feature name (kebab-case).
3. Run `~/.claude/shared/scripts/init-feature-folder.sh {name}`, update interview.yml: metadata + phase1_feature_overview.

### Phase 1: Study Project Knowledge

Read [quick-ref-user-spec-planning.md](../quick-learning/references/quick-ref-user-spec-planning.md) (if exists).
Read ALL files from `.claude/skills/project-knowledge/references/`. Missing → warn, suggest project-planning skill.

### Phase 2: Cycle 1 — General Understanding

**Scope:** `phase1_feature_overview` items.

1. Score user's description against all items (detailed 80-95%, brief 50-70%, vague 20-40%, not mentioned 0%).
2. Run interview loop on phase1 items.
3. Determine feature size S/M/L and agree on testing strategy: S → integration/E2E usually not needed; M → propose whether integration fits; L → propose specific integration + E2E scope.

### Phase 3: Code Scanning

Launch `code-researcher` subagent (opus) with feature path and description. After completion — read `{feature_path}/code-research.md`, use in Cycle 2. If gap discovered later — re-launch with specific question.

### Phase 4: Cycle 2 — Code-Informed Refinement

**Scope:** `phase2_user_experience` + `phase3_integration` items.

1. Summarize: "Я понял задачу так: [X]. Делать планирую так: [Y, based on code]."
2. Code-based questions: "Нашёл модуль X, который делает Y — переиспользуем?"
3. Cover deploy + manual actions: what manual steps needed (API keys, bot creation, service setup)? Deploy approach (CI/CD, manual)? Post-deploy verification (MCP, curl, manual)? Pre-deploy checks (local API calls, localhost UI, config validation)?
4. Run interview loop on phase2 + phase3 items.

### Phase 5: Cycle 3 — Review & Finalize

**Scope:** ALL items still below threshold. Cleanup pass — revisit gaps, deepen edge cases and error scenarios. Run interview loop.

### Phase 6: Completeness Check

Launch `interview-completeness-checker` subagent (sonnet) with feature path. `needs_more` → ask suggested questions, re-run. `complete` → proceed.

### Phase 7: Create User Spec

1. Copy `~/.claude/shared/work-templates/user-spec.md.template` → `work/{feature}/user-spec.md`. Edit sections one by one via Edit tool (agent sees template comments while editing).
2. Rules: "Что делаем" self-contained; "Зачем" = concrete value; AC testable (no "работает корректно"); every discussed topic appears.
3. Large feature (>10 criteria, >3 flows, >5 integrations) → suggest splitting.

Git commit: `draft(userspec): create user-spec for {feature}`

### Phase 8: Validation

Run 2 validators in parallel: `userspec-quality-validator` (sonnet) — structure, template compliance; `userspec-adequacy-validator` (opus) — feasibility, over/underengineering.

Findings: obvious → fix silently; borderline → discuss with user; disagree → reject with reasoning; conflict between validators → adequacy takes priority (substance over form).

After fixes → commit `chore(userspec): validation round {N} — {summary}`. Re-run validators. Max 3 iterations.

### Phase 9: User Approval

Show user-spec.md link + validation summary. When approved:
1. Set user-spec.md frontmatter `status: approved`, interview.yml `metadata.status: completed`
2. Git commit: `chore(userspec): approve user-spec for {feature}`
3. Suggest `/new-tech-spec {feature-name}`

## Interview Loop

Runs inside each cycle until scope fully covered:

1. Find gaps: required items in scope with score < 85%, lowest first
2. Ask 3-4 questions about different gaps (reference PK + code findings)
3. User responds → update interview.yml immediately (conversation_history, item scores/values/gaps, metadata)
4. Stop when BOTH: all required items >= 85% AND every required item has non-empty value, no TBD, gaps empty or only conscious limitations
5. Not done → step 1

Scoring: detailed 80-95%, brief 50-70%, vague 20-40%, not mentioned 0%.
Optional items: cover when user mentions relevant context or naturally connected to required items.

## Work Type Adaptations

All three cycles apply to any work_type, but focus shifts:
- **Bug:** Cycle 1 → reproduction, expected vs actual, severity. Code scan → bug location + root cause. Cycle 2 → fix approach, regression risks.
- **Refactoring:** Cycle 1 → current problems, target architecture, stability guarantees. Code scan → structure, deps, test coverage. Cycle 2 → migration path, backward compatibility.

## Scope Changes

If understanding changes significantly: update scores downward, reassess size S/M/L, pivot items if work_type changed, note in interview.yml.

## Self-Verification

- [ ] All cycles completed, completeness checker passed
- [ ] user-spec.md filled (no placeholders), both validators passed or issues resolved
- [ ] User approved, frontmatter status: approved, interview.yml completed
- [ ] Suggested `/new-tech-spec` as next step

## Promoted Patterns

- **Генерируй все шаги deliverable целиком** (Seen: 3): Когда deliverable состоит из нескольких шагов (серия промптов, roadmap, план сессий, деплой-инструкция) — генерировать ВСЕ шаги сразу. Частичный deliverable заставляет пользователя ловить недостающие части и запрашивать доработку.

## Learned Patterns

- When writing client-facing documentation on behalf of the user -> filter every paragraph through the reader's knowledge model to avoid iterative corrections
- When user spec grows to 3+ sequentially-dependent deliverables -> keep the first active, create the rest as planned stubs with visible progress and preserved post-feature context
- When the repo contains skills/modules from multiple domains -> enumerate all domains and get is_in_scope per domain before writing spec, to avoid rewriting scope from iterative boundary clarification
- When user-spec has a descriptive block with a requirement not reflected in AC -> follow only the AC; document the gap with a decision record and update user-spec
- When user adds a non-trivial feature mid-interview -> ask a scope-impact question before updating the spec, to prevent expanding v1 to an architecture of a different complexity level
- When user-spec describes delete/cleanup in a system with pipeline statuses -> restrict deletion to terminal statuses (enriched/done), not field values, to avoid deleting records still in processing
- When a new role appears mid-interview -> immediately build a role x capabilities matrix and validate with the user, to avoid 3+ batches clarifying role intersections
- When user describes several interrelated features to implement -> explicitly clarify implementation order BEFORE initializing the first feature folder
- When a client sends amendments to an approved user-spec -> run a focused mini-interview on changed points only and update spec directly, to avoid restarting the full interview cycle
- When clarifying UI element placement during a spec interview -> choose a standard UX pattern without asking, to avoid blocking the interview on details the user does not formulate
- When updating user-spec for an already-implemented feature -> launch code-researcher to diff new requirements against existing code, to avoid creating tasks for already-implemented functionality
- When a feature generates a list of items where each item has a numeric attribute (price, score, rating) -> explicitly ask during interview who/what sets that value (LLM estimate, user catalog, or manual input) before writing AC, to prevent a critical architectural gap discovered only at validation
- When a user rejects a proposed simplification during interview -> ask "what distinction is lost by simplifying?" before continuing, to surface a missing key abstraction before the spec is finalized
- When spec describes a CRUD form for a single entity but the target workflow is an action over a group -> clarify cardinality ("one or many?") before implementation, to avoid rewriting finished UI due to UX mismatch
- When user describes "split UI area into X and Y" -> clarify whether existing interaction elements survive in the new layout, to avoid treating an additive change as a replacement
- When user-spec describes instant-save operations (click → write to DB) -> explicitly add AC for network error and rollback before validation, to avoid missing critical negative scenarios in round 1
- When a UI task adds visible disabled buttons as placeholders for a future task -> do not add visible disabled placeholders until the future task is confirmed, to prevent reactive feature reversal after user verification
- When user-spec is for a feature completing an existing sketch/stub with real API routes -> during code scanning read all API implementations (role checks, data filtering) and include found bugs in AC as explicit fix-requirements, to avoid critical/major security and correctness findings from validators that could have been caught earlier
- When the task adapts existing UI (responsive, a11y) without creating new visuals -> note in spec that design-plan can be skipped and go from design-spec directly to tech-spec, to not block on absent tokens.json or design system
- When parallel task-creators will reference the same external utility or approach -> explicitly capture the chosen approach as a Decision in user-spec before decomposition, to prevent contradictory instructions across tasks
- When MVP plan contains only modules without a runnable entry point or start script -> verify during spec writing that the plan includes a runnable entry point and npm start, so the user can launch and verify the result without developer help
- When user-spec explicitly excludes a capability in post-MVP -> before adding an analogous capability as a Decision check the exclusions list in user-spec, to prevent scope creep caught only at validation
- When a task creates a UI component -> include entry point integration (import and render in App/page) in the spec's implementation notes, to not leave downstream tasks with a wrong assumption that the component is already wired in
- When user-spec is for a style-only refactoring with full audit -> skip heavy validators or limit to lightweight validation, to not lose hours on stuck agents when architectural risk is zero
- When пользователь описывает фичу знакомым термином (демо, шаблон, виджет) → спросить «кто потребитель и зачем ему это?» до технических деталей, to не потратить 3 батча интервью на выяснение реальной потребности.
