# Lessons Learned: task-decomposition

### 2026-03-25 design-pipeline: Broken paths и depends_on в сгенерированных задачах

**Problem:** Первый раунд валидации нашёл несуществующие пути к файлам и неверные depends_on ссылки в 12 задачах.
**Cause:** Task creator генерировал пути по предположению из tech-spec, не проверяя реальную структуру репозитория. depends_on ссылались на task ID которые не соответствовали реальным зависимостям.
**Solution:** 2 раунда валидации: fix broken paths → fix depends_on и directory ownership.
**Rule:** После генерации задач проверяй каждый путь к файлу через `test -e`. Валидируй depends_on: зависимость должна создавать артефакт, который зависимая задача читает.
