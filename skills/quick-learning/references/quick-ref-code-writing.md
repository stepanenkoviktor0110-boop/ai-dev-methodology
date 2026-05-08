# Quick Reference — Code Writing

1. Маскируй секреты ДО выполнения команды — встраивать sed-маскировку или grep -c вместо вывода .env. (Seen: 2)
2. Assertions на output-формат, не на input-атрибуты — для format-conversion функций читать реальный пример вывода перед написанием теста. (Seen: 2)
3. Path traversal из любых внешних данных — валидировать каждое значение против allowlist, даже для значений записанных самим приложением. (Seen: 2)
4. Generic retry decorator — явно исключать non-retryable exceptions (auth, validation), иначе ретраит вечно и сжигает квоту. (Seen: 1)
5. Unit-тесты с моками внешних процессов/API — минимум 1 live smoke run до declared QA passed, иначе mock диверджит от реальности. (Seen: 1)
6. Retry decorator с rate-limited API — проверить считаются ли failed requests в квоту до включения retry. (Seen: 1)
7. Config files с enum/nested — верифицировать все allowed values из официальной schema/docs включая nested objects. (Seen: 1)
8. Deploy-скрипты создающие named resources — cleanup по identity (name/ID), не через management tool, иначе orphaned resources блокируют. (Seen: 1)
9. TDD Anchor для private method — вызывать через object instance, не через direct import, иначе ImportError до запуска логики. (Seen: 1)
10. Clear/reset внешнего сервиса — явно сбрасывать ВСЕ слои state (content + formatting + cache), иначе предыдущий state всплывает. (Seen: 1)
