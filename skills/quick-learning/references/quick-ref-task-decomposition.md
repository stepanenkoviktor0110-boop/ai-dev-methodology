# Quick Reference — Task Decomposition

1. Wave numbers, not labels — pass task-creators explicit numbers (audit=N+1, final=N+2); verify wave(consumer) > wave(producer) for every depends_on (Seen: 3)
2. Constraint-enforcement scope — check a value inside the region that actually enforces the constraint (predicate/restricting part), not in output/labels/metadata (Seen: 3)
3. Verify all cross-references after task generation — file paths via test -e, decision numbers by counting, depends_on by confirming the artifact is really produced (Seen: 2)
4. Тест на стыке задач — если тест относится к scope другой задачи, добавить его явно в её AC/TDD Anchor, а не только в decisions.md (Seen: 2)
5. Scope задач разных волн для одного файла — ограничить scope создающей задачи и в бриф расширяющей вписать "файл уже есть с X, Y; добавить только Z" (Seen: 2)
6. When a task changes a mandatory param of a public function and a downstream task calls it — state the new signature in the downstream brief to avoid silent TypeError (Seen: 1)
7. When a task-creator writes a curl/HTTP QA step — find the real endpoint path in integration helpers/routes, don't guess by REST convention (Seen: 1)
8. When two task-creators make new files with similar patterns — decide wave/depends_on by real import dependencies, not thematic similarity (Seen: 1)
9. When tech-spec paths are app-relative and the app lives in a subdir — pass full repo-root paths in each brief to keep Context File links valid (Seen: 1)
10. When a task adds client state to an existing server component — prescribe a client wrapper pattern, forbid converting the layout to "use client" (Seen: 1)
