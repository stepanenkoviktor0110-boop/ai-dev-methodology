---
name: design-plan-planning
description: |
  Autonomously creates design-plan.md with layout decisions, responsive strategy,
  and visual hierarchy for each screen. Takes design-spec.md + tokens.json as input,
  cross-references layout patterns and style profiles, produces a complete plan
  without asking user about CSS techniques or layout choices.

  Use when: "design plan", "план дизайна", "спланируй дизайн", "layout planning",
  "визуальные решения", "design-plan-planning"
---

# Design Plan Planning

Create a design plan that maps every screen from design-spec.md to a specific layout pattern,
responsive strategy, and visual hierarchy. All visual decisions are autonomous — the user
only approves or corrects the final plan.

**Input:** `work/{feature}/design-spec.md` (approved) + `.design-system/tokens.json` + optional taste-profile
**Output:** `work/{feature}/design-plan.md` (from template, approved)

## Phase 0: Load Context

1. **Read design-spec.md** at `work/{feature}/design-spec.md`.
   - If file is missing → stop: "design-spec.md not found. Run `/design-spec` first."
   - Check frontmatter contains `status: approved`. If status is not approved → stop: "design-spec.md is not approved. Get approval first."
   - Verify required sections are present (Screens section with at least one screen entry). If sections are missing or content is empty/garbled → stop: "design-spec.md appears corrupted or malformed. Re-run `/design-spec`."

2. **Read tokens.json** at `.design-system/tokens.json`.
   - If file is missing → stop: "Design system not found. Run `/design-system-init` first."
   - Parse as JSON. If parsing fails → stop: "tokens.json is corrupted. Run `/design-system-init` to recreate."
   - Extract: color palette, typography tokens, spacing scale, breakpoints (if defined).

3. **Read taste-profile.md** at `.design-system/taste-profile.md` (optional).
   - If file exists and is not empty → extract preferences: boldness level (conservative / balanced / bold / experimental), color temperature, typography style, anti-patterns (rejected approaches from past sessions).
   - If file is missing or empty → continue without it. This is normal for first sessions.

4. **Load style profile by mood.** Determine mood from taste-profile or tokens.json (look for mood/style keywords). Match mood against the Quick Lookup table in style-profiles.md — use the "Mood" column to find the closest match. Load only the matched section (Luxury, Brutalist, Editorial, Minimal, Playful, Corporate, Neo-Retro). If no clear match → default to Minimal.
   Style profiles reference: `~/.claude/shared/design-references/style-profiles.md`

5. **Read layout patterns** from [generation-guide.md](../design-generate/references/generation-guide.md) — the selection table mapping request types to 15 layout patterns (5 basic + 10 advanced). This table drives screen-to-layout matching in Phase 1.

**Checkpoint:**
- [ ] design-spec.md read and validated (exists, approved, sections present)
- [ ] tokens.json read and parsed (valid JSON, tokens extracted)
- [ ] taste-profile read or gracefully skipped
- [ ] Style profile section loaded by mood match
- [ ] Layout selection table loaded from generation-guide.md

## Phase 1: Analyze

1. **Extract screen list** from design-spec.md. For each screen collect:
   - Screen name and type (landing, dashboard, auth, settings, catalog, etc.)
   - Content description (what the screen shows)
   - Priority (primary / secondary / supporting)
   - User flows the screen participates in

2. **Match screens to layout patterns.** Use the selection table from generation-guide.md:
   - Map each screen's type to the recommended pattern (e.g., auth page → Split Screen, dashboard → Sidebar + Content).
   - If a screen type does not match any row exactly → pick the closest match by content structure.

3. **Apply taste-profile influence** (if loaded):
   - conservative / balanced → prefer basic layouts (Single Column, Sidebar+Content, Grid, Hero+Sections, Split Screen)
   - bold / experimental → consider advanced layouts (Broken Grid, Diagonal, Bento, Swiss Grid) where appropriate
   - Anti-patterns → exclude layout patterns the user has rejected before

