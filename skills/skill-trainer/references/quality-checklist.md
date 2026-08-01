# Skill quality checklist (post-embedding)

Run after Phase 6 (quick-ref regen), before Phase 7 (commit). One parallel agent per modified skill.

## Two layers

1. **General skill compliance** — delegated to the `skill-checker` agent, which covers frontmatter,
   size, references and the refinement patterns. Not re-implemented here.
2. **Skill-trainer-specific** — the items below. They check the NEW rules this run applied, not the
   whole skill.

## Agent prompt

```
You audit a skill after skill-trainer embedded new rules.

Skill: {skill-name}
SKILL.md path: $AGENTS_HOME/skills/{skill-name}/SKILL.md
Write target (where new rules went): {write_target}
Newly applied rule IDs: {applied_ids}

STEP 1 — General skill health (delegate via Task tool):
Invoke the skill-checker agent on this skill. Capture its findings.

STEP 2 — Read SKILL.md and write_target. Check the items below against the NEW
applied rules (identifiable by the `(triad #N)` suffix or the recent diff):

### Size discipline
- [ ] A1. SKILL.md body ≤ 250 lines (soft limit, stricter than the 500-line hard limit).
      - 200–250 → WARN "approaching; time to move blocks into references/"
      - >250 → FAIL with a concrete proposal: which sections to move out
- [ ] A2. write_target (references/*.md) ≤ 500 lines
- [ ] A3. If SKILL.md is over 250, the body stayed coordination — a map of files, a reading
      order, gate questions — rather than the score itself (long procedures inline)

### Rule quality (new rules only)
- [ ] B1. Logical level: no project names, no file names recalled from memory, no session
      names. Tool names (pdfplumber, BigQuery, Prisma) are fine. Internal artifact names
      (mvp-booking-flow, school-stol) are not.
- [ ] B2. Every new rule carries a trigger→action→goal triad on one line
- [ ] B3. Every new rule cites its source triad as `(triad #N)` for traceability
- [ ] B4. No new rule duplicates an existing one by trigger+goal (grep the write_target
      before the new rules)
- [ ] B5. The trigger is specific — a recognisable situation ("when X happens", "before
      doing Y") — not generic ("when writing code", "when working with files")
- [ ] B6. The action is imperative and checkable ("grep X", "enumerate Y", "verify against
      Z"), not vague ("be careful", "consider", "think about")

### Carrier (refinement pattern P13)
- [ ] C1. A rule that some state on disk could settle went into "Checks against state" as a
      command, not into the pattern list as prose
- [ ] C2. Each such command states what its result must be (P2)
```

## Output JSON

```json
{
  "skill": "{name}",
  "skill_checker_findings": [...],
  "trainer_specific": {
    "passed": ["A1", "B1"],
    "failed": [{"item": "A1", "evidence": "SKILL.md 312 lines", "fix": "move Phase 3+4 into references/phases.md"}],
    "warned": [{"item": "A1", "note": "248 lines, close to the limit"}]
  }
}
```

## Gate behaviour (soft)

After all agents return, the main context aggregates:

- All pass → silent, proceed to Phase 7
- Any failed → show the owner a compact summary:
  ```
  Quality issues found:
  - {skill-name}: A1 (SKILL.md 312 lines), B4 (rule duplicates existing)
  - {skill-name}: B1 (rule mentions a project name)

  Действия:
  [починить] — спавню fix-агентов по каждому failed item
  [записать в known-issues] — фиксирую в $AGENTS_HOME/skills/{skill}/known-issues.md
  [игнорировать] — commit без починки
  ```
- Only warned → one line in the final report, no blocking

A hard gate is deliberately not used: the soft one leaves the owner in control and does not block a
quick pass over an insignificant deviation.
