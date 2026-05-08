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

## Step 2: Check if Project Knowledge Exists

If `.claude/skills/project-knowledge/references/` does not exist or is empty:
- Skip documentation check
- Inform user: "Project knowledge not initialized, skipping docs check."
- Jump to Step 6

## Step 3: Load Drift Checklist

Read `.claude/skills/project-knowledge/references/drift-checklist.md`.

This file maps source file patterns → PK documentation sections.
Each project maintains its own checklist tailored to its structure.

**If the file does not exist** — generate it:
1. Read the project's PK files to understand what's documented
2. Scan the project structure (`ls` key directories)
3. Create a checklist mapping actual project paths → PK sections
4. Write to `.claude/skills/project-knowledge/references/drift-checklist.md`
5. Inform user: "Generated drift checklist. Review it after session close."

**If session changes revealed new mappings** not in the checklist
(e.g., a new config file was added that affects deployment):
- Append the new mapping to the checklist
- Note it in the drift report: "Added to drift checklist: {mapping}"

### Drift Checklist Format

```markdown
# Drift Checklist

Maps source files/patterns to PK documentation sections.
Used by `/done` to detect when documentation may be outdated.

## architecture.md
- path/to/config.* — what it documents (e.g., "images, output mode")
- path/to/schema.ts — what it documents (e.g., "data model, table count")
- path/to/page.tsx — what it documents (e.g., "sections, anchors")

## deployment.md
- .github/workflows/ — CI/CD pipeline, secrets
- path/to/pm2.config.* — process manager config

## patterns.md
- (typically empty — patterns drift is hard to map to files)

## ux-guidelines.md
- path/to/styles/ — breakpoints, responsive rules
```

Each line: `- <glob or path pattern> — <what aspect of the PK section it affects>`

## Step 4: Detect Documentation Drift

Cross-reference the session's changed files against the drift checklist.

For each match:
1. Read the relevant PK section
2. Read the actual source file to see current state
3. Compare: does the PK section reflect the source file's current state?
4. If not → record as drift item with one-line description

**For each drift item, produce a one-line description:**
```
[architecture.md] images config changed: was formats:webp, now unoptimized:true
[deployment.md] REVALIDATE_SECRET added to env but not documented
```

## Step 5: Present Drift Report

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

## Step 6: Update Documentation

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

## Step 7: Feature Archive (Feature Mode Only)

If a `work/{feature}/` directory was involved:

1. Read `decisions.md` (if exists) for quick-learning signals
2. Run quick-learning signal gate (fix rounds, scope change, recovery, context waste)
3. If signals present → extract patterns per quick-learning procedure
4. Move `work/{feature}/` → `work/completed/{feature}/`

If no feature directory — skip this step silently.

## Step 8: Commit & Report

If any documentation was updated:
```
docs: update project knowledge — <brief list of what changed>
```

If drift checklist was created or updated, include it in the commit.

Report to user:
- Documentation items updated (or "no drift detected")
- Drift checklist updates (if any)
- Feature archived (if applicable)
- Session closed

## Quick Path

If drift detection finds 0 items: report "Documentation is up to date. Session closed." — no commit, no questions.
