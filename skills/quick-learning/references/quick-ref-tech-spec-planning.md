# Quick Reference — Tech Spec Planning

1. При интеграции с внешним API — перенести в спек ВСЕ коды ответа, формат данных и edge cases; live API call для проверки (Seen: 3)
2. Верифицировать values/methods против реальной документации — не принимать на веру память (Seen: 3)
3. Файловые пути через ls/glob + grep по имени функции перед записью call sites в Files to modify (Seen: 3)
4. Запуск task-creator агентов → проверить runner (jest/vitest/pytest) и тест-директории, передать явно (Seen: 3)
5. Верифицировать целевые файлы перед описанием операции: grep по каждому файлу перед фиксацией типа (Seen: 2)
6. Требования к формату поступают итеративно → согласовать полную структуру до кода (Seen: 2)
7. Утверждение persistence-дизайна → прогнать мысленный walkthrough всех CRUD-операций до утверждения (Seen: 2)
8. Завершение Implementation Tasks → проверить overlap "Files to modify" внутри каждой волны (Seen: 2)
9. Вопрос об инфраструктуре или production URL → читать decisions.md ДО project-knowledge docs (Seen: 2)
10. Tech-spec decision меняет поведение из user-spec → проверить AC и таблицу проверки user-spec перед записью (Seen: 2)
