# Cleanup Protocol (Phase 0 detail)

Detailed steps for the destructive cleanup phase.
Each sub-phase commits before next begins.
$AGENTS_HOME = `~/.claude/skills`.

## 0.1 Pre-scan orphan-map

Doomed design skills (16):
banner-design, brand, design, design-generate, design-plan, design-plan-planning,
design-retrospective, design-review, design-spec, design-spec-planning,
design-system, design-system-init, design-task-decompose, slides, ui-styling,
ui-ux-pro-max.

Kept design skills (2): photo-crop, content-card.

Procedure:
1. Use `Glob $AGENTS_HOME/*/SKILL.md` and `Glob $AGENTS_HOME/*/references/*.md`
   to enumerate candidate files. Exclude doomed dirs themselves.
2. For each doomed name: `Grep "{name}"` across collected files
3. Build orphan-map: `{file: [{line, match, doomed_skill}]}`
4. Replacement rule:
   - Reference is about visual/styling generation → replace with
     `frontend-design:frontend-design`
   - Reference is about planning (design-spec, design-plan, design-task-decompose) →
     no equivalent in plugin → mark `unreplaceable` in orphan-map
5. Apply replacements via Edit tool
6. For doomed skills with `unreplaceable` references → record in known-issues
   under `## 0.2 skipped deletions` and exclude from 0.2
7. Commit: `chore(skills): replace orphan design refs with frontend-design plugin`

## 0.2 Delete design skills

Procedure:
1. For each non-skipped doomed skill: `Remove-Item -Recurse -Force ~/.claude/skills/{name}`
   (PowerShell native; do not use `rm -rf` which is bash-only on Windows)
2. Verify deletion: `Glob ~/.claude/skills/{name}/SKILL.md` returns empty
3. Commit: `chore(skills): remove obsolete design skills, keep photo-crop + content-card`

## 0.3 Purge codex from active skills

Target files:
- `skills/code-writing/SKILL.md` (and `references/`)
- `skills/do-task/SKILL.md` (and `references/`)
- `skills/feature-execution/SKILL.md` (and `references/`)
- `skills/quick-learning/references/quick-ref-feature-execution.md`

### Classification examples

| Category | Example line | Action |
|---|---|---|
| Codex-only block | "Use codex:rescue for all multi-file refactors" | Delete entire paragraph |
| Generic delegation with codex example | "Delegate to an external agent (e.g. codex:rescue) when task exceeds context" | Keep sentence, replace `codex:rescue` with `a subagent` |
| Bash command or hook | `codex setup --model gpt-4` | Delete line |

### Procedure per file

1. `Grep -n -i "codex"` to list occurrences
2. For each occurrence, classify per table above
3. Apply edit (delete or rephrase) — preserve surrounding paragraph integrity
4. Verify no remaining `codex` matches outside acceptable contexts
5. Commit: `chore(skills): purge codex references from active skills`

## 0.4 Purge codex triads

Files:
- `skills/quick-learning/references/triad-index.md`
- `skills/quick-learning/references/reasoning-patterns.md`
- `skills/quick-learning/references/quick-ref-feature-execution.md`

### Classification examples

Codex-specific (delete entirely):
- trigger=`codex task is queued`, action=`poll codex job status`
- Reason: removing the word codex leaves no coherent rule.

Generic delegation (rewrite, keep):
- trigger=`large multi-file refactor requested`, action=`delegate to codex subagent`
- Rewrite to: trigger unchanged, action=`delegate to external subagent`
- Reason: the rule is about delegation policy, codex is just an example agent.

### Procedure

1. `Grep -n -i "codex"` in triad-index.md
2. For each matched row, locate full entry in reasoning-patterns.md
3. Classify per examples above
4. Apply edits in single passes per file (one Edit/Write per file)
5. Regenerate quick-ref-feature-execution.md: collect remaining patterns from
   feature-execution/orchestrator-patterns.md + Promoted Patterns,
   top 10 by Seen desc
6. Commit: `chore(quick-learning): purge codex-specific triads, keep generic delegation`

## 0.5 Purge per-project codex memory

Scope: ALL `~/.claude/projects/*/memory/` directories.

### Procedure

1. Use `Glob ~/.claude/projects/*/memory/*codex*` (cross-platform; do not use
   POSIX `find`). Also enumerate any file named exactly `project_codex_pipeline_product.md`.
2. For each candidate, Read the file:
   - **Keep** if file contains an explicit prohibition of codex usage:
     direct phrases ("never use codex", "no codex", "do not use codex",
     "запрет на codex", "не использовать codex"), emoji markers (⛔, 🚫)
     applied to codex, or sentences declaring codex disabled/forbidden.
   - **Delete** otherwise (file references codex neutrally or positively).
3. For each deleted file:
   - Find the parent `MEMORY.md` index
   - Remove the matching `- [name](file.md) — ...` line via Edit
4. Commit: `chore(memory): purge stale codex memory across all projects`

## Known-issues file format

Section structure (appended through phases):

```markdown
# Recalibrate-all run {YYYY-MM-DD}

## Phase 0.1 — Orphan map
| File | Line | Match | Doomed skill | Replacement |

## Phase 0.2 — Skipped deletions
- {skill}: referenced by {file}:{line} — no replacement

## Phase 0.3 — Codex retention (generic delegation kept)
- {file}:{line}: rule retained, only example stripped

## Phase 0.4 — Triad retention
- triad #{N}: {reason}

## Phase 0.5 — Memory retention
- {file}: contains active prohibition

## Phase 1 — Skill discovery
| Skill | Lines | references/ | Status |

## Phase 2 — Audit findings (skipped)
- {skill}: {reason}

## Phase 3 — Manual fix needed
- {skill}: {item} {evidence}
```
