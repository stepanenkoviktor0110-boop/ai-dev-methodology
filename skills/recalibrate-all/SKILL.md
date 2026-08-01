---
name: recalibrate-all
disable-model-invocation: true
description: |
  Autonomous one-shot cleanup and calibration of all skills in $AGENTS_HOME.
  Removes 16 obsolete design skills (keeps photo-crop, content-card),
  purges codex references from active skills and triads, calibrates remaining
  skills against Anthropic best practices and the 250-line SKILL.md soft limit.
  Runs end-to-end without user gates; risky items skipped to known-issues
  for post-run review rather than asked about mid-flight.

  Use when user explicitly says "/recalibrate-all", "откалибровать все скиллы",
  "почистить устаревшее", "calibrate all skills", "перекалибровать скиллы",
  "recalibrate methodology", "clean up skills".
---

# Recalibrate All (autonomous)

End-to-end cleanup and calibration of `~/.claude/skills/`. Each phase commits separately.
All risky or ambiguous cases are logged to `~/.claude/skills/.known-issues/recalibrate-{date}.md`
for post-run review. No mid-flight user prompts.

## Pre-flight

1. `cd ~/.claude/skills`
2. Check `git status --porcelain` is empty. If dirty — abort with message;
   do not auto-stash (user may have intentional WIP).
3. Create `.known-issues/recalibrate-{YYYY-MM-DD}.md` with empty section headers
   for each phase. All skip-decisions append here.

## Phase 0: Cleanup

Execute the full destructive protocol in [cleanup-protocol.md](references/cleanup-protocol.md).

Risk gates (auto-skip rules, no user prompt):
- Deleting a design skill referenced by a kept skill → skip deletion, log
  `{skill} referenced by {file}:{line}, replacement not found`
- Codex triad where stripping the word codex breaks trigger/action semantics →
  retain triad as-is, log `{id} retained: semantic loss on codex-strip`
- Memory file whose filename matches `*codex*` but body is an active prohibition
  ("never use codex", "no codex", "запрет", ⛔) → keep
- Orphan reference to design skill with no equivalent in
  `frontend-design:frontend-design` plugin → skip deletion of that design skill, log

Sub-phases (sequential, each commits before next):

- **0.1** Pre-scan orphan-map, replace orphan refs → `frontend-design:frontend-design`
- **0.2** Delete the 16 design dirs (except those skipped in 0.1)
- **0.3** Purge codex from active skills
- **0.4** Purge codex triads (keep generic delegation, strip the word codex)
- **0.5** Purge per-project codex memory across all `~/.claude/projects/`

### Checkpoint: Phase 0 complete

Before entering Phase 1, verify:
1. `git log --oneline -6` shows the 5 expected sub-phase commits
2. All 16 design dirs absent from `Glob ~/.claude/skills/*/SKILL.md` except
   those recorded in known-issues `## 0.2 skipped deletions`
3. `photo-crop` and `content-card` SKILL.md still exist
4. `feedback_never_use_codex.md` and `feedback_no_codex.md` still exist in any
   project memory dir
5. known-issues file has non-empty Phase 0 sections

Any check fails → abort the run, print failures, leave state for inspection.

## Phase 1: Discovery (no gate)

See [calibration-protocol.md](references/calibration-protocol.md) → Discovery section.

1. `Glob $AGENTS_HOME/*/SKILL.md` ($AGENTS_HOME is `~/.claude/skills`)
2. Per skill: line count, presence of `references/`, status
   (❌ >250 / ⚠️ 200–250 / ✅ <200)
3. Append the full table to known-issues file under `## Phase 1 — Skill discovery`
4. Auto-scope: every ❌ and ⚠️ enters Phase 2; ✅ are recorded `ok` for the final report

### Checkpoint: Phase 1 complete

Before entering Phase 2:
1. Discovery table has ≥1 row
2. If calibration scope (❌ + ⚠️) is empty → skip Phase 2 with explicit
   "nothing to calibrate" log entry, jump to Phase 4

## Phase 2: Audit (waves of 3 concurrent agents, never larger)

See [calibration-protocol.md](references/calibration-protocol.md) → Audit section.

- One agent per skill, spawned in waves of 3 concurrent agents (never larger
  — protects session budget when scope is 20+ skills)
- Between waves: aggregate JSON, no user prompt
- Hard skip rules (auto, log to known-issues):
  - SKILL.md > 500 lines (2× soft limit) → mark `needs_human_redesign`
  - Skill is informational (no `## Phase N` blocks, no numbered steps) and
    only failure is A1 → section extraction unsafe, skip

## Phase 3: Auto-fix (no per-skill confirm)

See [calibration-protocol.md](references/calibration-protocol.md) → Autofix section.

Auto-apply without confirmation:
- Forward slashes in file paths
- Naming and description formal corrections
- Time-sensitive phrasing rewrites

Conservative-apply only when high confidence:
- Section extraction to `references/` when procedural skill + block >40 lines + clear boundary
- Rule dedup only on exact normalized trigger+goal match

## Phase 4: Final report and push

1. Console summary:
   ```
   Cleanup: deleted {N} skills, purged {N} files, retained {N} prohibition memories
   Calibration: audited {N}, fixed {N}, known-issues {N}, needs-redesign {N}
   ```
2. `git push origin master`. On failure: `git fetch && git rebase origin/master`,
   retry push once. Second failure → leave local, log to known-issues
3. Print absolute path to known-issues file

## Checks against state

This skill deletes and rewrites files across every project, so the checks read what survived
rather than what was intended.

```bash
# 1. the prohibitions that must never be deleted are still present
rg -l "feedback_never_use_codex|feedback_no_codex" ~/.claude/projects/

# 2. no skill listed in the run's retain-list went missing
rg -l . ~/.claude/skills/*/SKILL.md | wc -l

# 3. the plugin directory was not touched
git -C ~/.claude/skills status --short -- ../plugins

# 4. every phase left a commit, and the known-issues file was appended
git -C ~/.claude/skills log --oneline -20
rg -c . ~/.claude/skills/.known-issues/recalibrate-*.md

# 5. per-project MEMORY.md indices no longer point at deleted memory files
rg -o "\]\(([a-z0-9-]+\.md)\)" -r '$1' ~/.claude/projects/*/memory/MEMORY.md
```

Check 1 returning nothing means an active prohibition was deleted — restore it from git before
doing anything else. Check 5 lists every file each index claims exists; any name with no file
behind it is a dangling index entry left by a deletion.
