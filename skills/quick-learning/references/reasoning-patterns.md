# Reasoning Patterns

Accumulated insights about decision-making logic across projects.
Single transit buffer for ALL methodology knowledge — both reasoning patterns and operational lessons.

**This is a transit buffer.** Patterns that reach `Seen: 3` get promoted into skill SKILL.md files and removed from here. Stale entries (Seen: 1, older than 30 days) get pruned.

---

## Universal

Patterns that apply to any project, any stack, any domain.

<!-- Append universal patterns below -->

### 2026-04-01 employee-cabinet / session 1: Поведение конфиг-опций в новой major-версии библиотеки

**Seen:** 1
**Adapted:** —
**Triad:** конфигурационная опция библиотеки молча игнорируется в новой major-версии → проверить поведение опции в config-file vs CLI через changelog/issues для текущей версии ДО написания конфига → не тратить fix-раунд на конфигурацию которую версия игнорирует
**Context:** Task 1 — Vitest 4.x игнорирует `passWithNoTests` в inline project definitions, но flag работает в CLI. Конфиг был написан по документации предыдущих версий — потребовался Deviation-комментарий и добавление `--passWithNoTests` в npm scripts.
**Pattern:** Если конфигурационная опция задокументирована, но приложение ведёт себя иначе — проверить changelog/issues для точной major-версии. Поведение может быть intentionally changed с workaround через другой слой (CLI flag вместо config key).
**Scope:** universal
**Category:** tool-selection

---

### 2026-04-01 employee-cabinet / session 2: Интеграционные тесты с pg pool — singleton teardown

**Seen:** 1
**Adapted:** —
**Triad:** интеграционные тесты с pg connection pool (shared singleton) → объявить globalTeardown в vitest.config, вызывать pool.end() там один раз → не допустить зависание тест-процесса или "pool ended" при последовательных suite
**Context:** Task 9 — каждый из 4 тест-файлов вызывал `testDb.end()` в своём afterAll. Это shared singleton из helpers/db.ts. При последовательном запуске suite в одном worker первый завершившийся закрывал пул; следующие suite падали с "Cannot use a pool after calling end". Исправление: убрать end() из всех afterAll, создать global-teardown.ts с единственным вызовом, подключить через vitest.config globalSetup.

---

### 2026-04-01 dashboard-progress-sync / session decompose: именованные экспорты для cross-wave тестов

**Seen:** 1
**Adapted:** —
**Triad:** Task B тестирует функции из файла, созданного Task A → добавить сигнатуры этих функций в What to do Task A (не только в TDD Anchor Task B) → гарантировать ownership экспортов — ни одна функция не остаётся без явного владельца
**Context:** Task 5 ожидала unit-тестировать `validateProgressBody` и `formatProgressDays` из server/index.js (Task 1), но Task 1 не упоминала их создание. Нарушение поймано cross-task reality checker на этапе валидации. Task 5 получила recovery-путь "добавь сам если нет", но это означает молчаливое изменение чужого файла без декларации.
**Pattern:** При написании TDD Anchor для задачи B — если тестируются функции из файла задачи A — проверить What to do задачи A и явно добавить туда создание и экспорт этих функций. Функция без объявленного владельца рискует быть пропущена или дублирована.
**Scope:** universal
**Category:** problem-decomposition

---

### 2026-04-01 employee-cabinet / session 2: E2E тесты — детерминированный assertion вместо waitForTimeout

**Seen:** 1
**Adapted:** —
**Triad:** E2E тест с async UI-операцией (upload, submit, save) → заменить waitForTimeout(N) на assertion конкретного data-testid элемента (toBeVisible/toBeDisabled) → избежать flaky test и false-positive из-за race с таймером
**Context:** Task 10 — certificates.spec.ts использовал waitForTimeout(2000) после загрузки файла. Ревью поймало: тест мог пройти при медленном сервере (успел за 2с) или провалиться при быстром (сервер не вернул ошибку вовремя). Решение: добавить data-testid="upload-error" в production page.tsx, ждать через toBeVisible({ timeout: 10000 }).

---

### 2026-04-01 employee-cabinet / session 3: DB-соединение — проверить до запуска QA волны

**Seen:** 1
**Adapted:** —
**Triad:** QA волна с integration/E2E тестами требующими БД → верифицировать DB-соединение одним ping-запросом ДО запуска тест-сьютов → не тратить QA волну на инфраструктурный блокер
**Context:** Task 14 — все 28 integration-тестов и 12 E2E-тестов заблокированы 28P01 (неверный пароль PostgreSQL в .env). Юнит-тесты (20/20) прошли, но QA волна не могла верифицировать ни один integration AC. Проблема обнаружилась только при запуске тестов, не на этапе подготовки волны.
**Pattern:** Перед запуском integration/E2E тестового сьюта добавь один preflight шаг: `psql $TEST_DATABASE_URL -c "SELECT 1"`. Если падает — остановить волну и устранить инфраструктурный блокер. Это экономит все ресурсы волны и даёт явный диагноз вместо размытого "28 тестов не прошли".
**Scope:** universal
**Category:** sequencing

---

### 2026-04-01 employee-cabinet / session 3: Ad-hoc fix без review — inline review лидом вместо пропуска

**Seen:** 1
**Adapted:** —
**Triad:** ad-hoc fix задача когда инструмент спавнинга агентов недоступен → выполнить inline review лидом (прочитать diff самостоятельно по чек-листу ревьюера) вместо пропуска ревью → не оставлять hotfix в production-ветке без минимальной верификации
**Context:** Task ad-hoc (audit-fixer) — 3 фикса применены корректно, но ревью пропущено целиком из-за недоступности SendMessage tool. В decisions.md зафиксировано "Skipped — SendMessage tool unavailable". Hotfix пошёл в master без ревью.
**Pattern:** Когда spawning tool недоступен — не пропускай ревью, делай его inline: прочитай git diff самостоятельно, проверь по чек-листу code/security reviewer (IDOR, error paths, TypeScript). Это занимает 2-3 минуты и даёт минимальный gate. Запись в decisions.md: "Inline review by lead — SendMessage unavailable".
**Scope:** situational
**Situation:** ad-hoc fix или hotfix при недоступном инструменте спавнинга агентов
**Category:** recovery

---

### 2026-03-30 dashboard-v1 / session 1: Reviewer agents — спавнить после diff, не одновременно с тиммейтом

**Seen:** 1
**Adapted:** —
**Triad:** запуск reviewer-агентов в feature-execution волне → спавнить ревьюеров ПОСЛЕ того как diff готов (после завершения тиммейта), передав diff прямо в промт → не получить ревьюеров что завершились до отправки diff
**Context:** Все 6 ревьюеров (Tasks 1 и 2) были запущены параллельно с тиммейтами. Каждый инициализировался, прочитал контекст, написал "жду diff" — и завершился. Когда тиммейты закончили реализацию, SendMessage был недоступен, ревьюеры терминированы. Тиммейты перешли к self-review.
**Pattern:** Reviewer agents — stateless, не умеют "ждать" в фоне после return. Спавнить их нужно только ПОСЛЕ завершения тиммейта, передавая готовый diff в промт напрямую. Либо — давать diff в промте изначально (если код написан lead-ом).
**Scope:** situational
**Situation:** feature-execution волна с reviewer workflow
**Category:** sequencing

### 2026-03-30 dashboard-v1 / session 1: AC для deploy-задач — включать concurrency guards явно

**Seen:** 1
**Adapted:** —
**Triad:** написание AC для deploy pipeline задачи → явно включить concurrency/idempotency guards (cancel-in-progress, prevent overlapping deploys) в AC → избежать предсказуемых "deviation" записей в decisions.md для best-practice additions
**Context:** Task 2 добавил `concurrency: cancel-in-progress: true` как deviation — guard не был в AC, но стандартен для CI/CD. Агент добавил правильно, но это создало шум в decisions.md.
**Pattern:** В AC задач деплоя явно перечисляй concurrency guards. Эти safeguards предсказуемо нужны для любого CI/CD — их отсутствие в AC означает агент либо забудет их, либо добавит как deviation.
**Scope:** situational
**Situation:** написание AC для задачи создания CI/CD pipeline
**Category:** sequencing

### 2026-03-29 stylist-website / client-edits: Верифицируй результат, а не только изменение

**Seen:** 3 → PROMOTED to feature-execution
**Adapted:** —
**Triad:** создание/изменение артефакта → верифицировать результат в реальной среде перед объявлением "готово" → не объявлять "готово" пока результат не подтверждён
**Context:** (1) Скилл создан в репо, но не попал в runtime. (2) CSS flex-выравнивание добавлено, но цена была вложена слишком глубоко в HTML — flex не мог до неё достать. Дважды сказал "готово", пользователь дважды увидел что ничего не изменилось. (3) 2026-03-31 juridical-parser: пайплайн деплоился без `__main__` блока — крон срабатывал, но процесс сразу выходил. Объявил "деплой работает" не проверив реальный лог.
**Pattern:** После любого изменения — проверь что результат действительно работает в целевой среде. Для cron-деплоев: проверь лог через 5 минут после первого срабатывания. Изменить код ≠ получить результат.
**Scope:** universal
**Category:** sequencing

### 2026-03-28 employee-dashboard / session 3: Build-before-commit при server/client boundary

**Seen:** 3 → PROMOTED to feature-execution
**Adapted:** —
**Triad:** изменение server/client boundary или сигнатуры → запустить build между волнами → поймать type/import violations до QA
**Context:** Tasks 8-9 импортировали getSession() (server-only, uses next/headers) в "use client" pages. Unit-тесты прошли, build сломался. Обнаружено только на QA wave. Ранее: callback type mismatch тоже поймал только build.
**Pattern:** Запускай полный build после каждой волны (не только на QA). Unit-тесты не ловят: server/client boundary violations, callback type mismatches, import ошибки runtime-only модулей.
**Scope:** universal
**Category:** sequencing

### 2026-03-26 mvp-parser / session 1: Retry-декоратор должен знать, что НЕ ретраить

**Seen:** 1
**Adapted:** —
**Triad:** generic retry decorator оборачивает API-вызов → явно исключить non-retryable exceptions → не ретраить ошибки, которые повторятся всегда
**Context:** `retry_with_backoff` ловил все Exception, включая HTTP 429 (quota exceeded). Ревьюер поймал: quota не восстановится через 30 секунд, retry бессмыслен и тратит время. Пришлось менять архитектуру: _request возвращает Response без raise, caller проверяет status code.
**Pattern:** При проектировании retry-обёртки сразу определи список non-retryable исключений. Если декоратор generic (ловит Exception) — добавь параметр `exclude` или проверяй тип перед retry. Retryable = транспортные ошибки + 5xx. Non-retryable = 4xx (quota, auth, not found).
**Scope:** universal
**Category:** tool-selection

### 2026-03-26 tech-spec / meta: Верифицируй API response shapes из code-research

**Seen:** 2
**Adapted:** —
**Triad:** code-research описывает внешний API (методы или response shape) → сделать live call и проверить реальную документацию до включения в спек и написания тестов → предотвратить propagation миражей code-research → tech-spec → implementation → тесты
**Context:** (1) Code-research может содержать неточные описания API — если tech-spec копирует их без проверки, мираж распространяется до реализации. (2) mvp-parser: code-research задокументировал `/stat/` как `{"remaining": N}`. Реальный ответ — `[{"service":"arbitr","month_request_count":2,"month_limit":200,...}]`. Тесты написаны под неверную форму, прошли 100%. Audit-агенты нашли код консистентным. Баг обнаружен только при live testing.
**Pattern:** Перед включением API response shapes из code-research в tech-spec — сделай реальный API call и сверь с документацией. Один live call стоит дёшево, а propagation миража через весь pipeline (spec → code → tests → audit) стоит дорого.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 tech-spec / meta: Error state machine для внешних API

**Seen:** 3 → PROMOTED to tech-spec-planning
**Adapted:** —
**Triad:** спек для интеграции с внешним API → перенести ВСЕ коды ответа И формат данных из документации/code-research в спек → предотвратить пропуск нестандартных ответов API при реализации
**Context:** (1) user-spec court-workdays пропустил isDayOff код 2 и ошибки 100/101/199. (2) tech-spec указал xmlcalendar как JSON, реально — XML. Название "xmlcalendar" буквально содержит "xml", но спек копировал предположение. (3) Ранее: без error state machine исполнители реализуют handling по-своему.
**Pattern:** PROMOTED: При написании спека для внешнего API — перенести ВСЕ коды ответа, формат данных, и edge cases. Сделать live call для проверки формата до включения в спек.
**Scope:** universal
**Category:** information-gathering

### 2026-03-24 payroll-full-calc: Post-deploy UX-правки — это норма

**Seen:** 1
**Adapted:** —
**Triad:** post-deploy verification с пользователем → планировать 2-4 итерации UX-правок как норму → не считать UX-корректировки проблемой процесса
**Context:** 6 post-deploy коммитов с UX-правками (скрыть штрафы, показать обе ставки, авто-перезагрузка, выравнивание, добавить роль ADMIN). Все обнаружены только при live-верификации — user-spec не покрывал UI-детали.
**Pattern:** При post-deploy verification — планировать 2-4 итерации UX-правок. Пользователь видит реальный UI впервые и уточняет требования. Коммитить каждый фикс отдельно для чистой истории.
**Scope:** universal
**Category:** scope-management

### 2026-03-29 design-pipeline-v2: Проверяй все cross-references в сгенерированных задачах

