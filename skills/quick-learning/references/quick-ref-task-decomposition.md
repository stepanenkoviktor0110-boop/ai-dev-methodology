# Quick Reference — Task Decomposition

1. Pass waves to task-creator as explicit numbers, not semantic labels (audit=N+1, final=N+2); validate wave(consumer) > wave(producer) for every depends_on pair. (Seen: 3)
2. When two waves touch one file, constrain the earlier task's scope explicitly and tell the later task the file already exists with which functions to add. (Seen: 3)
3. After task generation, verify every cross-reference: file paths via test, decision numbers by counting, depends_on by confirming the dependency produces the referenced artifact. (Seen: 2)
4. When a test belongs to another task's scope, add it explicitly to that task's AC or TDD Anchor — a decisions.md note is not enough. (Seen: 2)
5. When writing an assertion for conditional/data-dependent behavior, ask "does it fail for any correct-but-wrong impl?" before committing, to avoid all-paths assertion bias. (triad #413, Seen: 2)
6. For string-output tests, extract the enforcing region (restricting/predicate part) and search the token only there; a token in output/labels/metadata must not count. (triad #384, Seen: 1)
7. When a spec assigns an error-catching mechanism, verify it operates in every execution context where the failure can originate (sync vs async, render vs handler). (triad #401, Seen: 1)
8. When judging a "match the reference exactly" criterion, enumerate every facet and verify each independently, not just the most-visible one. (triad #403, Seen: 1)
9. When a generator keeps emitting a forbidden output after strengthened "don't" rules, reframe the eliciting task as a capability/identity boundary instead of stacking prohibitions. (triad #408, Seen: 1)
10. When a unit test checks an attribute via a loose mock, pin the test double to the real attribute path (spec=, real value, or real instance) to close the mock-autospec trust gap. (triad #412, Seen: 1)
