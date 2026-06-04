# Quick Reference — Tech Spec Planning

1. Верифицируй целевые файлы перед описанием операции — grep каждый файл, чтобы отличить replace от add (Seen: 2)
2. Верифицируй API response shapes live-вызовом перед включением в спек — один curl дешевле миража через pipeline (Seen: 2)
3. Верифицируй файловые пути через ls/glob, а не из памяти или architecture docs — docs описывают намерение, не реальность (Seen: 2)
4. При migration на проектный scope — уточни, ресурс универсальный или domain-specific, чтобы не сломать universal-access (Seen: 1)
5. Production defaults (run time, port, limit) — явно подтверждай с пользователем, иначе late correction каскадом (Seen: 1)
6. На "проверь соответствие первоисточнику" — сначала fetch источника, потом правки, не выдумывай данные (Seen: 1)
7. Permission matrix для одной destructive операции — проверь ВСЕ аналогичные (deactivate, reset, role change) на тот же matrix (Seen: 1)
8. URL/endpoints в user-spec AVP из памяти — grep каждый URL+method в коде до approve, чтобы не пропустить mirage (Seen: 1)
9. GET=admin+manager и PUT=manager-only при guard разрешающем оба — явно опиши создание нового guard для PUT (Seen: 1)
10. task-creator агенты — проверь runner (jest/vitest/pytest) и тест-директории, передай явно в каждый бриф (Seen: 1)