**Seen:** 2
**Adapted:** —
**Triad:** генерация задач из tech-spec → проверять все cross-references (пути файлов через test -e, номера решений, depends_on) → предотвратить битые ссылки в задачах
**Context:** (1) 2026-03-25: task-creator сгенерировал несуществующие пути к файлам и неверные depends_on ссылки в 12 задачах. (2) 2026-03-29: task-creator создал ссылку "Decision 12" в tech-spec с только 10 решениями — номер взят по предположению.
**Pattern:** После генерации задач проверяй все cross-references по source: пути через `test -e`, номера решений — пересчётом по tech-spec, depends_on — что зависимость реально создаёт нужный артефакт. Агент генерирует ссылки по аналогии/предположению, не по факту.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 design-pipeline-v2 / session 6: awk не фейлит pipe — используй [ ... ] для size guard

**Seen:** 1
**Adapted:** —
**Triad:** smoke-команды с проверкой размера файла → использовать `[ $(wc -l < FILE) -lt N ]` вместо awk-условия → предотвратить ложно-проходящий size guard
**Context:** Smoke-команды из tech-spec содержали `wc -l | awk '{if ($1 < 500) print "OK"; else print "OVER LIMIT"}'` — повторились в 4 задачах и Task 8 QA. awk всегда exit 0 (даже когда печатает OVER LIMIT), поэтому smoke всегда проходит.
**Pattern:** Для проверки размера через CLI используй `[ $(wc -l < FILE) -lt N ]` — это bash test, exit 1 при провале. Awk в конце pipe не фейлит pipeline независимо от вывода. Проверяй exit-логику в smoke-командах перед тем как копировать из tech-spec в задачи.
**Scope:** universal
**Category:** sequencing

### 2026-03-26 design-pipeline-v1: AC через артефакты, не через поведение

**Seen:** 1
**Adapted:** —
**Triad:** AC для markdown-only фич → формулировать через наличие конкретных артефактов → сделать AC автоматически проверяемыми
**Context:** User-spec прошёл 2 раунда валидации — AC описывались на уровне поведения агента ("агент предлагает"), а не верифицируемых артефактов. Переписаны в формат "файл X содержит Y".
**Pattern:** При написании AC для markdown-only фич (скиллы, reference-файлы) формулировать критерии через наличие конкретных артефактов: "файл X содержит Y", "SKILL.md содержит шаг Z в Phase N".
**Scope:** universal
**Category:** scope-management

### 2026-03-26 mvp-parser / session 2: HTTP timeout — обязательный параметр

**Seen:** 1
**Adapted:** —
**Triad:** реализация вызовов к внешним сервисам → устанавливать явный timeout на каждый вызов → предотвратить бесконечное зависание pipeline при stale соединении
**Context:** Вызов к внешнему API без timeout привёл к бесконечному зависанию pipeline — сервер начал отдавать ответ, но не завершил передачу.
**Pattern:** При любом вызове к внешнему сервису — устанавливай явный timeout. Отсутствие timeout превращает stale соединение в бесконечное зависание всего pipeline. Это касается HTTP, gRPC, WebSocket, DB-соединений.
**Scope:** universal
**Category:** tool-selection

### 2026-03-26 mvp-parser / session 2: Эскалирующая диагностика перед гипотезой "сервис сломан"

**Seen:** 1
**Adapted:** —
**Triad:** внешний сервис возвращает неожиданный результат → провести эскалирующую диагностику (менять параметры запроса, сравнить с curl, перечитать документацию) → найти рабочий обходной путь через существующие API-параметры, не ждать исправления сервиса
**Context:** parser-api.com обрывал ответ на ~23KB. Агент сначала предположил "API сломан" — пользователь возразил. Последовательная диагностика: разные даты → curl-тест → streaming → повторное чтение docs с нуля → обнаружено, что `Inn` принимает строку, не только ИНН → `Inn=ИП` дало малый ответ → решение: разбить запросы по типу ответчика.
**Pattern:** Когда внешний сервис ведёт себя неожиданно — не объявляй "сервис сломан" без исчерпывающей диагностики: (1) измени параметры запроса, (2) протестируй curl (изолируй Python), (3) перечитай документацию целиком с нуля. Часто fix — это нестандартное использование уже существующего параметра.
**Scope:** universal
**Category:** recovery

### 2026-03-28 bp-pipeline / skeleton-pipe Phase 4: проверять enum-значения при генерации конфигов

**Seen:** 2
**Adapted:** —
**Triad:** генерация конфигурационного файла с enum-полями (frontmatter, YAML, JSON schema) → проверить допустимые значения enum перед записью → избежать невалидных значений, которые выглядят правдоподобно но отклоняются средой
**Context:** (1) В agent-файле записал `model: claude-sonnet-4-6` — выглядит логично, но Claude Code принимает только `sonnet|opus|haiku|inherit`. (2) 2026-04-01 employee-cabinet Task 1: `passWithNoTests: true` добавлен в ProjectConfig — опция валидна только на top-level, не в inline projects. TypeScript поймал при build, но агент уже закоммитил.
**Pattern:** При генерации конфигурационных файлов с enum-полями или вложенными конфигами — не подставляй "логичный" вариант, а проверь список допустимых значений из документации или схемы. "Правдоподобно" ≠ "валидно". Особенно: опции библиотек могут быть валидны на top-level но не в вложенных объектах.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 mvp-parser / session 4: Кэш обработанных записей при работе с платным API

**Seen:** 1 (this feature/session)
**Adapted:** —
**Triad:** платный API с лимитом + данные пересекаются между запусками → кэшировать обработанные записи в БД, пропускать известные → не тратить квоту на уже обработанные данные
**Context:** parser-api.com, 200 квот/месяц, 231 дело/день — без кэша квота сгорает за 1 день полностью. С кэшем (пропуск уже известных case_number) расход падает в 5-7 раз со второго дня.
**Pattern:** При интеграции с любым платным API с лимитом запросов — сразу закладывай кэш обработанных записей в БД. Перед запросом details/enrichment проверяй, есть ли запись в базе. Это не оптимизация, а обязательный паттерн — без него лимит может сгореть за один запуск.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 mvp-parser / session 5: Фильтр по модели знаний читателя при написании документации

**Seen:** 1
**Adapted:** —
**Triad:** написание клиентской документации от имени пользователя → пройти каждый абзац через фильтр «что читатель уже знает / что не может увидеть сам / почему это работает так» → избежать итеративных коррекций от пользователя
**Context:** 5 раундов коррекций на документе для заказчика: (1) забыл упомянуть ООО/АО как запланированные, (2) не объяснил ПОЧЕМУ парсер сам фильтрует по сумме, (3) объяснил размер пакета, который заказчик и так знает, (4) не назвал второй сервис по имени. Все ошибки одной природы — документ описывал систему с точки зрения разработчика, а не с точки зрения читателя.
**Pattern:** При написании клиентской документации делать «reader filter» проход по каждому абзацу: (1) читатель уже это знает? → убрать, (2) видит ли читатель откуда берутся данные? → назвать каждый источник, (3) понимает ли читатель ПОЧЕМУ ограничение существует? → объяснить причину. Режим по умолчанию «описать систему» пропускает все три.
**Scope:** universal
**Category:** communication

### 2026-03-28 ai-dev-methodology / ad-hoc: "Пусто" ≠ "данных нет" — проверь все каналы

**Seen:** 1
**Adapted:** —
**Triad:** запрос данных из внешней системы вернул "пусто" → перечислить и проверить все каналы/endpoints где данные могут храниться → не пропустить данные в альтернативном канале
**Context:** `gh pr list --json comments` вернул 0 комментариев для обоих PR. На самом деле Codex-бот оставил 5 review comments (inline на строках кода). GitHub хранит комментарии в 3 местах: issue comments, PR conversation, PR review comments — каждый со своим API-эндпоинтом. Первый запрос проверил только один.
**Pattern:** Когда запрос к внешней системе вернул пустой результат, но есть основания полагать что данные существуют — не заключай "ничего нет". Перечисли все каналы/endpoints где данные могут храниться (GitHub: issues/comments + pulls/comments + pulls/reviews; Slack: channel + threads; Jira: comments + linked issues) и проверь каждый.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 employee-dashboard / session 3: Auth credentials для импортированных данных

**Seen:** 1
**Adapted:** —
**Triad:** добавление auth flow к данным, импортированным вне seed → проверить что все записи имеют auth credentials → не обнаруживать missing auth на user verification
**Context:** Сотрудники были импортированы на прод вручную (вне seed.ts). При деплое employee-dashboard — credential для Горбунова существовала, но isActive=false. Обнаружено только при user verification ("Доступ заблокирован"). Потребовался debug-скрипт и ручной UPDATE.
**Pattern:** При добавлении auth flow — проверять не только наличие credential records, но и их isActive status. Для данных, импортированных вне стандартного seed — написать миграционный скрипт, который создаёт/активирует credentials.
**Scope:** universal
**Category:** sequencing

### 2026-03-28 performance-review / session 2: Маскируй секреты ДО выполнения команды

**Seen:** 2 → PROMOTED to code-writing
**Adapted:** —
**Triad:** чтение конфигов удалённой системы для диагностики → маскировать секретные поля в самой команде (sed/pipe), не полагаться на пост-обработку → не допустить утечку секретов в персистентные логи сессии
**Context:** (1) При диагностике скорости VPS: `cat .env | grep DATABASE` — пароль PostgreSQL в логах. (2) 2026-03-29: повторно `grep DATABASE_URL .env` на сервере — пароль снова в логах. Два сайта недоступны несколько часов.
**Pattern:** При любом чтении конфигов с удалённой машины — встраивать маскировку прямо в команду (`sed 's/:[^@]*@/:***@/'`). Лучше: проверять наличие переменной без вывода значения (`grep -c`). Никогда не выводить .env, credentials, secrets целиком — даже если кажется что "это только в контексте".
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 performance-review / deploy-fix: Чисти ресурс по identity, не по management context

**Seen:** 1
**Adapted:** —
**Triad:** deploy script с именованным ресурсом (container_name, named volume, PID-файл) → чистить по identity (имя/ID), а не через management tool (compose down) → предотвратить сбой от orphaned ресурса, созданного другим инструментом или прерванным запуском
**Context:** `docker compose -f docker-compose.prod.yml down` не удалял контейнер `analiticxxs-app`, созданный ранее через другой compose-файл или ручной запуск. Deploy падал с "container already exists". Фикс: `docker rm -f analiticxxs-app` перед `compose down`.
**Pattern:** Если deploy/teardown скрипт управляет именованным ресурсом — чисти его напрямую по имени (`docker rm -f`, `rm -f pidfile`, `kill $(cat pidfile)`), а не только через management tool (`compose down`, `systemctl stop`). Management tool знает только о "своих" ресурсах, но ресурс с тем же именем мог быть создан другим способом.
**Scope:** universal
**Category:** sequencing

### 2026-03-28 performance-review / analiticxxs: Timing с первого дня в комплексных проектах

**Seen:** 1
**Adapted:** —
**Triad:** старт комплексного проекта по методологии → включить server action timing (withTiming-обёртка + таблица + UI) в scope MVP → иметь baseline метрик до оптимизаций, видеть деградацию на проде
**Context:** В AnaliticXXS timing добавлен постфактум — после 4 блоков оптимизаций. Baseline "до" потерян, сравнить before/after невозможно. Если бы timing был с MVP — каждая оптимизация имела бы измеримый эффект.
**Pattern:** В комплексных проектах включать server action timing в MVP scope наравне с audit log. Стоимость минимальна (модель + обёртка + 1 страница), а ценность растёт с каждой итерацией: baseline → оптимизации → мониторинг деградации.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 / session 2: Off-by-one в bounded loops — тестировать граничное значение

**Seen:** 1
**Adapted:** —
**Triad:** AC содержит числовую границу (max N iterations/attempts/rounds) → включить граничное значение N в smoke или AC как executable check → поймать off-by-one до code audit
**Context:** design-session-execution Phase 3 Step 4 написан как `< 3` вместо `<= 3`, что даёт только 2 re-spawn вместо заявленных 3. Дефект обнаружен только на wave 3 code audit (Task 5), хотя фича была почти готова.
**Pattern:** Если AC описывает "max N iterations/retries/rounds" — добавь в smoke-команду или в отдельный AC check условие с граничным значением N. Компилятор и unit-тесты не ловят off-by-one в условиях цикла агента; только явный тест на граничное значение даёт гарантию.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 / session 2: TRIZ-идеальность при выборе между эквивалентными фиксами

**Seen:** 1
**Adapted:** —
**Triad:** два варианта фикса корректны, но один требует ручного обновления при эволюции артефакта → применить TRIZ-принцип идеальности — выбрать вариант с нулевой стоимостью обслуживания → не создавать технический долг при исправлении
**Context:** design-done Step 6: зафиксировать ретроспективные артефакты через `git add <specific files>` (точность) vs `git add -A` (идеальность). При росте design-system выходные файлы ретроспективы меняются — `git add <files>` требовало бы ручного обновления скилла при каждом расширении.
**Pattern:** При выборе между двумя корректными исправлениями — оцени стоимость обслуживания каждого через TRIZ-принцип идеальности: выбирай вариант, который не требует изменений при эволюции системы. "Идеальная" система делает своё дело сама, без вмешательства.
**Scope:** universal
**Category:** problem-decomposition

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30) -->

### 2026-03-31 dashboard-v1 / deploy: SSH key auth падает — проверь owner домашней директории

