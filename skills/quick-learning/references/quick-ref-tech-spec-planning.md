# Quick Reference — Tech Spec Planning

1. When a discovery list, query or bulk operation defines the scope → cross-check the count by an independent enumeration, read count-equals-limit as truncation, order by relevance before any cap, and verify the result by a signal independent of the selector (Seen: 4)
2. When a view, search or store returns empty / an implausible value → enumerate every channel and every layer that can hold it, including derived and index stores invisible to text search, before concluding it is absent or fabricated (Seen: 3)
3. When an external naming claim (stakeholder, doc, spec) is about to enter the spec → verify it against ground truth in code or docs before recording, to avoid name-mirage (Seen: 3)
4. When a quantitative gate is computed on a narrower input set, or an existing derived artifact is put to a new use → re-derive its scope, filters and thresholds against the new question before reading the number as a verdict (Seen: 2)
5. When starting work in a domain with persisted constraints, or writing code in a category already fixed once → pull those notes and prior fix signatures into a pre-flight checklist applied in one pass (Seen: 2)
6. When a remote endpoint degrades or times out while both ends look healthy → suspect the shared transport and get an independent external vantage before declaring the host down (Seen: 2)
7. When moving a task to another environment, or validating a portable artifact still sitting in the environment that produced it → enumerate implicit environment dependencies and verify it detached, as the recipient would receive it (Seen: 2)
8. When a reviewer confidently asserts a fact, or a deliverable states something cheaply checkable against a live source → run the cheapest live check before acting; assertiveness and training recall are not evidence (Seen: 2)
9. When carrying an API or data shape from research, docs or someone's description into a spec → get ONE live sample and copy the real status codes, format and edge cases (Seen: 2)
10. When a spec says "remove X from N files" or "replace Y" → grep every one of them before fixing the operation type; a file without X needs an add, not a replace (Seen: 2)
