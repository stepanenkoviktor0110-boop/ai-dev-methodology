# Calibration Protocol (Phases 1–3 detail)

$AGENTS_HOME = `~/.claude/skills`. Use forward-slash paths everywhere.

## Discovery

1. `Glob $AGENTS_HOME/*/SKILL.md` — collected after Phase 0 deletions
2. Per skill, compute:
   - SKILL.md line count via `Read` tool (count returned lines) or
     PowerShell `(Get-Content path | Measure-Object -Line).Lines`
   - `references/` directory exists (boolean)
   - Status:
     - ❌ if lines > 250
     - ⚠️ if 200 ≤ lines ≤ 250
     - ✅ if lines < 200
3. Append the full table to known-issues file under `## Phase 1 — Skill discovery`
4. Build calibration scope: every ❌ and ⚠️ skill. ✅ skills are recorded as
   `ok` in the final report and not audited

## Audit

One agent per skill in scope, spawned in waves of 3 concurrent agents
(never larger — protects session budget). Between waves the main context
only aggregates JSON results; no user prompt.

### Agent prompt

```
<context>
You are one of three parallel audit agents in a calibration run.
Your JSON output is aggregated by an orchestrator that decides which skills
to autofix and which to escalate. Emit exactly one JSON object — no prose
before or after it.
</context>

Output: one JSON object, structure defined in STEP 5.
All array fields default to [] when empty — never omit them.

Skill: {skill-name}
SKILL.md: ~/.claude/skills/{skill-name}/SKILL.md

STEP 1 — General compliance
Spawn a subagent via the Agent tool with subagent_type="skill-checker".
Pass the skill path. Capture findings as `skill_checker_findings`
(array of strings, raw finding text).

STEP 2 — Trainer-specific checks
Read SKILL.md and any references/*.md.
Apply the checklist in ~/.claude/skills/skill-trainer/references/quality-checklist.md
items A1–A3 (size discipline) and B1–B6 (rule quality, only on rules
carrying a `(triad #N)` suffix).

STEP 3 — Skip conditions (set flags, exclude from `failed`, skip STEP 4 for these)
- SKILL.md > 500 lines → set `needs_human_redesign: true`
- Skill is informational (no `## Phase N` blocks, no numbered procedural steps)
  and only A1 fails → set `unsafe_to_autofix: true`

STEP 4 — For each non-skip failure, propose a concrete fix:
- A1 (>250 lines) → list specific section headers to extract,
  predicted post-extract line count
- B1 (project name) → exact line + replacement string
- Path/naming/description issues → exact edit

STEP 5 — Output contract

Field types:
- skill: string
- size.current: integer (line count)
- size.verdict: "ok" | "warn" | "fail"
- skill_checker_findings: array of strings
- failed: array of {item: string, evidence: string, fix: string}
- warned: same shape as failed; fix may be ""
- auto_fixable: array of strings, each formatted as "<label> (<count>)"
- needs_human_redesign: boolean
- unsafe_to_autofix: boolean

Example (filled):
{
  "skill": "code-writing",
  "size": {"current": 263, "verdict": "fail"},
  "skill_checker_findings": ["description exceeds 1024 chars"],
  "failed": [{"item": "A1", "evidence": "263 lines > 250", "fix": "Extract '## Phase 3' block (41 lines) to references/phase3-detail.md → predicted 222 lines"}],
  "warned": [],
  "auto_fixable": ["forward slashes (2)"],
  "needs_human_redesign": false,
  "unsafe_to_autofix": false
}
```

## Autofix

Per skill (from Audit results), apply fixes in this order without user prompt.

### Auto-apply (no confidence check)
- Forward slashes in file paths
- Naming and description formal corrections (kebab-case enforced,
  description trimmed to ≤1024 chars, lowercase name)
- Time-sensitive phrasing rewrites ("after August 2025" → "previously")
- Removal of references to deleted design skills (already handled in 0.1
  but double-check here)

### Conservative-apply (only when all conditions met)

**Section extraction to `references/`** — apply only if:
1. Skill is procedural (has `## Phase N` or numbered `## N. Step` blocks)
2. The block to extract is >40 lines
3. Block has clear boundary (next `##` heading or end of file)
4. Skill has no existing block name collision in `references/`

If any condition fails → record under `## Phase 3 — Manual fix needed`,
do not edit.

**Rule deduplication** — apply only when:
- Two rules in same `references/*-patterns.md` file have exact match on
  normalized trigger + goal (case-insensitive, whitespace-collapsed)
- Otherwise → record under known-issues, do not merge

### Commit per skill

After all fixes for one skill applied:
- Verify SKILL.md still parses (frontmatter intact, headings preserved)
- Verify line count reduced to ≤250 if A1 was fixed
- Commit: `chore(skill): calibrate {name} ({old_lines}→{new_lines} lines, {fix_summary})`
- Move to next skill

### Skipped to known-issues

Anything not applied is appended to known-issues with category:
- `needs_human_redesign` (>500 lines or architectural issues)
- `unsafe_to_autofix` (informational skill, no clear extraction targets)
- `manual_section_extraction` (procedural but boundaries unclear)
- `dedup_partial_overlap` (rules look similar but trigger/goal differ)