**Seen:** 1
**Adapted:** —
**Triad:** SSH key auth падает несмотря на правильный authorized_keys и PubkeyAuthentication yes → проверить `ls -la ~` — домашняя директория должна принадлежать именно этому пользователю → устранить auth-блокер без изменения sshd_config
**Context:** `authorized_keys` корректен, sshd_config правильный, но домашняя директория `/root/` принадлежала UID 1001. `chown root:root /root` — SSH заработал немедленно.
**Pattern:** При диагностике SSH key auth — после проверки authorized_keys и sshd_config выполни `ls -la ~`. Домашняя директория обязана принадлежать тому пользователю под которым идёт вход. Неправильный owner — частая silent failure на VPS с нестандартной конфигурацией.
**Scope:** universal
**Category:** recovery

### 2026-03-31 dashboard-v1 / deploy: Браузер молчит — смотри server access log до диагностики сети

**Seen:** 1
**Adapted:** —
**Triad:** браузер показывает "не грузит" без ошибки → сразу проверить server access log → узнать реальный HTTP-статус до диагностики firewall/сети
**Context:** Пользователь видел пустой браузер и думал что порт заблокирован. Nginx access log показал 4 запроса с 401 — сервер работал, проблема была в неверном пароле Basic Auth.
**Pattern:** Когда браузер не отвечает — не диагностируй сеть вслепую. Первый шаг: `tail -f /var/log/nginx/access.log`. Если запросы доходят — проблема в приложении. Если запросов нет — проблема в сети.
**Scope:** universal
**Category:** recovery

### 2026-03-30 methodology-sync-sketch / session 1: агент-файл для multi-context — нейтральные сигналы завершения

**Seen:** 1 (methodology-sync-sketch / session 1)
**Adapted:** —
**Triad:** написание агент-файла, который используется и inline, и через spawn_agent → не использовать ссылки на родительский контекст ("return to Phase N"), давать нейтральный сигнал завершения ("task complete. [result]") → артефакт работает корректно в обоих execution environments
**Context:** sketch-interviewer.md написан с `"return to SKILL.md Phase 5"` — это работает в Claude Code (inline load), но ломается в Codex spawn_agent где агент не знает про родителя.
**Pattern:** Когда файл агента предназначен для нескольких execution environments (inline + spawned) — описывать завершение нейтрально: "task complete. [result description]". Вызывающая сторона сама решает что делать дальше. Back-reference на parent step — это coupling на конкретную среду.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 employee-cabinet / session 1: Проверять overlap файлов внутри волны перед финализацией tech-spec

**Seen:** 1
**Adapted:** —
**Triad:** завершение секции Implementation Tasks в tech-spec → проверить "Files to modify" каждой задачи на пересечение внутри одной волны → предотвратить merge-конфликт при параллельном выполнении
**Context:** Tasks 7 и 8 в Wave 3 оба изменяли `cabinet/timesheet/page.tsx`. При параллельном выполнении — гарантированный конфликт. Поймал только template-validator.
**Pattern:** После написания всех задач в волне — прогнать мысленный (или grep-based) check: нет ли двух задач в одной волне с совпадающим файлом в "Files to modify". Если есть — объединить задачи или разнести по волнам.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 employee-cabinet / session 1: File upload в архитектуре требует явного описания file download

**Seen:** 1
**Adapted:** —
**Triad:** проектирование фичи с загрузкой пользовательских файлов на диск → явно определить механизм доставки файлов (protected API endpoint с ownership check, не static) в Architecture секции → предотвратить IDOR через неавторизованный прямой доступ к файлам
**Context:** Tech-spec описывал POST для загрузки PDF-сертификатов, но не описывал как файлы отдаются клиенту. Файлы попали бы в `/uploads/` без auth-защиты. Поймал security-auditor — добавлен новый Task 5.
**Pattern:** Когда фича включает хранение файлов пользователя, upload и download — разные операции с разными требованиями безопасности. В Architecture явно описать оба direction: куда файл попадает при upload И через какой endpoint возвращается при download (с auth check). Статическая раздача файловой директории по умолчанию небезопасна.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 employee-cabinet / session 1: Субагент сообщает о блокере — верифицировать самостоятельно

**Seen:** 1
**Adapted:** —
**Triad:** субагент сообщает о блокере (build failure, missing dep, broken env) как причине незавершённой задачи → запустить ту же команду самостоятельно → не принимать диагноз агента как факт без проверки
**Context:** Task 5 агент заявил "pre-existing build failure (missing admin/timesheets route, unrelated)" и пометил это как не-блокер. Верификация показала: build проходил нормально, никакого pre-existing failure не было. Диагноз агента был ложным.
**Pattern:** Когда субагент сообщает о блокере как оправдании — не принимать этот диагноз как факт. Запустить ту же команду (build, test, curl) самостоятельно. Если блокер не воспроизводится — задача не заблокирована, а агент ошибся в диагностике. "Pre-existing blocker" — распространённый паттерн самооправдания.
**Scope:** universal
**Category:** recovery

### 2026-04-01 employee-cabinet / session 1: Субагент не обновляет frontmatter статус задачи

**Seen:** 1
**Adapted:** —
**Triad:** завершение задачи субагентом → явно обновить `status: done` в frontmatter task-файла как финальный шаг → не накапливать задачи со статусом "planned" требующие ручного batch-обновления от лида
**Context:** Tasks 2, 4, 5, 6, 7 оставлены со статусом "planned" после выполнения — агенты обновляли decisions.md, но не трогали task frontmatter. Лид обнаружил при wave transition и обновлял вручную партиями.
**Pattern:** В промт каждого teammate явно добавить шаг "обновить `status: planned → done` в frontmatter task-файла". Это не опциональная административная работа — без этого lead не может определить состояние фичи без ручного просмотра. Включить в commit flow перед reporting completion.
**Scope:** universal
**Category:** sequencing

## Situational

Patterns that apply only in specific contexts. Each has a `Situation` field describing when it's relevant.

<!-- Append situational patterns below -->

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30) -->

### 2026-03-31 dashboard-v1 / session 3: Local-first режим — уточнить среду деплоя до запуска deploy-pipeline

**Seen:** 1
**Adapted:** —
**Triad:** pre-deploy QA завершён, пользователь в local-first / sketch режиме → уточнить желаемую среду верификации ДО запуска deploy wave → не готовить VPS-деплой для пользователя который не планирует его сейчас
**Context:** Task 12 (Deploy) запустился по плану волны. Только после попытки настройки выяснилось: нет remote, нет GitHub, нет секретов — пользователь сказал "пока размещаем локально". Создан GitHub репо, код запушен, но VPS-деплой отложен. Волна 7-8 зафиксирована как deferred.
**Pattern:** Перед запуском deploy wave уточнить у пользователя: "Деплоим сейчас на VPS или оставляем локально?" — особенно в sketch/local-first проектах. GitHub + deploy.yml можно настроить в любой момент; principal goal — working local result.
**Scope:** situational
**Situation:** sketch-mode или local-first фичи, где пользователь не заявил явного намерения деплоить
**Category:** communication

### 2026-03-26 shift-confirmation: Ошибки повторяются между волнами

**Seen:** 1
**Adapted:** —
**Triad:** ревью нашло паттерн ошибки (не разовый баг) → добавить предупреждение в промт следующего teammate → предотвратить повторение ошибки в следующих задачах
**Context:** В Task 1 ревьюер нашёл `confirmationStatus: string` вместо enum. Исправили. В Task 4 — ровно та же ошибка. Агент Task 4 не знал о находке Task 1, т.к. каждый teammate с чистым контекстом.
**Pattern:** Когда ревью находит паттерн ошибки (не разовый баг), lead добавляет предупреждение в промт следующего teammate: "В предыдущих задачах ревьюеры находили [X] — убедись, что новый код не повторяет эту ошибку."
**Scope:** situational
**Situation:** multi-agent feature execution с несколькими волнами
**Category:** communication

<!-- PROMOTED → code-writing (Seen: 2, 2026-03-30) -->

### 2026-03-26 shift-confirmation: Known-issues реестр для аудитов

**Seen:** 1
**Adapted:** —
**Triad:** security/code audit в multi-task feature → вести known-issues.md, аудитор читает перед ревью → не тратить время на повторный репорт известных проблем
**Context:** Security auditor нашёл IDOR в `markEvent()` при ревью Task 2. Та же находка повторилась в audit wave. Нет реестра известных проблем — тратит время на уже известное.
**Pattern:** Завести `known-issues.md` на уровне проекта. Перед ревью агент читает его и пропускает задокументированные проблемы.
**Scope:** situational
**Situation:** multi-task features с security/code audit
**Category:** information-gathering

### 2026-03-28 mvp-pipeline-core + mvp-parser: Тесты на моках скрывают расхождение с реальным внешним процессом

**Seen:** 2
**Adapted:** —
**Triad:** unit-тесты с моками для внешнего процесса/API → провести минимум 1 live smoke-прогон перед объявлением QA passed → предотвратить ложное "all tests pass" при расхождении мока и реальности
**Context:** (1) mvp-parser: 75 тестов pass, но реальный API возвращал другую структуру. (2) mvp-pipeline-core: 77 тестов pass, QA passed — но реальный `claude -p` вернул JSON в envelope + markdown fences + свой формат полей. 7 fix-коммитов после "успешного" QA.
**Pattern:** Перед объявлением QA passed — сделать минимум 1 live прогон с реальным внешним процессом (API/CLI). Не доверять мокнутым тестам для валидации интеграции. Сохранить реальный ответ как golden fixture.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 mvp-parser / live-test: Программное создание документа — зачищай дефолтные артефакты

**Seen:** 1
**Adapted:** —
**Triad:** программное создание документа через API → после создания кастомного контента удалить дефолтные артефакты → не оставлять мусор в финальном документе
**Context:** При создании spreadsheet через API дефолтный лист остался пустым рядом с кастомными вкладками. Проверка пустоты по техническому свойству (row_count) не сработала — свойство имеет ненулевой default. Фикс: идентифицировать дефолтные артефакты по имени.
**Pattern:** При программном создании документа через API — проверить какие дефолтные элементы создаются автоматически и зачистить их после наполнения кастомным контентом. Идентифицировать дефолтные элементы по имени/типу, не по содержимому (пустота может не определяться из-за default-значений).
**Scope:** universal
**Category:** tool-selection


<!-- PROMOTED → feature-execution SKILL.md (2026-03-30, Seen: 2) -->

### 2026-03-28 bp-pipeline / skeleton-pipe: Язык пользователя, не профессиональный жаргон

**Seen:** 1
**Adapted:** —
**Triad:** обсуждение решений с пользователем → использовать язык и терминологию пользователя, расшифровывать каждый термин → ускорить принятие решений, не тратить время на "а что это значит?"
**Context:** Спорные пункты pipeline.md были описаны с аббревиатурами (T1/T2/T3, ICE, severity levels). Пользователь сказал: "я не знаю что такое Т1, ты знаешь, не сокращай ничего". После переформулирования простым языком — все 6 решений приняты за один раунд.
**Pattern:** При обсуждении решений с пользователем — каждый термин расшифровывать при первом упоминании, объяснять последствия на примерах из его домена. Если пользователь хоть раз спросил "что это?" — это сигнал переключиться на простой язык для ВСЕХ последующих обсуждений.
**Scope:** universal
**Category:** communication

### 2026-03-31 dashboard-v1 / session 3: CSS position:fixed провалился на React inline style — зеркаль JS-паттерн соседнего компонента

**Seen:** 1
**Adapted:** —
**Triad:** CSS `position: fixed` не применяется к компоненту с React inline `style={{ display: "none" }}` → использовать JS `isMobile` state с resize listener (зеркально существующему компоненту) → не тратить раунды на CSS, который не может надёжно переопределить React inline style
**Context:** mobile-nav в App.jsx имел `style={{ display: "none" }}` с переопределением через `@media { .mobile-nav { display: flex !important; position: fixed; } }`. Пользователь подтвердил: вкладка находится не внизу viewport, нужно прокрутить страницу. При этом ProjectModal уже использовал `isMobile = useState(() => window.innerWidth <= 640)` + useEffect resize listener. Фикс: применить тот же паттерн к nav div, убрав CSS-подход.
**Pattern:** Когда CSS медиа-запрос должен переопределить React inline style (особенно `position: fixed`) — не полагайся на CSS `!important`. Вместо этого используй JS state `isMobile` с `window.addEventListener("resize", ...)` и прямые inline styles. Этот паттерн уже реализован в модалках — зеркаль его.
**Scope:** universal
**Category:** recovery

### 2026-03-27 mvp-parser / live-test: Проверить стоимость retry до включения

**Seen:** 1
**Adapted:** —
**Triad:** API с лимитом запросов + retry decorator → проверить считаются ли неудачные запросы в лимит ДО включения retry → не сжечь квоту на бессмысленные повторы
**Context:** retry_with_backoff на parser-api.com сжёг 51 запрос из 200/месяц за одну сессию. Каждый обрыв соединения (ConnectionError, ReadTimeout) = запрос списан. Документация не указывает, считаются ли failed requests. Предположение "считаются только успешные" оказалось ложным.
**Pattern:** Перед добавлением retry на API с жёстким лимитом, сделать 2-3 тестовых запроса и сверить счётчик через /stat/ (или аналог). Если failed считаются — retry убрать или ограничить 1 попыткой.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 mvp-parser / session 3: Согласуй структуру выходного артефакта до реализации

