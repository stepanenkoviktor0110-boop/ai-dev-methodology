# Quick Reference — Task Decomposition

1. Wave numbers, not labels — передавать task-creator явные числа; для каждой пары depends_on проверять wave(consumer) > wave(producer) (Seen: 3)
2. Verify all cross-references after task generation — file paths via `test -e`, decision numbers, depends_on artifacts (Seen: 2)
3. Тест на стыке задач — добавить явно в AC/TDD задачи-владельца; decisions.md соседние агенты не читают (Seen: 2)
4. String-output assertions — извлекай нужную секцию (regex/split), затем проверяй значение внутри неё (Seen: 2)
5. Scope задач разных волн для одного файла — явно ограничить scope A ("только X"); в бриф B: "файл уже есть с X, Y. Добавить только Z." (Seen: 2)
6. Task меняет сигнатуру public function — явно прописать новую сигнатуру в брифе downstream-задачи (Seen: 1)
7. curl/HTTP в QA-шаге — искать реальный endpoint в integration helpers/routes, не гадать по REST-конвенции (Seen: 1)
8. Два новых файла с похожим кодом — проверять реальные import-зависимости перед wave/depends_on (Seen: 1)
9. App в подпапке репо — передавать полный путь от корня репо в каждом брифе task-creator (Seen: 1)
10. Параллельная волна — попарно проверить Files to modify всех задач волны на пересечения до коммита (Seen: 1)
