---
name: done
description: |
  Finalize work session: detect documentation drift from git changes,
  show drift items for review, update project knowledge, optionally archive feature.

  Use when: "done", "/done", "проект done", "фича готова", "заверши фичу",
  "финализация", "закрой фичу", "перенеси в completed"
---

# Done — Finalize Session

Closes a work session by detecting what changed in code/config and verifying
that project documentation reflects those changes.

Works in two modes:
- **Feature mode** — if `work/{feature}/` directory exists with specs
- **Session mode** — any work session, no feature directory required

## Step 1: Collect Session Diff

Determine what changed in this session:

```
git log --oneline -20
```

From the log, identify the range of commits made in the current session
(typically: everything after the last `docs:` commit or the last commit
before the session started).

Then collect changed files:
```
git diff --name-only <first-session-commit>^..HEAD
```

**Output:** list of changed files grouped by area:
- Config: `next.config.*`, `ecosystem.config.*`, `.env*`, `nginx/`
- Schema/DB: `shared/db/schema.ts`, `migrations/`
- API routes: `**/api/**`
- Components: `src/containers/`, `src/components/`, `cabinet/src/`
- Deploy: `.github/workflows/`, `Dockerfile`, etc.
- Docs: `.claude/skills/project-knowledge/`

## Step 2: Check if Project Knowledge Exists

If `.claude/skills/project-knowledge/references/` does not exist or is empty:
- Skip documentation check
- Inform user: "Project knowledge not initialized, skipping docs check."
- Jump to Step 6

## Step 3: Detect Documentation Drift

For each PK file, check if session changes affect documented content:

### architecture.md
Drift if session touched:
- `next.config.*` — images config, output mode, transpile
- `shared/db/schema.ts` — data model, table count
- `shared/db/index.ts` — connection pool config
- `src/app/page.tsx` — section rendering, LazySection usage, navigation anchors
- `src/lib/` — data fetching functions
- Component structure changes (new/removed containers)

### deployment.md
Drift if session touched:
- `.github/workflows/` — CI/CD pipeline, secrets, steps
- `ecosystem.config.*` — PM2 config, ports, restart policy
- `nginx/` or server SSH commands were run — nginx config
- `.env*` — environment variables
- New GitHub Secrets added

### patterns.md
Drift if session touched:
- Git workflow changes
- New testing patterns discovered
- Business rules changed

### ux-guidelines.md (if exists)
Drift if session touched:
- Responsive breakpoints, CSS changes
- UI component behavior changes

**For each potential drift item, produce a one-line description:**
```
[architecture.md] images config changed: was formats:webp, now unoptimized:true
[deployment.md] REVALIDATE_SECRET added to env but not documented
[deployment.md] PM2 hardening settings added but not in docs
```

## Step 4: Present Drift Report

Show the user the drift report:

```
Documentation drift detected (N items):

[architecture.md]
  1. <description>
  2. <description>

[deployment.md]
  3. <description>

No drift: patterns.md, ux-guidelines.md
```

Then ask: "Update documentation? (all / pick numbers / skip)"

- **all** → update all drift items
- **pick numbers** → update only selected items (e.g., "1, 3")
- **skip** → skip documentation update entirely

## Step 5: Update Documentation

For each approved drift item:
1. Read the current PK file
2. Read the actual source file to get current values
3. Update only the specific section affected
4. Do NOT rewrite unrelated sections

Quality rules (from documentation-writing):
- No code blocks in PK files — describe in prose
- No obvious/generic content — only project-specific
- Keep sections concise — one fact per line where possible
- Update counts/versions to match reality

After updates, show a brief summary of what was changed in each file.

## Step 6: Feature Archive (Feature Mode Only)

If a `work/{feature}/` directory was involved:

1. Read `decisions.md` (if exists) for quick-learning signals
2. Run quick-learning signal gate (fix rounds, scope change, recovery, context waste)
3. If signals present → extract patterns per quick-learning procedure
4. Move `work/{feature}/` → `work/completed/{feature}/`

If no feature directory — skip this step silently.

## Step 7: Commit & Report

If any documentation was updated:
```
docs: update project knowledge — <brief list of what changed>
```

Report to user:
- Documentation items updated (or "no drift detected")
- Feature archived (if applicable)
- Session closed

## Quick Path

If drift detection finds 0 items:
```
Documentation is up to date. Session closed.
```

No commit needed, no questions asked.

## Self-Verification

- [ ] Session diff collected (git log + changed files)
- [ ] PK files checked against actual changes
- [ ] Drift report shown to user (or "no drift" confirmed)
- [ ] User approved updates before writing
- [ ] Only affected sections updated (no unnecessary rewrites)
- [ ] Feature archived if applicable
- [ ] Changes committed
- [ ] Report delivered