**Seen:** 1
**Adapted:** —
**Triad:** требования к формату выходных данных поступают итеративно → согласовать полную структуру на макете до написания кода → не переписывать реализацию на каждое уточнение
**Context:** Структура экспорта менялась 4 раза за сессию. Каждое изменение = переписывание export + query + тесты.
**Pattern:** Когда фича генерирует выходной артефакт для заказчика — показать пример на 2-3 строках и получить подтверждение структуры ДО реализации. Цена согласования минимальна, цена переделки кратна количеству итераций.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 design-pipeline-v2 / techspec: Verify-smoke для markdown — проверяй структуру, не ключевые слова

**Seen:** 1
**Adapted:** —
**Triad:** verify-smoke для markdown-артефакта (SKILL.md, шаблон) → проверять структурные элементы (фазы, ссылки на файлы, guard-ы), не просто ключевые слова → убедиться что артефакт полноценный, а не stub с нужными словами
**Context:** Изначально verify-smoke для ~180-строчного deep skill содержал 2 grep-проверки (имя скилла + слово "Phase"). Test reviewer справедливо указал: SKILL.md из одной строки с этими словами пройдёт проверку. После фикса — 6-8 проверок: Phase 0, Phase 2, ссылки на input-файлы, corruption guard.
**Pattern:** Для markdown-only артефактов verify-smoke должен проверять не наличие слов, а структурные элементы: (1) множественные фазы по номерам, (2) ссылки на input/output файлы, (3) guard-ы для edge cases, (4) resolution ссылок на reference-файлы. Количество проверок пропорционально размеру артефакта.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 design-pipeline-v2 / userspec: Генерируй все шаги deliverable целиком, не только ближайший

**Seen:** 3
**Adapted:** —
**Triad:** создание multi-step deliverable (план, roadmap, серия промптов) → сгенерировать все шаги целиком, не только ближайший → не заставлять пользователя ловить недостающие части
**Context:** Создал промпт только для Session 1 из 6. Пользователь сразу заметил что промпт для Session 2 будет некорректным. Пришлось создавать session-roadmap.md со всеми промптами — то, что нужно было сделать сразу.
**Pattern:** Когда deliverable состоит из нескольких шагов (серия промптов, roadmap, план сессий) — генерировать ВСЕ шаги сразу, даже если пользователь явно просил только следующий. Предвидеть проблему устаревания, а не ждать пока пользователь её поймает.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 analiticxxs / perf-fix: Проверяй дефолты библиотек до оптимизации кода

**Seen:** 1
**Adapted:** —
**Triad:** performance problem на сервере с низким трафиком → проверить дефолтные таймауты/лимиты connection pool и кэшей → найти root cause в конфигурации до оптимизации кода
**Context:** TTFB 7-23 секунд на Next.js SSR. Инстинкт — искать тяжёлые запросы, N+1, SSR complexity. Реальная причина: pg Pool `idleTimeoutMillis: 10000` (дефолт) — на low-traffic сервере ВСЕ соединения закрывались каждые 10 секунд, каждый запрос = DNS + TCP + PG handshake. Фикс: одно число `10000 → 60000` = TTFB с 7-23 сек до 196 мс.
**Pattern:** При performance-проблемах на low-traffic серверах — первым делом проверять дефолтные таймауты и лимиты библиотек (connection pool idle timeout, cache TTL, keepalive). Одно число в конфиге часто даёт больше, чем рефакторинг запросов.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / techspec: Файловые пути — верифицировать, не угадывать (PROMOTED)

**Seen:** 2 → PROMOTED → tech-spec-planning
**Adapted:** —
**Triad:** написание файловых путей в tech-spec или skill из памяти/docs → верифицировать через ls/glob или прочитать source-файл → не допустить неверных путей в artifacts
**Context:** (1) design-task-decompose: путь к session-plan.md указан по аналогии, реальный путь отличался. (2) methodology-sync-sketch: tech-spec написал `~/.claude/skills/shared/work-templates/`, реальный — `~/.claude/shared/work-templates/`. Оба поймал mirage detector в validation round 1.
**Pattern:** Перед написанием любого файлового пути в tech-spec — верифицировать ls/glob. Architecture docs описывают намерение, а не факт filesystem.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 fix-knowledge-pipeline / decompose: Заменяй межзадачную зависимость на общий source of truth

**Seen:** 1
**Adapted:** —
**Triad:** задача в одной волне ссылается на результат другой задачи той же волны → заменить зависимость на чтение общего source of truth (decisions.md, tech-spec.md) → сохранить параллельность волны без рисков read-after-write
**Context:** Task 2 (align retrospective) ссылалась на quick-learning/SKILL.md "after Task 1 modifies it", но обе задачи в Wave 1 (параллельно). depends_on: [1] + wave: 1 — противоречие. Решение: Task 2 читает decisions.md напрямую (те же решения, но source of truth, а не output другой задачи). Зависимость убрана, параллельность сохранена.
**Pattern:** При декомпозиции на параллельные задачи — если задача "читает результат другой" в той же волне, заменить зависимость на чтение общего документа (decisions.md, tech-spec.md). Если это невозможно — перенести задачу в следующую волну. Третьего не дано: depends_on + same wave = гонка данных.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 missing-ui-details / wave-2: Сверяй типографику с референсом ДО реализации

**Seen:** 1
**Adapted:** —
**Triad:** визуальная задача с референс-скриншотами → сверить типографику (шрифт, вес, размер, padding) с референсом ДО написания CSS → избежать серии итеративных fix-коммитов по визуальному несоответствию
**Context:** Task 2 (visual polish) выполнен по спеку, но спек не описывал конкретный шрифт и пропорции. Пользователь увидел несоответствие — 9 fix-коммитов подряд: condensed шрифт, +20% размер, padding, кнопки, единообразие строк. Каждый fix был очевиден при сравнении с референсом.
**Pattern:** Перед реализацией визуальной задачи с референсами — открыть скриншот и составить чеклист: шрифт (семейство, condensed/normal), размеры относительно строки, вес, межстрочные отступы, цвет акцентов. Реализовывать по чеклисту, не по абстрактному описанию в спеке.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 pipeline-stabilization / session 1: Перед ревью — проверить артефакты удаления

**Seen:** 1
**Adapted:** —
**Triad:** задача на удаление фичи/константы/поля → перед отправкой на ревью проверить dead variables, stale comments, duplicate tests от удалённого кода → не тратить review-раунд на предсказуемые артефакты удаления
**Context:** Task 1 удалил MAX_OUTPUT_CHARS и два поля из REQUIRED_FIELDS. Task 2 удалил extended mode и wave-поля. Все 6 ревьюеров нашли только minor-находки: мёртвая переменная `missing` (ссылалась на удалённый check), stale-комментарии с "extended", дублирующийся тест (старый обновлён до пустого набора — совпал с новым TDD-тестом). Все предсказуемы.
**Pattern:** После задачи на удаление — перед отправкой на ревью пройти чеклист: (1) dead variables/imports, ссылающиеся на удалённый код, (2) комментарии/docstrings, упоминающие удалённую функциональность, (3) тесты, ставшие дублями или тестирующие удалённое поведение. Три минуты проверки экономят review-раунд.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 pipeline-stabilization / session 2: При редактировании AI-промтов — явно проверять emphasis-framing

**Seen:** 1
**Adapted:** —
**Triad:** редактирование/компрессия AI-промта → явно проверить все prohibition/caps формулировки ("НЕЛЬЗЯ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО") и заменить на motivation-framing → не тратить review-раунды на предсказуемую emphasis-ошибку
**Context:** Tasks 4, 5, 6 (компрессия agent-04..10) — три задачи подряд получили major-находку от prompt-reviewer: prohibition lists и капслок ("СТРОГО СОБЛЮДАЙ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО"). Паттерн повторился во всех трёх задачах. Все найдены в одном review-раунде и исправлены в одном коммите.
**Pattern:** При редактировании или компрессии AI-промтов — добавить финальный чеклист перед ревью: (1) найти все КАПСЛОК-заголовки, (2) найти все формулировки "нельзя/запрещено/жёсткие/строгие", (3) заменить на мотивационное обоснование ("чтобы X, делай Y" вместо "ЗАПРЕЩЕНО делать Y"). Prohibition-framing — предсказуемая находка в любом AI-промте.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 fix-knowledge-pipeline: Overflow-политика при распределении в capped buckets

**Seen:** 1
**Adapted:** —
**Triad:** алгоритм распределяет записи по bucket-ам с max-cap → определить overflow-политику (куда идут записи сверх лимита) до реализации → не терять записи при заполнении bucket-а
**Context:** Task 5 генерировал per-skill quick-ref файлы с лимитом 10 записей. quick-ref-feature-execution.md заполнился (10 записей из sequencing/recovery/communication), запись #32 была молча отброшена. Reviewer обнаружил: #32 должна попасть в do-task (overflow bucket). Задача не описывала overflow-поведение.
**Pattern:** При реализации алгоритма "распределить N элементов по M buckets с max-cap" — явно определить политику overflow до написания кода: (1) куда попадают элементы сверх cap (следующий bucket, default bucket, ошибка), (2) как проверить что ни один элемент не потерян. Без явной политики реализатор молча выбросит overflow.
**Scope:** universal
**Category:** tool-selection

### 2026-03-29 design-pipeline-v2 v2.3 / session 1: При cross-domain адаптации шаблона — проверять совместимость каждого поля

**Seen:** 1
**Adapted:** —
**Triad:** адаптация шаблона задачи из одного домена в другой → проверить каждое поле frontmatter на применимость к целевому домену → не исправлять domain-несовместимые defaults отдельной задачей после деплоя
**Context:** design-task.md.template был создан в v2.2 по образцу task.md.template. Поле `reviewers: [skill-checker]` скопировано из code-domain шаблона — там оно осмысленно. В design-domain quality gate — user visual review, не skill-checker. Несовместимость обнаружена при написании tech-spec v2.3 и потребовала отдельной Task 2 в следующей версии.
**Pattern:** При адаптации шаблона из одного домена в другой — пройти каждое поле frontmatter через вопрос "это поле имеет смысл в целевом домене?". Если нет — изменить default прямо при адаптации, не копировать как есть. Несовместимые defaults, скопированные "на потом", становятся отдельными задачами в следующей итерации.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 design-pipeline-v2 v2.3 / task-decomposition: Пилотная задача перед массовой генерацией по новому шаблону

**Seen:** 1
**Adapted:** —
**Triad:** массовая генерация задач по шаблону, применяемому к новому домену впервые → сначала 1 пилотная задача → проверить и валидировать → масштабировать на все задачи → не накапливать 30+ правок при первом прогоне
**Context:** task-creator сгенерировал 8 задач по design-task.md.template за один прогон. Validation round 1 дал 30+ находок (несовместимые поля, неверные пути, domain-mismatch в reviewers). Если бы задача 1 была проверена первой — паттерн ошибок был бы найден до масштабирования на 7 оставшихся.
**Pattern:** При первом применении шаблона к новому домену — сгенерировать 1 пилотную задачу, прогнать через валидатор, зафиксировать все несоответствия. Только после успешной пилотной — генерировать остальные. Стоимость пилота минимальна; стоимость 30+ правок в 8 задачах — в 8 раз выше.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 pipeline-stabilization / session-3: Security severity привязывается к модели развёртывания

**Seen:** 3 → PROMOTED to security-auditor
**Adapted:** —
**Triad:** security audit находит medium-уязвимости в локальном CLI-инструменте → классифицировать как non-blocking с явным условием "до перехода на service/multi-user деплой" → не блокировать релиз по находкам нерелевантным текущей модели развёртывания
**Context:** Task 9 нашла 3 medium-находки (отсутствие hard-limit на --text, произвольный --data-dir, отсутствие size limits на validator fields). Все три реальны и требуют fix — но только перед service deployment. Для single-user CLI они не создают угрозы.
**Pattern:** При аудите безопасности явно привязывать severity к модели развёртывания. Medium-находка в single-user CLI и medium-находка в multi-user service — разные приоритеты. Записывать условие перехода ("before service deployment") прямо в статус задачи, не только в comments.
**Scope:** situational
**Situation:** инструмент развёртывается как локальный CLI для одного пользователя; есть планы перейти на service-модель
**Category:** scope-management

<!-- PROMOTED → task-decomposition (Seen: 2, 2026-03-30) -->

### 2026-03-29 pipeline-stabilization / session-3: QA разделяет failed и deferred

**Seen:** 1
**Adapted:** —
**Triad:** QA-критерий требует live-вызова внешнего сервиса (LLM, API, DB) недоступного в test-среде → отметить как deferred с явным условием, не как failed → получить чистый QA pass на автоматизируемых критериях без блокировки
**Context:** Task 11 (pre-deploy QA) прошла 20 из 22 критериев. 2 оставшихся требуют live Claude CLI вызова с активной подпиской. Вместо fail или skip — deferred с записью в deferredToPostDeploy, что даёт чёткий план для post-deploy verification.
**Pattern:** В QA-отчёте явно разделять три статуса: passed, failed, deferred. Deferred — критерий, истинность которого не может быть проверена автоматически (требует live-среды, подписки, внешнего пользователя). Deferred не блокирует релиз, но создаёт обязательный чеклист для post-deploy. Не смешивать с "не успели проверить".
**Scope:** universal
**Category:** sequencing

### 2026-03-29 analiticxxs / recovery: Давай команды по одной нетехническому пользователю

**Seen:** 1
**Adapted:** —
**Triad:** нетехнический пользователь выполняет команды на сервере по инструкции → давать по одной команде с явным "запусти, скажи результат" между шагами → предотвратить вставку блока в неправильный контекст
**Context:** Пользователь вставил весь блок команд (read + ALTER USER + python3 + pm2) прямо в psql вместо bash. В результате пароль postgres установлен буквально как "$NEWPASS" вместо реального значения.
**Pattern:** Когда пользователь выполняет команды на сервере вручную — никогда не давать блоки. Давать ровно одну команду, ждать вывода, убедиться что контекст правильный, только потом следующую.
**Scope:** situational
**Situation:** нетехнический пользователь выполняет команды на сервере (psql, bash, python repl)
**Category:** communication