4. **Identify shared patterns** across screens:
   - Common navigation component (top nav, sidebar nav, breadcrumbs)
   - Shared footer or CTA sections
   - Repeated card/list patterns
   - Color usage consistency (which tokens map to which roles across screens)

**Checkpoint:**
- [ ] All screens extracted with type, content, priority
- [ ] Each screen has a candidate layout pattern
- [ ] Taste-profile preferences applied to layout selection
- [ ] Shared cross-screen patterns identified

## Phase 2: Decide

Decisions are autonomous — explain reasoning in the output, do not ask the user to choose.

1. **Assign layout pattern per screen.** For each screen, finalize one layout from the 15 available patterns. Write a 1-sentence rationale (e.g., "Sidebar+Content chosen for dashboard — dense data with persistent navigation suits this pattern").

2. **Define responsive strategy per screen:**
   - Breakpoint behavior: what stacks, what hides, what reflows
   - Mobile-first or desktop-first approach (decide based on project type from design-spec)
   - Touch target considerations for interactive screens

3. **Establish visual hierarchy per screen:**
   - Primary focus (what the user sees first)
   - Secondary focus (what draws attention next)
   - Tertiary content (supporting information)

4. **Ensure cross-screen consistency:**
   - Navigation pattern is the same across all screens (or intentionally different with rationale)
   - Spacing scale from tokens.json is applied uniformly
   - Color roles are consistent (primary color always means the same thing)
   - Typography hierarchy is coherent across screens (same h1/h2/body sizing)

**Checkpoint:**
- [ ] Every screen has exactly one assigned layout pattern with rationale
- [ ] Responsive strategy defined per screen (breakpoints, stacking, adaptation)
- [ ] Visual hierarchy defined per screen (primary / secondary / tertiary)
- [ ] Cross-screen consistency verified (navigation, spacing, color, typography)

## Phase 3: Create design-plan.md

1. **Copy template** to feature folder:
   ```bash
   cp ~/.claude/shared/work-templates/design-plan.md.template work/{feature}/design-plan.md
   ```

2. **Fill frontmatter** using Edit tool:
   - `created`: today's date
   - `status`: draft
   - `design-spec`: path to the design-spec.md used

3. **Fill Design Strategy section:**
   - Mood & Atmosphere — derived from design-spec mood and taste-profile
   - Style Profile Match — which profile was selected from Quick Lookup and why
   - Visual Approach — dominant colors, typography pairing rationale, spacing philosophy

4. **Fill Screen Plans** — one block per screen:
   - Layout Pattern (from Phase 2 decision)
   - Responsive Strategy (from Phase 2 decision)
   - Visual Hierarchy (primary / secondary / tertiary)
   - Component List (components needed from DS for this screen)
   - Notes (edge cases, animations, loading states, or "None")

5. **Fill Cross-Screen Consistency:**
   - Shared Patterns, Navigation, Color Usage

6. **Fill Responsive Strategy:**
   - Breakpoints (from tokens.json or standard mobile/tablet/desktop)
   - Adaptation Priorities (what content gets hidden/stacked first)
   - Mobile-Specific Decisions (touch targets, font bumps, gestures)

**Checkpoint:**
- [ ] design-plan.md created from template in work/{feature}/
- [ ] All sections filled (no template placeholders remain)
- [ ] Every screen from design-spec.md has a corresponding Screen Plan block
- [ ] Layout patterns reference valid names from generation-guide.md

## Phase 4: User Approval

1. Present the full design-plan.md to the user.

2. Wait for explicit approval. If the user gives corrections ("I want a different layout for the dashboard", "make it bolder"):
   - Apply the correction in design-plan.md
   - Re-present the changed section
   - Wait for approval again

3. After approval:
   - Update `status: draft` → `status: approved` in frontmatter
   - Git commit: `feat(design): approve design-plan for {feature}`

4. Tell user next step: run `/design-generate` to generate pages from this plan.

**Checkpoint:**
- [ ] User explicitly approved the design plan
- [ ] status = approved in frontmatter
- [ ] Plan committed to git

## Final Check

All phase Checkpoints satisfied; design-plan.md committed with `status: approved` and no template placeholders remain.
