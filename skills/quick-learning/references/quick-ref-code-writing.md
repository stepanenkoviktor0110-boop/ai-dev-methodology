# Quick Reference — Code Writing

1. Маскируй секреты ДО выполнения команды: при чтении конфигов удалённой машины — встраивать маскировку в команду (`sed 's/:[^@]*@/:***@/'`) или проверять через `grep -c`; никогда не выводить `.env` целиком (Seen: 2)
2. Assertions на output-формат, не на input-атрибуты: перед написанием assertions прочитать реальный пример вывода функции; для format-conversion функций assertions должны соответствовать output-формату (Seen: 2)
3. Path traversal из любых внешних данных — allowlist: перед построением файлового пути из внешнего значения — валидировать каждое значение против allowlist (Seen: 2)
4. useMemo dependency на промежуточный массив из render — вынести null-guard/нормализацию внутрь вычисляющей функции, dependency — исходный prop/state (Seen: 1)
5. Проект с "type":"module" и нужен CommonJS cron-скрипт — именовать .cjs и использовать DI: `main(_dep = require('dep'))` (Seen: 1)
6. Тест для finally-блока с except Exception — использовать BaseException (например KeyboardInterrupt) как trigger (Seen: 1)
7. Скрипт с дорогостоящей инициализацией (auth flow, DB connection) создаёт объект внутри цикла — вынести init за цикл и указать явно в spec (Seen: 1)
8. JS-функция устанавливает button.disabled = true в начале fetch — добавить .catch() на каждую fetch-цепочку которая мутирует UI state (Seen: 1)
9. Расширение API-ответа новым полем — grep тесты на exact-equality assertions для этого endpoint, чтобы не допустить отложенного тест-фейла (Seen: 1)