### 2026-03-30 design-pipeline-v2 v2.3: Граничное условие счётчика — верифицируй против спецификации

**Seen:** 2
**Adapted:** —
**Triad:** написание числовой логики с граничным условием (max N повторений, retry limit, iteration cap) → сразу подставить граничное значение и убедиться что условие выполняется ровно N раз → не пропустить off-by-one через code review
**Context:** Wave-итерации в design-session-execution: counter=1, условие `< 3` — вместо 3 re-spawn получилось 2. Decision 9 требовал max 3 итерации. Code audit (HIGH finding) поймал; обычный review не заметил бы. Fix: `< 3` → `<= 3`.
**Pattern:** При написании логики "повторять максимум N раз" — сразу подставить граничное значение и посчитать итерации вручную: если counter=1, то `<= N` даёт N итераций, `< N` даёт N-1. Off-by-one визуально неотличим от правильного кода — review ловит редко.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: git add scope должен покрывать все write locations скилла

**Seen:** 1
**Adapted:** —
**Triad:** скилл или агент делает commit и пишет файлы в несколько директорий → перечислить все write locations из тела скилла перед написанием git add → не потерять файлы вне основного дерева при коммите
**Context:** design-done: `git add work/completed/{feature}/` не захватывал `.design-system/` файлы, которые design-retrospective пишет в корне проекта. Архивный коммит был неполным. HIGH finding на code audit; fix: `git add -A`.
**Pattern:** При написании шага commit в скилле — просмотреть все фазы, которые пишут файлы, и составить список write locations. Если хотя бы одна запись происходит вне основной директории — использовать `git add -A`. Path-specific `git add` скрыто ломается при добавлении новых write locations в будущем.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: TRIZ для выбора между равнозначными вариантами фикса

**Seen:** 1
**Adapted:** —
**Triad:** два варианта фикса дают одинаковый результат но отличаются по устойчивости к будущим изменениям → применить tradeoff-анализ (minimal diff vs systemic robustness) → выбрать вариант с меньшим coupling к текущим деталям реализации
**Context:** HIGH #1: `< 3` vs `counter=0` — оба дают 3 итерации, но `<= 3` семантически точнее и ближе к спецификации. HIGH #2: `git add work/completed/` vs `git add -A` — оба фиксируют текущие файлы, но `-A` устойчив к добавлению новых write locations. Оба выбора сделаны за один раунд без обсуждения.
**Pattern:** Когда два варианта фикса технически корректны — проверить: (1) какой вариант продолжает работать при изменении смежного требования, (2) какой вариант создаёт меньше implicit coupling с деталями реализации. Выбрать более устойчивый даже если diff чуть больше.
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 agent-research-prompt-fix userspec: поведение агента после пропуска — логика, не маркер

**Seen:** 1
**Adapted:** —
**Triad:** описание skip-поведения агента при пустом user input → явно описать что агент ДЕЛАЕТ после пропуска (продолжает анализ), не только какой маркер ставит в поле → не допустить реализации label-swap без изменения логики
**Context:** Спек описывал [ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ] как замену [НЕТ ДАННЫХ]. Пользователь уточнил: агент должен реально завершить анализ с имеющимися данными, а не просто переименовать заглушку. Разница критическая для реализации.
**Pattern:** Когда описываешь поведение агента при пустом/пропущенном вводе — формулируй не только output marker, но и processing logic: "агент продолжает анализ с тем, что есть, и помечает только вычислительно недостижимые поля". Без явной processing logic разработчик реализует label-swap.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix userspec: active + planned stubs для многочастного скопа

**Seen:** 1
**Adapted:** —
**Triad:** user spec вырастает до 3+ последовательно зависимых deliverable разного размера → оставить первый deliverable active draft, остальные создать как planned stubs → пользователь видит прогресс на каждой части и контекст постфич сохранён
**Context:** Спек начался как 3 пункта, вырос до 4, потом пользователь попросил разбить "чтобы видеть прогресс". Создали 3 отдельных файла: part1 (active/approved), part2+3 (planned). Части 2 и 3 полностью проработаны для контекста, но не запускаются сразу.
**Pattern:** Если feature вырастает до 3+ частей с чёткими зависимостями — не пытайся уместить всё в один спек. Создай первую часть как active draft, остальные как planned stubs с полным описанием. Это даёт видимость прогресса без потери плана. Planned stubs не требуют повторного интервью при запуске.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 design-v2 / session 1: Зона субъекта фото — до расстановки UI overlay

**Seen:** 1
**Adapted:** —
**Triad:** размещение текста/UI поверх full-bleed фото → определить зону субъекта в кропированном вьюпорте ДО расстановки элементов → не перекрыть лицо/объект текстом
**Context:** Hero с portrait фото в landscape viewport — текст был поставлен по центру экрана и накрыл лицо стилиста. Потребовался полный редизайн grid-структуры.
**Pattern:** Перед расстановкой UI-элементов поверх фото — вычислить где окажется субъект после object-fit cover кропа. Portrait в landscape → субъект всегда около горизонтального центра. Текст ставить только в негативное пространство: низ (bottom gradient zone), крайний угол или зону без субъекта.
**Scope:** situational
**Situation:** Hero или full-bleed секция с фото, поверх которой размещаются текст или UI-блоки
**Category:** design-process

### 2026-03-30 design-v2 / session 1: Редизайн = независимый выбор layout, не наследование структуры

**Seen:** 1
**Adapted:** —
**Triad:** задача "альтернативный дизайн" или "редизайн существующей страницы" → выбирать layout pattern независимо от существующей верстки → получить реальную альтернативу, а не ресайн с другими цветами
**Context:** Первый preview был отклонён ("всё ещё сильно основан на прошлой версии") — структура 50/50 split была перенесена из v1, изменены только шрифты и цвета.
**Pattern:** При задаче редизайна — не смотреть в существующий CSS/HTML при выборе layout. Начинать с вопроса: "как принципиально иначе можно показать этот контент?" Только после независимого решения сверяться с существующим кодом для понимания контента (тексты, фото), но не структуры.
**Scope:** situational
**Situation:** Задача создать v2, альтернативный вариант или редизайн существующей страницы
**Category:** design-iteration

### 2026-03-30 methodology-sync-sketch / session 1: Классификация глубины diff до написания sync scope

**Seen:** 1
**Adapted:** —
**Triad:** планирование синка файлов между двумя версиями одного репо → запустить code-research для классификации глубины различий до написания scope → не описывать в AC механический синк который требует ручного ревью каждого файла
**Context:** Планировали синк 26 скиллов в Codex через замену путей (.claude/→.agents/). Code-research показал что 24 из 26 имеют реальные content-различия (feature-execution переписан под spawn_agent API) — scope пришлось полностью переписать.
**Pattern:** Перед тем как включить cross-repo sync в scope спека — запустить code-research с вопросом "path-only diff или content diff?". Если content diff > 50% файлов — это не механическая задача, это ручной ревью. Отдельная фича.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / session 1: Итеративная классификация доменов в mono-repo

**Seen:** 1
**Adapted:** —
**Triad:** репо содержит скиллы из нескольких доменов → явно перечислить каждый домен и получить is_in_scope per domain до написания спека → не переписывать scope в 3 итерации из-за постепенного уточнения границ
**Context:** Один репо содержит методологию, дизайн-пайплайн, promoter, skeleton-pipe, sketch. Уточнения "это отдельный пайплайн" происходили трижды (design → promoter/skeleton → уточнение что sketch ВХОДИТ). Каждый раз — реакция на вопрос.
**Pattern:** При старте user-spec для проекта с несколькими доменами — сразу предъявить полный список всего что есть в репо и попросить пометить каждый домен: in/out/separate. Одним вопросом, а не серией уточнений.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 agent-research-prompt-fix / session 2: верифицировать содержимое каждого целевого файла перед описанием операции

**Seen:** 2 (agent-research-prompt-fix × 2)
**Adapted:** —
**Triad:** spec (user, tech, task) называет набор файлов и описывает трансформацию → верифицировать каждый файл на наличие изменяемого элемента → не допустить ошибочный тип операции (replace вместо add)
**Context:** (1) User-spec назвал "runner.py" и "счётчик уже есть" — неточные утверждения, пойманы code-research. (2) Tech-spec описал "убрать [НЕТ ДАННЫХ] из всех 9 промптов" — agent-03 этой строки не содержит, нужна другая операция (add instruction). Поймано reality-checker при декомпозиции.
**Pattern:** Любой spec-артефакт (user-spec/tech-spec/task) доверяет, что файлы содержат описываемый элемент. Перед тем как зафиксировать "удалить X" или "заменить X" — grep по каждому целевому файлу. Файлы без X требуют операции add, не replace. Ошибка типа операции обнаруживается только при выполнении.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix / session 2: тест с точной строкой-маркером создаёт неявный depends_on

**Seen:** 1 (agent-research-prompt-fix)
**Adapted:** —
**Triad:** задача содержит тест с точной строкой-маркером определённой в другой задаче → объявить depends_on на задачу-источник даже если строка — литерал → не пропустить неявную зависимость через разделённый дизайн-маркер
**Context:** Task 4 содержала `test_propushcheno_not_pipeline_defect` ассертящий на `"[ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ]"`. Строка определяется в Task 2 (pipeline.py). Task 4 объявила only `depends_on: [1]`. Индивидуальные валидаторы пропустили — cross-task валидатор поймал.
**Pattern:** Если задача содержит тест ассертящий на конкретную строку/константу/маркер — проверить: кто принял дизайн-решение об этой строке? Задача-источник должна быть в depends_on даже если строка используется как литерал а не импортируется.
**Scope:** situational
**Situation:** multi-task декомпозиция с sentinel strings / protocol markers общими между задачами
**Category:** problem-decomposition

### 2026-03-30 methodology-sync-sketch / techspec: Каталог скиллов — читай ДО написания задач

**Seen:** 1
**Adapted:** —
**Triad:** написание секции Implementation Tasks в tech-spec → прочитать skills-and-reviewers.md перед заполнением Skill и Reviewers → не использовать несуществующие или неверные skill-имена
**Context:** Tasks 1-5 использовали `write-code` (wrapper) вместо `skill-master`, `documentation-writing`. Template-validator поймал в validation round 1 — потребовал полный перезаголовок задач.
**Pattern:** Перед написанием Implementation Tasks — открыть `tech-spec-planning/references/skills-and-reviewers.md`. Wrapper-skills (`write-code`, `new-tech-spec`) не являются execution skills. Всегда проверять: skill в tasks = строка из каталога, не интуитивный псевдоним.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 pipeline-report / decompose: TDD Anchor для private метода — вызов через инстанс

**Seen:** 1
**Adapted:** —
**Triad:** TDD Anchor описывает тест для private метода класса → указывать вызов через инстанс объекта, не через прямой импорт → тесты не падают с ImportError до запуска реальной логики
**Context:** task-creator написал TDD Anchor с инструкцией `import _generate_report from bp_pipeline.pipeline`. Private метод нельзя импортировать напрямую — reality-checker поймал как critical. Правка: `pipeline_instance._generate_report(session, session_dir)`.
**Pattern:** В TDD Anchor для private/protected метода — явно указывать паттерн доступа: создать инстанс класса, вызвать `instance._method()`. Не писать `from module import _method` — это ImportError. Актуально для любого языка с private convention (Python `_`, JS `#`).
**Scope:** situational
**Situation:** task-creator генерирует TDD Anchor для private метода класса
**Category:** problem-decomposition

### 2026-03-30 design-v2-stylist / session 2: Совместимость фото с контейнером — проверять до CSS

**Seen:** 1
**Adapted:** —
**Triad:** выбор лейаута с full-bleed фото → проверить ориентацию фото и кадрирование субъекта против формы контейнера ДО написания CSS → не тратить итерации на геометрически невозможный кроп
**Context:** Портретное фото стилиста (субъект стоит в полный рост на фоне яркого окна) поставили в 50vh landscape-баннер. Ни один Y не мог показать субъекта — это геометрический факт определяемый до верстки. Понадобилось 3 итерации и полная переделка лейаута.
**Pattern:** Перед вёрсткой секции с фото: (1) посмотреть фото через Read, (2) проверить ориентацию (portrait/landscape), (3) оценить где субъект в кадре (верх/центр/низ, % от края), (4) сопоставить с контейнером. Если субъект занимает <30% ширины landscape-контейнера или фото portrait при контейнере landscape — сменить лейаут на тот, который сохраняет пропорцию.
**Scope:** situational
**Situation:** верстка секций с фотографиями в фиксированных контейнерах (hero, banner, split)
**Category:** design-process

### 2026-03-30 design-v2-stylist / session 2: Структурированные данные → UI напрямую

**Seen:** 1
**Adapted:** —
**Triad:** верстка контентной секции из структурированных данных пользователя → маппировать каждое поле данных в UI-элемент напрямую → не изобретать структуру отображения которая расходится с источником
**Context:** Пользователь прислал услуги в формате: название → суть → цена → буллеты. Вместо прямого маппинга была создана отдельная таблица-индекс + аккордеон с другими именами. Потребовались 2 раунда переделки пока структура не совпала с источником.
**Pattern:** Получив от пользователя структурированные данные с явными полями — написать маппинг полей в HTML-элементы ДО верстки (поле_1 → тег_1, поле_2 → тег_2). Дополнительные UI-слои (таблица-индекс, фильтры) добавлять только если пользователь явно запросил.
**Scope:** universal
**Category:** design-process

