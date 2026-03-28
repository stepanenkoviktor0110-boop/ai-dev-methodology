---
name: design-spec-planning
description: |
  Conducts adaptive design interview for non-designers: discovers screens,
  content, user flows, and produces design-spec.md. Propose-first approach
  with category-based screen suggestions.

  Use when: "сделай дизайн спек", "дизайн спецификация", "какие экраны нужны",
  "design spec", "create design spec", "спланируй дизайн", "что дизайнить",
  "design planning", "/design-spec-planning"
---

# Design Spec Planning

Adaptive interview for non-designers → design-spec.md with screens, content, and user flows.
Output: `work/{feature}/design-spec.md` with status `approved`.

## Interview Style

Conduct interview in Russian. Propose-first: suggest typical screens and content for the project category, user confirms or adjusts. Avoid open-ended design jargon questions.

**How to interview:**
- 3-4 questions per batch. Run as many batches as needed until cycle items are covered.
- Propose concrete options: "Для SaaS обычно нужны dashboard, settings, profile — что из этого актуально?"
- Keep questions simple — describe screens by what users do there, not by design terminology.
- Accept the answer after one clarifying follow-up and move on.

## Screen Sets by Category

Use this table to propose initial screen lists in Phase 2. User removes unneeded screens and adds custom ones.

| Category    | Typical Screens                                            |
|-------------|------------------------------------------------------------|
| Landing     | hero, features, pricing, testimonials, contact, footer     |
| Webapp      | login, dashboard, settings, profile, list/table, detail    |
| SaaS        | login, dashboard, settings, profile, billing, analytics    |
| Admin       | dashboard, users, content-management, analytics, settings  |
| Portfolio   | home, projects, project-detail, about, contact             |
| E-commerce  | home, catalog, product, cart, checkout, order-confirmation |

## Process

### Phase 0: Init

1. Check for existing interview: look in `work/*/logs/designspec/interview.yml` for `interview_metadata.status: in_progress`. If found — load, show discussed topics summary, resume from current state.
2. Get project description: "Опиши проект, для которого нужен дизайн."
3. Propose feature name (kebab-case), get user confirmation.
4. Create feature folder if absent: `mkdir -p work/{name}/logs/designspec`.
5. Copy interview template: `~/.claude/shared/interview-templates/design.yml` → `work/{name}/logs/designspec/interview.yml`.
6. Update interview.yml: set `interview_metadata.started`, `interview_metadata.status: in_progress`, `phase1_project_context.project_name.value`.

**Checkpoint:** interview.yml exists with status `in_progress`, feature name confirmed.

### Phase 1: Study Context

1. Read project knowledge from `.claude/skills/project-knowledge/references/` if it exists. These files provide context for the entire interview.
2. Check for `.design-system/tokens.json`:
   - If exists — note "Design system found" for inclusion in design-spec.md DS Status section.
   - If missing — note recommendation: run `/design-system-init` before generating designs.
3. Determine project category from user's description (Landing / Webapp / SaaS / Admin / Portfolio / E-commerce).
4. Read the matching `## {Category}` section from [designer-experience.md](~/.claude/shared/design-references/designer-experience.md) — use accumulated preferences and anti-patterns when formulating proposals. If file is missing or section is empty — continue without it.

**Checkpoint:** Project category determined. Design system status noted. Context loaded.

### Phase 2: Adaptive Interview

Two cycles covering all interview.yml phases.

#### Cycle 1: Project Context

**Scope:** `phase1_project_context` items in interview.yml.

1. Score user's initial description against all items (detailed 80-95%, brief 50-70%, vague 20-40%, not mentioned 0%).
2. Run interview loop on phase1_project_context items.
3. During this cycle — determine design size (S: 1-3 screens, M: 4-8, L: 9+).

#### Cycle 2: Screens, Content, and Flows

**Scope:** `phase2_screens_and_content` + `phase3_user_flows` items.

1. Propose screen set from the Screen Sets table above based on confirmed category. Present as: "Для {category} обычно делают: {screens}. Что убрать? Что добавить?"
2. For each confirmed screen — ask what content belongs there: headings, text blocks, forms, CTAs, data displays. Propose typical content, user adjusts.
3. Ask about the primary user flow: "Пользователь заходит на {entry} — куда идёт дальше? Что делает на каждом экране?"
4. For multi-screen projects — ask about navigation structure (navbar, sidebar, tabs).
5. Run interview loop on phase2 + phase3 items.

If user wants only one screen — skip user flow questions between screens. Focus on content and layout of that single screen.

#### Cycle 3: Cleanup

**Scope:** All items across all phases still below threshold.

Revisit anything not fully covered. Run interview loop on remaining gaps.

### Phase 3: Create design-spec.md

1. Copy template: `~/.claude/shared/work-templates/design-spec.md.template` → `work/{feature}/design-spec.md`.
2. Fill sections using Edit tool, replacing placeholders with interview data:
   - **Project Overview** — description and category from phase1
   - **Target Audience** — from phase1 target_audience
   - **Screens** — table with all confirmed screens, their type, content, and priority
   - **User Flows** — primary and secondary flows from phase3
   - **DS Status** — "exists" or "missing" with `/design-system-init` recommendation
   - **Notes** — additional constraints, preferences, style notes
3. Set frontmatter: `created: {date}`, `status: draft`, `size: {S/M/L}`.

Git commit: `draft(designspec): create design-spec for {feature}`

**Checkpoint:** design-spec.md exists with all sections filled from interview data. No placeholders remain.

### Phase 4: User Approval

1. Show design-spec.md link and brief summary of what was captured.
2. If user requests changes — edit and show again.
3. When approved:
   - Set design-spec.md frontmatter `status: approved`
   - Set interview.yml `interview_metadata.status: completed`, `phase4_completion.status: approved`
   - Git commit: `chore(designspec): approve design-spec for {feature}`
   - Suggest next step: `/design-plan {feature-name}` to create the design execution plan.

**Checkpoint:** design-spec.md status is `approved`. Interview completed.

## Interview Loop

Runs inside each cycle. Repeats until the cycle scope is fully covered.

```
1. Find gaps: required items in current scope with score < 85%. Lowest first.
2. Ask 3-4 questions about different gaps. Propose concrete options.
3. User responds.
4. Update interview.yml:
   - conversation_history: add Q&A entry
   - Item: score, value, gaps, status
   - metadata: last_updated, current_question_num
   - Save immediately
5. Check stop criteria (BOTH must be true):
   a) All required items in scope score >= 85%
   b) Structural: every required item has non-empty value,
      no TBD, gaps empty or conscious limitations only
6. Not done → step 1. Done → exit cycle.
```

Scoring: detailed answer 80-95%, brief 50-70%, vague 20-40%, not mentioned 0%.

Optional items: cover when user mentions relevant context or when naturally connected to required items.

## Self-Verification

Before finishing, verify:
- [ ] All phases (0-4) completed
- [ ] design-spec.md filled with real content (no placeholders, no template markers)
- [ ] Screens table has at least one entry with type, content, and priority
- [ ] User flows section describes at least one complete path (or noted as single-screen project)
- [ ] DS Status section reflects actual `.design-system/tokens.json` presence
- [ ] designer-experience.md was read by project category (or noted as empty/missing)
- [ ] User approved, frontmatter status: approved
- [ ] interview.yml metadata.status: completed
- [ ] Suggested `/design-plan` as next step
