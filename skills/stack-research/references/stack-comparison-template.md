# Stack Comparison: {decision-context}

Comparison table produced by `stack-research` skill when evaluating multiple candidates for a stack decision. Written to `.claude/skills/project-knowledge/references/stack-comparison-{slug}.md`.

**Checked:** {YYYY-MM-DD}
**Decision context:** {one-sentence description of what is being decided}
**Depth:** shallow | deep
**Sources:** {list of report files under work/{feature}/logs/stack-research/}

---

## Focus Answers

| Focus question | {Candidate A} | {Candidate B} | {Candidate C} |
|---|---|---|---|
| {Q1 from focus} | {answer A} | {answer B} | {answer C} |
| {Q2 from focus} | {answer A} | {answer B} | {answer C} |
| {Q3 from focus} | {answer A} | Not found in official docs | {answer C} |

## Key Facts

| Fact | {Candidate A} | {Candidate B} | {Candidate C} |
|---|---|---|---|
| Stable version | {version A} | {version B} | {version C} |
| Auth | {auth A} | {auth B} | {auth C} |
| Pricing | {pricing A} | {pricing B} | {pricing C} |
| Principal limit 1 | {limit A} | {limit B} | {limit C} |
| Principal limit 2 | {limit A} | {limit B} | {limit C} |

## Notes

- {candidate}: value for {focus question} was [cached from {date}] — version unchanged since last check.
- {candidate}: {focus question} — `Not found in official docs`; decision requires user input or live test.

---

**This file does not contain a recommendation.** The calling skill (project-planning or tech-spec-planning) reads this table and decides.