### 2026-03-30 methodology-sync-sketch / code-audit: Граница ответственности SKILL.md vs. agent-file

**Seen:** 1
**Adapted:** —
**Triad:** создание скилла с companion agent-file (SKILL.md + agents/{name}.md) → явно разграничить что делает SKILL.md (оркестрация фаз) и что делает agent-file (протокол одного шага) → избежать дублирования одного действия в обоих файлах
**Context:** sketch/SKILL.md Phase 3 и sketch-interviewer.md оба описывали сохранение sketch.md. Code audit поймал дублирование как minor finding — execution model оказалась неоднозначной: кто реально выполняет save?
**Pattern:** При написании скилла с companion agent-file: SKILL.md описывает ЧТО происходит на каждой фазе (вход, выход, переход), agent-file описывает КАК выполняется конкретный шаг внутри одной фазы. Каждое конкретное действие (save, send, transform) должно быть явно описано ровно в одном месте.
**Scope:** situational
**Situation:** Новый скилл делегирует часть логики в отдельный agents/{name}.md файл
**Category:** problem-decomposition

### 2026-03-30 pipeline-report / techspec: AC — единственная верификационная рамка при противоречии с описательным блоком

**Seen:** 1
**Adapted:** —
**Triad:** user-spec содержит описательный блок с требованием не отражённым в AC → следовать только AC как источнику истины; противоречие зафиксировать decision-записью и обновить user-spec → не тащить неопределённость из описательного блока в реализацию
**Context:** pipeline-report: описательный блок говорил "стандартный запрос по шаблону поля" — AC этого не содержал. tech-spec принял AC за истину, оформил разрыв решением, обновил user-spec. Без этого разрыв дошёл бы до реализации как неоднозначность.
**Pattern:** Если user-spec содержит описательный блок с требованием не отражённым в AC — AC является источником истины. Зафиксировать разрыв в tech-spec decisions и обновить user-spec, иначе следующий агент снова наткнётся на то же противоречие и будет вынужден решать его самостоятельно.
**Scope:** universal
**Category:** scope-management

<!-- PROMOTED → code-writing (Seen: 2, 2026-03-30 pipeline-report retro — merged: session_id user-provided input added to trigger) -->
### 2026-03-30 methodology-sync-sketch / test-audit: grep в AVP чувствителен к регистру

**Seen:** 1
**Adapted:** —
**Triad:** написание grep-based smoke check для markdown-контента → проверить фактический регистр строки в целевом файле перед финализацией команды → предотвратить ложно-отрицательный AVP check при несовпадении регистра
**Context:** AVP step 2 искал `'decision gate'` (lowercase), SKILL.md содержал `## Phase 6: Decision Gate` (Title Case). grep -c вернул бы 0 вместо ожидаемого ≥ 2. Поймано в test audit, не в момент написания AVP.
**Pattern:** При написании grep-смоков для markdown: открыть целевой файл и убедиться что искомая строка написана именно так. Если регистр не предсказуем (фаза, секция, метка) — добавить флаг -i. Правило: "сначала прочитай, потом grep".
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 methodology-sync-sketch / done: Атомарная запись в shared-файл при конкурентных сессиях

**Seen:** 1
**Adapted:** —
**Triad:** Edit tool возвращает "File has been unexpectedly modified" на shared файле методологии → переключиться на атомарный read-modify-write через скрипт, не повторять Edit → избежать накопления partial writes и дублирующихся записей
**Context:** При исправлении дублирующихся номеров в triad-index.md Edit tool 3 раза падал с "unexpectedly modified" — файл одновременно изменялся другими сессиями. Python-скрипт с прямой записью решил за 1 попытку.
**Pattern:** Первое "File has been unexpectedly modified" — сигнал конкурентной записи, не случайная ошибка. Не повторяй Edit — переключайся сразу на atomic read-modify-write: прочитать файл целиком, преобразовать в памяти, записать атомарно через скрипт.
**Scope:** situational
**Situation:** Shared файлы методологии (triad-index.md, reasoning-patterns.md), редактируемые из нескольких сессий одновременно
**Category:** recovery

### 2026-03-30 pipeline-report / session 1: параллельный запуск ломает смысловой порядок

**Seen:** 1
**Adapted:** —
**Triad:** два шага процесса связаны по смыслу (A должен завершиться до показа B) → запускать A синхронно, ждать завершения, только потом выполнять B → гарантировать смысловой порядок — фоновый запуск A не означает A < B
**Context:** quick-learning запущен в фоне одновременно с генерацией next-session prompt — уведомление пришло после, нарушив ожидаемый порядок "сначала анализ, потом промт".
**Pattern:** Если два шага имеют смысловую зависимость для пользователя (B опирается на результат A или должен следовать после него), не оптимизируй под параллелизм — запускай A синхронно. Фоновый запуск сохраняет время, но ломает порядок и доверие.
**Scope:** universal
**Category:** sequencing


<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30 pipeline-report retro) -->
<!-- PROMOTED → task-decomposition (Seen: 2, 2026-03-30 pipeline-report retro) -->
### 2026-03-30 freelance-dashboard / session 1: scope-impact check перед добавлением фичи в спек

**Seen:** 1
**Adapted:** —
**Triad:** пользователь говорит "встроить" / "добавить" на вопрос о новой фиче в середине user-spec интервью → задать scope-impact вопрос ("это v1 или отдельная фича?") до обновления спека → не добавить в текущий спек фичу, которая утроит объём и потребует другой архитектуры
**Context:** Пользователь подтвердил включение sync-агента в dashboard-v1 ("это нужно в первый заход встроить"). Я начал перестраивать архитектуру (localStorage → backend). Пользователь сам откатил через 2 сообщения. Потерял 1 цикл интервью.
**Pattern:** Когда пользователь добавляет нетривиальную фичу в текущий спек — не вноси немедленно. Сначала озвучи архитектурный импакт и спроси явно: "Это v1 или отдельная спека?" Один вопрос дешевле чем переписывание scope.
**Scope:** situational
**Situation:** user-spec интервью, пользователь предлагает добавить фичу которая меняет архитектурный слой или удваивает объём задач
**Category:** scope-management

### 2026-03-30 freelance-dashboard / session 1: client-only storage + серверная автоматизация — проверять совместимость сразу

**Seen:** 1
**Adapted:** —
**Triad:** в одной фиче сочетаются client-only хранилище (localStorage, IndexedDB, cookies) и серверная автоматизация (cron, background script, webhook) → до финализации архитектуры проверить: может ли серверный процесс читать/писать в это хранилище → не обнаружить data-access конфликт в середине tech-spec
**Context:** localStorage + ежедневный sync-скрипт были предложены как v1. Поймал конфликт до спека: серверный скрипт не имеет доступа к browser storage — потребовался бы полный backend. Предотвратил ошибочную архитектуру.
**Pattern:** Если фича включает client-only storage и любой серверный процесс — немедленно проверь data-access layer: кто пишет, кто читает, через какой канал. localStorage недоступен с сервера; server-side файл недоступен из браузера без API. Это базовый compatibility check, который нужно делать до любого архитектурного решения.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-30 photo-crop / session 1: структурные gate-вопросы при конвертации алгоритма в процедурный скилл

**Seen:** 1
**Adapted:** —
**Triad:** конвертация пользовательского алгоритма (список шагов) в процедурный SKILL.md → добавить gate-вопрос («перечисли что определил на этом шаге») в конце каждой фазы, даже если его нет в оригинале → удовлетворить структурные требования процедурного скилла без повторного прогона валидатора
**Context:** пользователь передал 4-шаговый алгоритм для расчёта object-position; первый черновик точно воспроизвёл шаги, но пропустил межфазовые чекпоинты — skill-checker потребовал второй прогон.
**Pattern:** Пользовательский алгоритм — это контент, не формат. При конвертации в процедурный скилл добавляй checkpoint-gates независимо от исходника: в конце каждой фазы явно требуй от агента зафиксировать промежуточный результат перед переходом к следующему шагу.
**Scope:** situational
**Situation:** создание нового процедурного SKILL.md на основе алгоритма, предоставленного пользователем или взятого из документации
**Category:** sequencing

### 2026-03-30 export-contacts-filter / session 1: Деструктивная операция в пайплайне — фильтр по статусу, не по полю

**Seen:** 1
**Adapted:** —
**Triad:** user-spec описывает delete/cleanup в системе с pipeline-статусами → ограничивать удаление терминальными статусами (enriched/done), не значением поля → не удалить записи ещё в обработке (pending/in-progress)
**Context:** Предложение "удалять дела без телефона при каждом запуске" удалило бы pending-записи, которые просто не дошли до обогащения (квота ofdata исчерпана на середине цикла). Adequacy validator поймал это как critical data loss риск.
**Pattern:** Если specs описывают деструктивную операцию над записями в системе с processing-статусами — всегда уточни: удаляем только те, что прошли финальный статус (enriched/failed/complete). "Нет нужного поля" ≠ "обработка завершена".
**Scope:** universal
**Category:** scope-management

### 2026-03-30 export-contacts-filter / session 1: Сужение фильтра в спеке — документируй исключение явно

**Seen:** 1
**Adapted:** —
**Triad:** spec сужает критерий от обсуждённого в интервью (A or B → только A) → добавить в Технические решения "решили НЕ включать B, потому что..." → не тратить дополнительные раунды валидации на задокументирование очевидного для автора решения
**Context:** В интервью обсуждался фильтр "phone OR email". Spec молча сузил до "только phone". Quality validator 3 раза подряд флажил это как undocumented decision, пока не появилась явная строка "решили не фильтровать по email, потому что нужен отзвон".
**Pattern:** Когда в спеке сужаешь фильтр/критерий относительно того, что обсуждалось — документируй не только то, что взяли, но и то, что явно отбросили и почему. Reviewers не знают что это осознанное решение, а не упущение.
**Scope:** universal
**Category:** scope-management

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30): Флаг-файл run-once — путь от якоря, не от CWD -->

### 2026-03-30 pipeline-report / session 2: checkpoint.yml не создан при старте второй сессии

**Seen:** 1
**Adapted:** —
**Triad:** многосессионная фича с session-plan → создавать/коммитить checkpoint.yml в конце каждой сессии, не только читать его в начале следующей → предотвратить ситуацию «ожидаемый файл состояния отсутствует» при старте сессии 2+
**Context:** При старте сессии 2 pipeline-report ожидался checkpoint.yml, но файл не был создан в конце сессии 1. Сессия 1 завершилась коммитом кода, но без явного шага создания state-файла — checkpoint.yml не входил в outputs сессии 1 по session-plan.
**Pattern:** В session-plan для каждой сессии явно добавлять checkpoint.yml в список outputs. Если сессия 2 начинается с «читаем checkpoint.yml» — сессия 1 должна заканчиваться «создаём checkpoint.yml». Ожидать state-файл без его явного создания — молчаливая ошибка handoff.
**Scope:** situational
**Situation:** multi-session feature execution с явным session-plan и передачей состояния между сессиями
**Category:** sequencing

### 2026-03-30 export-contacts-filter / session 2: Audit-волна ловит cross-task баги невидимые per-task ревьюеру

**Seen:** 1
**Adapted:** —
**Triad:** завершение implementation-волн в multi-task фиче → запустить code + security + test аудиты параллельно в отдельной волне → поймать баги из взаимодействия задач, невидимые для ревьюера отдельного diff-а
**Context:** Per-task ревьюеры одобрили Task 1 (флаг-файл создан). Audit-волна нашла major finding: путь к флаг-файлу CWD-relative — проблема возникает из контекста deployment, а не из diff отдельной задачи.
**Pattern:** После implementation-волн добавляй audit-волну (code + security + test, параллельно). Каждый аудитор читает финальное состояние всех файлов фичи — ловит deployment-sensitive и cross-component проблемы, которые per-task ревьюер видит только в своём diff-е.
**Scope:** situational
**Situation:** multi-task feature с 3+ implementation задачами в разных файлах
**Category:** sequencing

### 2026-03-30 juridical-parser / deploy: Метрика в статус-дашборде — уточни временной горизонт

**Seen:** 1
**Adapted:** —
**Triad:** добавление метрики в status/dashboard без явного требования → уточнить у пользователя: за текущий запуск или за всё время → не додумывать горизонт самостоятельно, он варьируется
**Context:** Реализовал счётчики обогащения как SQL-агрегат по всей БД. Пользователь поправил: нужно за текущий запуск. Разные метрики могут требовать разных горизонтов в зависимости от задачи.
**Pattern:** Перед реализацией любой метрики в дашборде/отчёте уточни временной горизонт: за запуск, за день, за период, за всё время. Не выбирай дефолт самостоятельно — это требование, которое варьируется.
**Scope:** universal
**Category:** scope-management

### 2026-03-31 juridical-parser / session: clear() не сбрасывает форматирование во внешних сервисах

**Seen:** 1
**Adapted:** —
**Triad:** вызов clear()/reset() на внешнем сервисе перед записью новых данных → явно сбрасывать ВСЕ слои состояния (контент + форматирование + кэш) → предотвратить проявление предыдущего состояния после "очистки"
**Context:** ws.clear() в Google Sheets очищает ячейки, но не форматирование — красные цвета от предыдущего вызова оставались на новых строках.
**Pattern:** Перед перезаписью данных в внешнем сервисе (Sheets, browser storage, CDN) — проверить, очищает ли "reset"-операция все слои состояния. Если нет — добавить явный сброс каждого слоя отдельно перед записью.
**Scope:** universal
**Category:** tool-selection

