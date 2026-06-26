# Quick Reference — Task Decomposition

1. When moving tasks between waves, check "Files to modify" of all wave tasks pairwise for file overlap to prevent merge conflict and duplication. (Seen: 5)
2. Scope tasks of different waves touching one file: constrain the earlier task's scope explicitly and tell the later task the file already exists, with which functions to add. (Seen: 3)
3. When a task changes a function's API contract, or parallel task-creators generate producer/consumer tasks — state the full signature (name, args, return types) and who generates which fields in the downstream brief. (Seen: 3)
4. After generating tasks, verify all cross-references (file paths, decision numbers, depends_on producing the referenced artifact). (Seen: 2)
5. Wave fields are numbers, not labels (audit=N+1, final=N+2); validate wave(consumer) > wave(producer) for every depends_on pair. (Seen: 2)
6. Add the test explicitly to that task's spec/AC, not only to notes — limit string-output assertions to the needed section slice. (Seen: 2)
7. When task N creates no-op stubs "for later tasks", add an explicit "replace the no-op stub with the implementation" step to each filling task's brief. (Seen: 2)
8. Parallel task-creators using relative paths (import, @use, context files) at different nesting depths — compute and pass the concrete path in each brief, don't rely on copying a neighbor's pattern. (Seen: 2)
9. When two tasks describe behavior/scope for one resource or edge case, cross-check both descriptions for consistency before commit. (Seen: 2)
10. Spawning parallel autonomous producers whose outputs must interoperate — pass exact interface contracts to each; independent producers can't converge from prose alone. (Seen: 2)
