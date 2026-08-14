# Quick Reference — Task Decomposition

1. Wave numbers, not labels — pass task-creators explicit integers (audit=N+1, final=N+2); verify wave(consumer) > wave(producer) for every depends_on (Seen: 3)
2. Constraint-enforcement scope — check a value inside the region that actually enforces the constraint (predicate/restricting part), not in output/labels/metadata (Seen: 3)
3. Verify all cross-references after task generation — file paths via test -e, decision numbers by counting, depends_on by confirming the artifact is really produced (Seen: 2)
4. A test that straddles two tasks goes into the owning task's AC or TDD Anchor explicitly — a note in decisions.md is not read by the agent running that task (Seen: 2)
5. Same-file tasks across waves — bound the creating task's scope and write into the extending brief "the file already exists with X and Y; add only Z" (Seen: 2)
6. When an authoritative source appears for a previously inferred value — switch the approximate path off wherever the authoritative one exists, don't gate the fallback on its per-case outcome (Seen: 1)
7. When a protective rule seems not to fire — inspect what actually reached its input before editing the rule; an earlier stage may have decided the outcome (Seen: 1)
8. When making a hidden degradation visible — first establish who reads the proposed channel, then rank remedies: impossible-by-construction, then failing an existing gate, then notification (Seen: 1)
9. When two tasks describe the same edge case — cross-check both descriptions for consistency before committing, don't leave the contradiction to the validator (Seen: 1)
10. When a task adds client state to an existing server component — prescribe the client wrapper pattern, forbid converting the layout to "use client" (Seen: 1)