### 2026-03-31 juridical-parser / session: production-аномалия может объясняться старой версией кода

**Seen:** 1
**Adapted:** —
**Triad:** production данные не соответствуют поведению текущего кода → сверить timestamp задеплоенного файла с временем запуска → не искать баг в коде который уже правильный
**Context:** was_incomplete=1 в БД при корректном коде — оказалось, фикс был задеплоен ПОСЛЕ прогона, т.е. прогон выполнялся на старом коде.
**Pattern:** При аномалии в production-данных сначала проверить: был ли исправленный код задеплоен ДО момента запуска (ls -la timestamp vs run_date в логе). Если нет — это артефакт старой версии, баг уже устранён.
**Scope:** universal
**Category:** recovery

### 2026-03-31 juridical-parser / session: уточни ownership сервера до деплоя

**Seen:** 1
**Adapted:** —
**Triad:** выполнение deploy-команды в проекте клиента → уточнить чей сервер и кто контролирует деплой-процесс ДО выполнения → не произвести несогласованное изменение на продакшене клиента
**Context:** Задеплоил файлы напрямую на VPS через scp, не уточнив что это продакшен клиента, а не тестовый сервер разработчика.
**Pattern:** Перед выполнением deploy-команды в чужом проекте — явно уточнить: чей это сервер (клиента или разработчика) и как согласовывается деплой. Наличие DEPLOY_HOST в .env не означает права на прямой деплой.
**Scope:** situational
**Situation:** Работа над проектами внешних клиентов, где deploy-инфраструктура принадлежит клиенту
**Category:** communication

### 2026-03-31 juridical-parser / session ad-hoc: изолированный вызов компонента вместо полного пайплайна

**Seen:** 1
**Adapted:** —
**Triad:** запрос на обновление одного компонента системы (статус, отчёт, вкладка) → вызвать только этот компонент изолированно через минимальный скрипт → не тратить ресурсы полного пайплайна и не вызывать побочных эффектов
**Context:** Пользователь попросил обновить статус-вкладку — запустил полный пайплайн с парсером, сжёг API-квоту клиента.
**Pattern:** Когда просят обновить конкретный компонент (статус, отчёт, вкладку) — идентифицировать минимальный вызов этого компонента и запустить его изолированно. Не запускать полную систему, если не попросили явно.
**Scope:** universal
**Category:** scope-management

### 2026-03-31 dashboard-v1 / task-decomposition: stub-ownership gap при межзадачных placeholder-ах

**Seen:** 1
**Adapted:** —
**Triad:** задача N создаёт no-op stubs "для следующих задач" → в бриф каждой заполняющей задачи явно добавить шаг "замени no-op stub на реализацию" → гарантировать что placeholder не останется no-op в рабочем коде
**Context:** Task 4 создала 6 handler-стабов в App.jsx "для Wave 4". Tasks 5 и 6 описывали как вызывать хендлеры, но не содержали шага замены стаба реальной имплементацией. Cross-task ревьюер поймал это: verify-user провалился бы — reload → данные не сохраняются.
**Pattern:** Когда задача N создаёт stubs/placeholders "для следующих задач" — task-creator заполняющих задач должен явно включать шаг "в App/Controller/родителе: заменить no-op stub [название] на реальную имплементацию". Не рассчитывать что агент выведет это из контекста.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 dashboard-v1 / deploy: SSH + sudo в GitHub Actions CI деплое

**Seen:** 1
**Adapted:** —
**Triad:** GitHub Actions SSH step выполняет `sudo service-name reload` от deploy-пользователя → убрать sudo из reload-команды (или настроить NOPASSWD в sudoers заранее), добавить `-o StrictHostKeyChecking=no` в SSH-команду → не получать permission denied на первом CI деплое
**Context:** deploy.yml использовал `sudo nginx -s reload` — deploy user не имел sudo. Плюс StrictHostKeyChecking блокировал first-time connect в CI. Итого 8 fix-коммитов.
**Pattern:** При написании GitHub Actions SSH deploy — сразу убрать sudo перед командой reload (nginx/pm2/etc), добавить `-o StrictHostKeyChecking=no` к ssh-команде, и проверить локально права deploy-user до первого push в CI.
**Scope:** universal
**Category:** sequencing

### 2026-03-31 employee-cabinet / session 1: уточнять регион и регуляторику ДО предложения стека

**Seen:** 1 (employee-cabinet/session 1)
**Adapted:** —
**Triad:** предложение хостинг/стека для нового проекта → уточнить регион развёртывания и регуляторные ограничения ДО предложения решений → не переписывать архитектурный стек после обсуждения
**Context:** Предложил Supabase+Railway, затем узнал что проект в России (152-ФЗ, данные граждан РФ) — пришлось полностью менять стек на PostgreSQL+Timeweb VPS.
**Pattern:** При выборе хостинга и инфраструктуры — первым вопросом уточнить страну/регион развёртывания и наличие регуляторных требований (локализация данных, compliance). Только после этого предлагать конкретные сервисы.
**Scope:** universal
**Category:** information-gathering

## Universal

### 2026-03-31 employee-cabinet / session 1: проверять тип БД-объекта до init-кода адаптера

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** подключение адаптера внешней библиотеки к БД → проверить ожидаемый тип объекта (raw driver vs query builder) в docs ДО написания init-кода → не получить runtime ошибку несовместимости адаптера на первом запросе
**Context:** better-auth принимает Kysely-инстанс, мы передали pg.Pool → `db.selectFrom is not a function` при первом login
**Pattern:** Когда библиотека принимает "database" параметр — найти в docs конкретный тип (Pool / Kysely / Prisma), не угадывать по названию. Разные обёртки над одной БД несовместимы на уровне интерфейса.
**Scope:** universal
**Category:** tool-selection

### 2026-03-31 employee-cabinet / session 2: новая роль mid-interview → немедленная матрица прав

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** новая роль появляется в середине user-spec интервью → немедленно составить матрицу "роль × ключевые возможности" и согласовать с пользователем до продолжения → не тратить 3+ батча на выяснение пересечений между ролями
**Context:** Пользователь ввёл роль "руководитель" mid-interview — потребовалось 3 батча чтобы выяснить что она почти совпадает с admin, после чего роль вынесли в отдельную фичу.
**Pattern:** При появлении новой роли — сразу составить таблицу "роль × возможность" и показать пользователю. Пересечения ролей обнаруживаются немедленно, лишние батчи не нужны.
**Scope:** situational
**Situation:** user-spec интервью для приложений с несколькими ролями пользователей
**Category:** scope-management

### 2026-03-31 employee-cabinet / session 1: мокировать инфраструктурную зависимость чтобы разблокировать демо

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** демонстрация UI застряла из-за нерабочей инфраструктурной зависимости (auth, БД, API) → замокировать зависимость локально в компоненте → не блокировать оценку UX из-за инфраструктурной проблемы
**Context:** better-auth не работал локально, пользователь не мог увидеть кабинет → подставили mock-session прямо в компонент и убрали guard в middleware
**Pattern:** Если инфра-зависимость блокирует демо — замокировать её в компоненте за 2 минуты и показать UI. Исправлять инфра отдельно, не держать UX-демо заложником конфига.
**Scope:** universal
**Category:** recovery

### 2026-04-01 dashboard-v1 / session post-deploy: nginx server_name conflict detection

**Seen:** 1
**Adapted:** —
**Triad:** диагностика недоступности nginx снаружи → запустить `nginx -T | grep -B2 -A10 server_name` → обнаружить конфликт server blocks за один шаг
**Context:** два server block претендовали на server_name 217.114.2.159 — dashboard и levelupme (certbot). Ручной просмотр каждого конфига занял бы несколько шагов.
**Pattern:** При недоступности nginx-сервиса снаружи — первым шагом запускать `nginx -T` с grep по server_name. Конфликты server blocks часто невидимы при просмотре одного конфига.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 dashboard-v1 / session post-deploy: мобильный оператор блокирует HTTP по IP

**Seen:** 1
**Adapted:** —
**Triad:** сервис доступен через curl с сервера (порт 80), но браузер на мобильном зависает → уточнить "по домену или по IP" до диагностики nginx/сети → не тратить время на network-диагностику
**Context:** nginx отвечал 401 на curl, curl с ноутбука работал, а с телефона через 4G зависал без ошибки — причина в блокировке прямых HTTP-запросов по IP у мобильного оператора.
**Pattern:** Если сервис работает через curl но зависает в мобильном браузере — сразу уточнить: домен или IP. Российские мобильные операторы блокируют прямые HTTP-запросы по IP; решение — домен + SSL.
**Scope:** situational
**Situation:** мобильный интернет российских операторов, сервис доступен только по IP
**Category:** recovery


### 2026-04-01 employee-cabinet / session decompose: параллельные тесты — изолировать seed по email

**Seen:** 1
**Adapted:** —
**Triad:** два параллельных теста пишут в общую тестовую БД через одного seed-пользователя → использовать разные email-константы для каждой тестовой задачи → избежать teardown race condition при параллельном выполнении
**Context:** Tasks 9 (integration) и 10 (E2E) в одной волне оба пишут в TEST_DATABASE_URL. globalSetup Task 10 чистил timesheets seeded-user в момент когда integration-тесты Task 9 могли ещё работать.
**Pattern:** Если несколько тестовых задач работают параллельно с общей БД — каждой задаче присвоить уникальный seed-email (integration-test@..., e2e-test@...). Уточнять это в Details задачи явно, не полагаться на transaction isolation.
**Scope:** situational
**Situation:** параллельное выполнение нескольких тестовых задач против одной тестовой БД
**Category:** problem-decomposition

### 2026-04-01 dashboard-progress-sync / userspec: подтвердить порядок фич до инициализации папки

**Seen:** 1
**Adapted:** —
**Triad:** пользователь описывает несколько взаимосвязанных фич для реализации → явно уточнить порядок реализации ДО инициализации папки первой фичи → не создавать и переименовывать артефакты под неправильную фичу
**Context:** Сессия стартовала с `/new-user-spec dashboard-crm`, папка создана — но пользователь уточнил что первой фичей должен быть progress-sync, а не CRM. Папку пришлось переименовывать.
**Pattern:** Когда пользователь показывает спеки для N взаимосвязанных фич — перед стартом спросить "в каком порядке реализуем?" и только после подтверждения запускать `init-feature-folder.sh`.
**Scope:** situational
**Situation:** пользователь приносит несколько готовых спеков или модулей в одной сессии
**Category:** scope-management

### 2026-04-01 dashboard-progress-sync / userspec: проверять наличие файлов в git до GitHub API в AC

**Seen:** 1
**Adapted:** —
**Triad:** фича читает файлы методологии (work/, checkpoint.yml) через GitHub Contents API → уточнить у пользователя закоммичены ли эти файлы в репозитории ДО написания AC → не получить "прогресс не отслеживается" для всех проектов из-за .gitignore
**Context:** В спеке предполагалось читать checkpoint.yml через GitHub API для % прогресса — но пользователь подтвердил что work/ нередко в .gitignore. Потребовалось добавить fallback-ветку "прогресс не отслеживается".
**Pattern:** Если фича читает проектные файлы через GitHub Contents API — перед написанием AC проверить: "эти файлы вообще коммитятся в репо?" Особенно это касается папок вроде work/, .claude/, logs/ которые часто gitignore-ятся.
**Scope:** situational
**Situation:** планирование фичи с GitHub API доступом к файлам в репозиториях пользователя
**Category:** information-gathering

## Universal

### 2026-04-01 freelance-dashboard / session design-refactor: JS viewport state — признак отсутствия CSS architecture

**Seen:** 1
**Adapted:** —
**Triad:** JS state существует только для переключения CSS-значений по viewport → заменить state+listener на CSS media queries + className → убрать re-renders и сделать layout управляемым CSS
**Context:** App.jsx и ProjectModal.jsx содержали `isMobile` state + resize listener только для выбора между двумя наборами inline styles
**Pattern:** Если JS state имеет ровно два значения и оба соответствуют CSS-состояниям для breakpoint — это признак отсутствующей CSS-архитектуры. Удалить state, вынести логику в media queries, заменить inline styles на className. Это не рефакторинг ради чистоты — это устранение источника будущих багов при добавлении новых breakpoints.
**Scope:** universal
**Category:** tool-selection

## Situational

### 2026-04-01 freelance-dashboard / session design-refactor: дизайн-пайплайн на приложении с inline styles → CSS migration приоритет

**Seen:** 1
**Adapted:** —
**Triad:** design-system-init запущен на существующем приложении с inline styles → пропустить interview, экстрактировать токены из кода, выполнить CSS migration → переключить source-of-truth стилей, а не задокументировать существующие значения
**Context:** дизайн-пайплайн вызван для React-дашборда с 200+ inline styles; пользователь сказал "всё нравится, просто сделай как надо"
**Pattern:** Когда design-system-init запускается на проекте с уже сложившимися стилями и пользователь одобрил существующую эстетику, interview-фаза не нужна. Экстрактировать токены напрямую из кода, создать CSS custom properties + классы, мигрировать компоненты. HTML-демо вторичны — ценность в миграции живого кода.
**Scope:** situational
**Situation:** существующий React/Vue/Svelte проект с inline styles + пользователь одобрил текущую эстетику
**Category:** design-process

### 2026-04-01 dashboard-progress-sync / session 1: Верификационный curl без auth = ложный положительный

