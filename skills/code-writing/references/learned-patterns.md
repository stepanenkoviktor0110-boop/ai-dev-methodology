# Learned Patterns — Code Writing

> Loaded by audit agents and retrospective only. Orchestrator loads only Promoted Patterns (in SKILL.md).

- When wrapping API calls with a generic retry decorator -> explicitly exclude non-retryable exceptions (auth errors, validation failures) to avoid retrying errors that will always recur
- When unit tests use mocks for external processes/APIs -> run at minimum 1 live smoke run before declaring QA passed, to prevent false all-tests-pass when mock diverges from reality
- When using a retry decorator with a rate-limited API -> verify whether failed requests count toward the quota before enabling retry, to avoid burning quota on pointless retries
- When generating config files with enum fields or nested configs -> verify all allowed values from the official schema/docs including nested objects to avoid invalid-but-plausible values
- When writing deploy scripts that create named resources -> clean up by identity (name/ID), not through management tool, to prevent failure from orphaned resources
- When TDD Anchor describes a test for a private class method -> invoke through an object instance, not through direct import, so tests do not fail with ImportError before running real logic
- When calling clear/reset on an external service before writing new data -> explicitly reset ALL state layers (content + formatting + cache) to prevent previous state from surfacing after cleanup
- When CSS-правило не применяется к элементу несмотря на правильное объявление → проверить наличие inline styles или JS-управляемых стилей на целевом элементе — применять стилизацию через тот же механизм, to не тратить fix-раунды на CSS который не может переопределить стиль с более высоким приоритетом
- When connecting an external library adapter to a DB -> verify the expected object type (raw driver vs query builder) in docs BEFORE writing init code, to avoid runtime adapter incompatibility on first query
- When CI/CD pipeline выполняет команду с повышенными правами от deploy-пользователя → проверить права deploy-пользователя и убрать sudo для операций доступных напрямую; явно задать параметры доверия хоста для автоматического SSH, to не получать permission denied на первом автоматическом деплое
- When параллельные тесты используют общий seed-ресурс (пользователь, запись) в тестовой БД → использовать уникальные идентификаторы per-test вместо общей константы, to избежать teardown race condition при параллельном выполнении
- When JS state exists only to toggle CSS values by viewport -> replace state+listener with CSS media queries + className to eliminate re-renders and make layout CSS-controlled
- When интеграционные тесты с разделяемым соединением к БД зависают после завершения suite → добавить явное освобождение соединения в глобальный teardown тест-окружения, не полагаться на GC, to не допустить зависание тест-процесса из-за незакрытого соединения
- When E2E тест с асинхронной UI-операцией (upload, submit, save) → заменить фиксированную задержку (sleep/timeout) на assertion конкретного состояния UI-элемента, to избежать flaky test и false-positive из-за race с таймером
- When implementing an HTTP server with API key auth -> include timing-safe comparison and explicit body size limit in the initial implementation, to avoid a predictable security review round
- When a helper function accepts a value from an external source (API response, env var, user input) -> manually check edge cases (null, undefined, empty string, 0) before first review
- When task has numeric thresholds in code -> extract magic numbers to named constants before first review, to avoid a predictable hardcoded-value review finding
- When a library config option is silently ignored in a new major version -> check option behavior in config-file vs CLI through changelog/issues for the current version BEFORE writing config
- When an integration test checks duplicate/error flow in an auth library -> verify through DB side effect, not HTTP status, to avoid false-negative when library returns 200 with a resend flow
- When E2E global-setup требует предсозданного пользователя с верифицированным статусом → создать пользователя напрямую в БД вместо sign-up flow — снять зависимость seed-фазы от работающего сервера, to гарантировать стабильность setup независимо от состояния сервера
- When adding a new parameter to an existing API request -> check nullable response fields with the new parameter on real data, to prevent TypeError in production
- When передача файла/данных на удалённый хост через сложную SSH-команду (heredoc, SCP) обрывает соединение → упростить передачу — передавать файл как stdin pipe вместо heredoc или SCP, to загрузить данные без смены способа аутентификации или порта
- When a bash command passes $(find ... | cut ...) as a path to a flag accepting a file path -> extract the substitution to a named variable in a separate quoted command, to avoid silent false results when paths contain spaces
- When обработчик auth-библиотеки возвращает 404 для корректного пути → проверить базовый URL конфигурации библиотеки на лишний path prefix перед диагностикой маршрутизации, to не тратить итерации на маршрутизацию когда ошибка в конфигурации URL
- When API route возвращает 404, серверных ошибок нет, логи не срабатывают → проверить compiled output на асинхронную инициализацию модуля как возможный silent initialization failure, to диагностировать тихий сбой инициализации модуля до перебора маршрутизации
- When dev-сервер возвращает ошибку про отсутствующий модуль при неизменных зависимостях → очистить кеш сборки и перезапустить сервер до диагностики зависимостей, to не тратить итерации на зависимости когда источник — устаревший кеш сборки
- When a backlog task describes adding a guard/validation to a file modified in earlier waves -> read the actual file before coding to check whether the guard already exists, to avoid duplicating implementation added as a byproduct of another task
