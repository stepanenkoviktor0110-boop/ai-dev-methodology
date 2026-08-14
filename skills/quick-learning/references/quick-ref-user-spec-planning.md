# Quick Reference — User Spec Planning

1. A deliverable made of several steps (prompt series, roadmap, session plan, deploy instructions) — generate ALL steps in one pass, never a partial set (Seen: 3)
2. Writing distribution or hand-off instructions — enumerate the target environment's prerequisites and invariants explicitly before choosing the method; never project the author's environment onto the executor's (Seen: 2)
3. User adds a non-trivial feature mid-interview — ask a scope-impact question before updating the spec, so v1 does not grow into a different complexity level (Seen: 2)
4. A new role appears mid-interview — immediately build a role x capabilities matrix and validate it with the user (Seen: 2)
5. Spec describes a CRUD form for one entity while the target workflow acts on a group — clarify cardinality ("one or many?") before implementation (Seen: 2)
6. A UI task adds visible disabled buttons as placeholders for a future task — do not add them until that future task is confirmed (Seen: 2)
7. Relaxing an access check to permit one operation — enumerate every operation the same predicate gates, add explicit checks for those that must stay closed, and test each still-closed path (Seen: 2)
8. A word in the request admits both a minimal and an additive reading — build the minimal one and raise the additive one as an explicit question before implementing it (Seen: 1)
9. Spec requires a field the current increment's producer cannot populate yet — implement a conditional no-op path and test BOTH the empty (now) and populated (later) inputs (Seen: 1)
10. Broadening a matching rule to fix a missed case — enumerate the adjacent inputs the widened rule now also matches and confirm none belongs in a different bucket (Seen: 1)