**Seen:** 1 (this feature/session)
**Adapted:** —
**Triad:** curl-команда в AVP/user-spec для endpoint с auth → проверить что команда включает auth header + добавить отдельный тест без ключа → 401 → не получить false QA pass при сломанной авторизации
**Context:** user-spec содержал curl POST без X-Api-Key; если бы auth middleware был сломан, команда вернула 200 — агент зафиксировал бы успех, не обнаружив проблему
**Pattern:** Для каждой верификационной curl-команды к защищённому endpoint — убедиться что команда передаёт auth credential. Добавить рядом явный тест "без ключа → 401". Тест auth работает только если один из вариантов должен упасть.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 juridical-parser / ops: изменение расписания «с завтрашнего дня»

**Seen:** 1
**Adapted:** —
**Triad:** пользователь просит изменить расписание «с завтрашнего дня» при наличии ближайшего запуска → проверить время ближайшего запуска и применить изменение ПОСЛЕ него → не потерять плановый прогон из-за немедленного переключения
**Context:** Крон стоял на 00:30 UTC, пользователь попросил переключить на 21:30 UTC «с завтрашнего дня» — изменение применили немедленно, ближайший запуск через 13 минут был пропущен.
**Pattern:** Перед применением изменения расписания проверить время следующего запуска. Если он ближе 30 минут — дождаться его завершения, только потом менять конфиг.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 1: HTTP-сервер с API key auth — security must-have в первой реализации

**Seen:** 1
**Adapted:** —
**Triad:** реализация HTTP-сервера с API key auth → включить timing-safe comparison (`crypto.timingSafeEqual`) и явный body size limit в первоначальную реализацию → не тратить review-раунд на предсказуемые security best practices
**Context:** Task 1 — первая реализация server/index.js сравнивала API key через `===`. Review round 1 нашла timing attack и отсутствие body limit. Пришлось коммитить fix-раунд. Обе находки предсказуемы для любого auth middleware.
**Pattern:** При реализации API key auth — сразу используй `crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))` и добавляй `express.json({ limit: '10kb' })`. Эти две детали находит любой security reviewer с первого взгляда — добавив их сразу, ты экономишь review-раунд.
**Scope:** situational
**Situation:** реализация HTTP-сервера с токен/key-based auth
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 1: Helper с null/undefined — верифицируй граничные значения до review

**Seen:** 1
**Adapted:** —
**Triad:** helper-функция принимает значение из внешнего источника (API-ответ, env var, user input) → вручную проверить edge cases (null, undefined, пустая строка, 0) перед первым review → не получать post-review fix на предсказуемые null/boundary guards
**Context:** Task 4 — `calcCommitDays(isoDateString, now)` принимала значение из GitHub API. Review нашло: при `null` передаётся в `new Date(null)`, что возвращает epoch (0 ms). Исправление: добавить `typeof isoDateString !== 'string'` guard. Предсказуемый граничный случай для любой функции, работающей с внешними данными.
**Pattern:** Перед первым review helper-функции, работающей с внешними данными — пройти по списку: null, undefined, пустая строка, 0, NaN. Добавить guard/return-null для каждого неожиданного значения. Reviewer найдёт эти кейсы в первом же раунде — лучше закрыть их заранее.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 2: вынести числовые threshold в константы до review

**Seen:** 1
**Adapted:** —
**Triad:** задача с числовым threshold в коде → вынести magic numbers в именованные константы до первого review → не тратить review-раунд на предсказуемые hardcoded value замечания
**Context:** Task 3 (Frontend Progress column) — reviewer нашёл magic number `3` (stale days threshold). Понадобился дополнительный fix-коммит и второй review-раунд.
**Pattern:** Перед отправкой на review кода с числовыми границами (дни, лимиты, таймауты, размеры) — вынести каждый threshold в именованную константу с говорящим именем. Это предсказуемое замечание reviewer-а, которое дешевле закрыть до ревью.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 juridical-parser / ops-2: позиция фильтра в pipeline

**Seen:** 1
**Adapted:** —
**Triad:** конфиг содержит whitelist/фильтр для ограничения обработки → явно уточнить на каком этапе pipeline применяется фильтр (сбор данных vs экспорт) и согласовать с пользователем → не тратить ресурсы (квоту/время) на обработку данных которые всё равно отфильтруются
**Context:** Whitelist по судам фильтровал только экспорт в Sheets, но не парсинг — квота тратилась на все 54 суда, хотя пользователь обсуждал ограничение до 2.
**Pattern:** Когда в конфиге есть whitelist/фильтр — проверить на каком этапе pipeline он применяется. Если фильтр стоит после ресурсоёмкой операции (API-запрос, обогащение), переместить его до неё.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 juridical-parser / session fix-status: семантика метрики перед патчем симптома

**Seen:** 1
**Adapted:** —
**Triad:** метрика показывает логически невозможное значение (A < B где A должно быть ≥ B) → установить семантическое определение каждой метрики ДО трейсинга кода → найти структурный баг вместо маскировки симптома
**Context:** found=0 при exported=2 — предложил `found = max(found, exported)` как фикс, пользователь поймал что логика неверна; оказалось found и exported считались из разных pipeline-стадий с разной семантикой.
**Pattern:** Когда метрика показывает невозможное значение — сначала зафиксировать: "что должна считать X?" и "что должна считать Y?" на уровне пользовательской семантики. Только после этого трейсить код-источники. Патч выходного значения маскирует структурный баг в логике накопления.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 juridical-parser / session fix-status: некорректное значение в БД — трейс write paths

**Seen:** 1
**Adapted:** —
**Triad:** поле БД содержит значение неверного формата (не NULL и не ожидаемый тип) → найти ВСЕ пути записи в это поле включая legacy-код и дефолты схемы → не создавать cleanup под гипотезу без верификации причины
**Context:** exported_to_sheets = '0' блокировало дела в очереди; гипотеза "whitespace phone" оказалась неверной — причина в legacy формате (булево 0 вместо NULL из старого кода).
**Pattern:** Аномальное значение в БД-поле (не NULL, не ожидаемый тип) требует полного трейса write paths: grep все UPDATE/INSERT для этой колонки, включая исторические миграции. Cleanup пиши только после подтверждённой причины, не под первую гипотезу.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 juridical-parser / session fix-status-2: формулировка остаточной проблемы через user-observable state

**Seen:** 1
**Adapted:** —
**Triad:** формулировка остаточной проблемы в session-end промте → верифицировать каждую проблему против того что пользователь видит в UI/выводе, а не против внутреннего состояния кода → не направить следующую сессию решать неверно идентифицированную проблему
**Context:** В промте описал проблему как "found/exported semantics в export_log" (code-internal), пользователь поправил: реальная проблема — "цифры в статусе не совпадают с содержимым таблицы" (user-observable).
**Pattern:** При описании остаточных проблем для следующей сессии — формулировать через то, что пользователь наблюдает в выводе ("статус показывает X, а в таблице Y"), а не через внутреннюю механику ("переменная court_stats считается из BatchA"). Внутренняя механика — это гипотеза о причине, не сама проблема.
**Scope:** universal
**Category:** communication

### 2026-04-01 employee-cabinet / userspec-amendment: Правки клиента после одобрения спека — точечный амендмент

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** клиент присылает правки к user-spec со статусом approved → задать вопросы только по неоднозначным пунктам, обновить существующий spec напрямую → не запускать полный интервью-цикл заново
**Context:** Клиент прислал 4 уточнения к уже одобренной спеке. Правильным шагом была не новая спека, а точечное мини-интервью и прямое обновление документа.
**Pattern:** Когда клиент присылает правки к одобренному user-spec — определить затронутые пункты (переименование / уточнение / новая микро-фича), уточнить только неоднозначные детали, обновить spec напрямую. Полный интервью-цикл — только если меняется scope всей фичи.
**Scope:** situational
**Situation:** client feedback arrives after user-spec is already approved
**Category:** scope-management

### 2026-04-01 employee-cabinet / userspec-amendment: UI микро-детали в spec — предлагать стандартный паттерн

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** user-spec интервью требует уточнения UI-расположения элемента (где/как панель, тулбар, диалог) → применить стандартный UX паттерн без вопроса к пользователю → не блокировать интервью на деталях, которые пользователь не может сформулировать
**Context:** Задал абстрактный вопрос "панель или диалог?" — пользователь ответил "не понял вопроса, посоветуйся с дизайн-пайплайном". Нужно было выбрать стандартный паттерн самостоятельно.
**Pattern:** Для UI микро-деталей (расположение, поведение элемента) — если требование ясно функционально — выбрать общепринятый паттерн и предложить его ("появляется прилипающая панель с кодами"), не задавать открытый вопрос. Пользователь подтвердит или скорректирует.
**Scope:** situational
**Situation:** уточнение UI-деталей в ходе user-spec или design-spec интервью
**Category:** scope-management

### 2026-04-01 employee-cabinet / techspec-update: Gap-анализ перед написанием задач на обновлённый спек

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** обновление user-spec к уже реализованной фиче → запустить code-researcher для diff новых требований против существующего кода перед написанием задач → не создавать задачи для уже реализованного функционала
**Context:** `/new-tech-spec` запустили после завершения реализации всех 15 задач. User-spec обновили с клиентским фидбеком. Без code-researcher gap-анализа риск — написать 5-7 задач из которых 3-4 уже реализованы.
**Pattern:** Если `/new-tech-spec` вызван на уже реализованную фичу (есть decisions.md с completed-задачами), сначала запустить code-researcher с вопросом "что из новых требований ещё не в коде". Только после — писать задачи. Это предотвращает дублирование работы и "задачи-призраки".
**Scope:** situational
**Situation:** обновление tech-spec для фичи, реализация которой уже завершена (есть решённые задачи)

### 2026-04-01 employee-cabinet / task-decomposition: Implementation hints должны отражать реальный код, а не идеальный

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** task-creator пишет hints для файла, который уже реализован в кодовой базе → прочитать фактический код файла ДО написания hints → не создавать hints противоречащие существующей реализации
**Context:** task-creator для Task 5 написал hint про `fs.createReadStream+Readable.toWeb()`, хотя реальный файл использовал `fs.readFile+NextResponse(buffer)`. Task 6 имел `authClient.forgetPassword()` вместо реального `authClient.requestPasswordReset()`. Reality-checker поймал оба в round 1.
**Pattern:** Если task-creator получает файл с пометкой "already exists" или "уже реализован" — читать фактический код перед написанием hints, не реконструировать по описанию. Правило: hints описывают КАК ЕСТЬ, а не КАК ДОЛЖНО БЫТЬ.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 employee-cabinet / task-decomposition: TDD Anchor не должен называть файл, являющийся deliverable другой задачи

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** TDD Anchor задачи A называет тестовый файл, который является primary deliverable задачи B → убрать тест из TDD Anchor A, добавить "интеграционное покрытие в задаче B" → один файл — один владелец, нет конфликта владения при параллельном выполнении
**Context:** Task 5 имел TDD Anchor с двумя тестами в `tests/integration/certificates.test.ts`. Но этот файл — primary deliverable Task 9. Кросс-задачная проверка обнаружила конфликт: Task 9 мог перезаписать нуль файла при создании с нуля.
**Pattern:** При написании TDD Anchor — проверить, не является ли названный тестовый файл основным deliverable другой задачи (по Files to modify в tech-spec). Если да — убрать якорные тесты из текущей задачи и сослаться на задачу-владельца. TDD Anchor задачи A не должен создавать зависимость write-after-write.
**Scope:** situational
**Situation:** multi-task фича с разделёнными задачами реализации и тестирования (задача X делает API, задача Y делает тесты для него)
**Category:** information-gathering

### 2026-04-01 employee-cabinet / session 2: auth-библиотека возвращает 200 на duplicate flow — тестировать через side effect

**Seen:** 1 (employee-cabinet/session 2)
**Adapted:** —
**Triad:** интеграционный тест проверяет ошибочный сценарий (duplicate signup) через auth-библиотеку → проверять через side effect (DB row count), не HTTP статус → не получить false-negative когда библиотека возвращает 200 с resend-flow вместо 400
**Context:** better-auth v1.5.6 при повторном signup возвращает 200 (resend verification), а не 400. Тест ожидал 400 → упал; исправление — проверять count строк в users.
**Pattern:** Для интеграционных тестов auth-флоу (duplicate, invalid state) — не предполагать что auth-библиотека возвращает стандартные 4xx. Сначала проверить поведение в docs/вручную. Тестировать через observable state: DB row count, наличие сессии. HTTP статус — вторичная проверка.
**Scope:** universal
**Category:** tool-selection

### 2026-04-01 employee-cabinet / session 2: E2E global-setup — прямой INSERT вместо sign-up через API

**Seen:** 1 (employee-cabinet/session 2)
**Adapted:** —
**Triad:** E2E global-setup требует seeded verified user → прямой INSERT с hashPassword через crypto вместо sign-up API + SQL UPDATE → устранить зависимость seed-фазы от работающего сервера
**Context:** Task 10 global-setup делал POST /api/auth/sign-up + SQL UPDATE. После round 1 переписан на прямой INSERT с `hashPassword` из better-auth/crypto — setup стал детерминированным, без зависимости от dev-сервера.
**Pattern:** Для E2E seed users — не использовать HTTP API. Найти функцию хеширования пароля в auth-библиотеке (типа `hashPassword`) и сделать прямой INSERT. Это отвязывает seed от application layer.
**Scope:** situational
**Situation:** E2E-тесты с pre-seeded users для auth-библиотек с собственным password hashing
**Category:** tool-selection
