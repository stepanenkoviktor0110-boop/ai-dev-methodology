# Quick Reference — Code Writing

1. При любом чтении конфигов с секретами — встраивать маскировку в команду (`sed 's/:[^@]*@/:***@/'`) или проверять через `grep -c`; никогда не выводить `.env` целиком (Seen: 2)
2. Для format-conversion функций assertions писать на output-формат, а не на input-атрибуты — иначе тест не ловит баги конвертации (Seen: 2)
3. Перед построением файлового пути из внешних данных (диск, user input, API) — валидировать каждое значение против allowlist (Seen: 2)
4. Тест для `finally`-блока с `except Exception` — использовать `BaseException` (например `KeyboardInterrupt`) как trigger, чтобы гарантировать выполнение finally при любом исходе (Seen: 2)
5. Скрипт с дорогостоящей инициализацией (auth flow, DB connection) создаёт объект внутри цикла — вынести init за цикл и указать явно в spec (Seen: 2)
6. Если файл не менялся — читать его один раз в начале задачи, не читать повторно (Seen: 2)
7. `useMemo` dependency ссылается на промежуточный массив из render — вынести null-guard/нормализацию внутрь вычисляющей функции, dependency — исходный prop/state (Seen: 1)
8. Проект с `"type":"module"`, нужен CommonJS cron-скрипт — именовать `.cjs` и использовать DI: `main(_dep = require('dep'))` (Seen: 1)
9. Кнопка делает async-запрос — добавить `disabled`+loading state на время запроса AND `.catch()` восстанавливающий state при ошибке, до первого review (Seen: 1)
10. Расширение API-ответа новым полем — grep тесты на exact-equality assertions для этого endpoint, чтобы не допустить отложенного тест-фейла (Seen: 1)
