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

Launch `code-researcher` subagent with feature path and description. After completion — read `{feature_path}/code-research.md`, use in Cycle 2. If gap discovered later — re-launch with specific question.

### Phase 4: Cycle 2 — Code-Informed Refinement

**Scope:** `phase2_user_experience` + `phase3_integration` items.

1. Summarize: "Я понял задачу так: [X]. Делать планирую так: [Y, based on code]."
2. Code-based questions: "Нашёл модуль X, который делает Y — переиспользуем?"
3. Cover deploy + manual actions: what manual steps needed (API keys, bot creation, service setup)? Deploy approach (CI/CD, manual)? Post-deploy verification (MCP, curl, manual)? Pre-deploy checks (local API calls, localhost UI, config validation)?
4. Run interview loop on phase2 + phase3 items.

### Phase 5: Cycle 3 — Review & Finalize

**Scope:** ALL items still below threshold. Cleanup pass — revisit gaps, deepen edge cases and error scenarios. Run interview loop.

### Phase 6: Completeness Check

Launch `interview-completeness-checker` subagent with feature path. `needs_more` → ask suggested questions, re-run. `complete` → proceed.

### Phase 7: Create User Spec

1. Copy `~/.claude/shared/work-templates/user-spec.md.template` → `work/{feature}/user-spec.md`. Edit sections one by one via Edit tool (agent sees template comments while editing).
2. Rules: "Что делаем" self-contained; "Зачем" = concrete value; AC testable (no "работает корректно"); every discussed topic appears.
3. Large feature (>10 criteria, >3 flows, >5 integrations) → suggest splitting.

Git commit: `draft(userspec): create user-spec for {feature}`

### Phase 8: Validation

Run 2 validators in parallel: `userspec-quality-validator` — structure, template compliance; `userspec-adequacy-validator` — feasibility, over/underengineering.

Findings: obvious → fix silently; borderline → discuss with user; disagree → reject with reasoning; conflict between validators → adequacy takes priority (substance over form).

After fixes → commit `chore(userspec): validation round {N} — {summary}`. Re-run the validators that raised findings, while each round leaves strictly fewer open findings than the one before. The first round that does not reduce them, stop and bring what remains to the user.

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

Optional items: cover when user mentions relevant context or naturally connected to required items.

## Work Type Adaptations

All three cycles apply to any work_type, but focus shifts:
- **Bug:** Cycle 1 → reproduction, expected vs actual, severity. Code scan → bug location + root cause. Cycle 2 → fix approach, regression risks.
- **Refactoring:** Cycle 1 → current problems, target architecture, stability guarantees. Code scan → structure, deps, test coverage. Cycle 2 → migration path, backward compatibility.

## Scope Changes

If understanding changes significantly: update scores downward, reassess size S/M/L, pivot items if work_type changed, note in interview.yml.


## Checks against state

```bash
# 1. the spec exists and reached approved status
rg -n "^status:" work/{feature}/user-spec.md

# 2. no placeholder survived into the approved spec
rg -n "TBD|\{[a-z_]+\}|\[заполнить\]" work/{feature}/user-spec.md

# 3. the interview record was closed, not abandoned mid-cycle
rg -n "status:" work/{feature}/logs/userspec/interview.yml

# 4. approval was committed
git log --oneline -5 --grep "userspec"
```

Check 2 must return nothing. A placeholder left in an approved spec becomes a task written
against a blank.

## Promoted Patterns

- **Generate every step of a deliverable at once** (Seen: 3): when a deliverable consists of several steps — a series of prompts, a roadmap, a session plan, deploy instructions — generate ALL of them in one pass. A partial deliverable forces the owner to notice what is missing and ask for the rest.

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during an interview.
