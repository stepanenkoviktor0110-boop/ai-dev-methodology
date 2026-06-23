# Reasoning Patterns

Accumulated insights about decision-making logic across projects.
Single transit buffer for ALL methodology knowledge — both reasoning patterns and operational lessons.

**This is a transit buffer.** Patterns that reach `Seen: 3` get promoted into skill SKILL.md files and removed from here. Stale entries (Seen: 1, older than 30 days) get pruned.

---

## Universal

Patterns that apply to any project, any stack, any domain.

<!-- Append universal patterns below -->

### 2026-04-14 menu-editor / session 1: runtime readiness conflation

**Seen:** 1
**Adapted:** —
**Cognitive Error:** runtime readiness conflation
**Triad:** исполнитель получает недоступный инфраструктурный сервис → явно разделить compile-time зависимости (типы/контракты) от runtime зависимостей и продолжать работу по compile-time ветке → не блокировать работу из-за смешения уровней зависимостей
**Context:** Применение миграции к БД заблокировано по инфраструктурным причинам. Следующие задачи зависели от schema.ts (compile-time types), а не от живой БД (runtime) — правильно продолжить и зафиксировать блокер как deferred.
**Scope:** universal
**Category:** sequencing

### 2026-04-14 menu-editor / session 2: eager state collapse bias

**Seen:** 1
**Adapted:** —
**Cognitive Error:** eager state collapse bias
**Triad:** компонент с переключаемым количеством видимых элементов → откладывать обрезку массива до момента submit, не при переключении режима → не потерять данные при обратном переключении
**Context:** volumes.slice(0, volumeCount) применяется только при отправке PUT, не при смене radio-кнопки. Если обрезать при switch — данные невидимых слотов уничтожены.
**Scope:** universal
**Category:** scope-management

### 2026-04-14 menu-editor / session 2: success-path-only state design

**Seen:** 1
**Adapted:** —
**Cognitive Error:** success-path-only state design
**Triad:** форма выполняет async-операцию с возможным failure → сбрасывать UI state только при успехе, сохранять при ошибке → пользователь не теряет ввод
**Context:** editState preserved on save error в Task 8. Дефолтная интуиция "операция завершена → сбросить форму" не различает success и error path.
**Scope:** universal
**Category:** scope-management

### 2026-03-31 dashboard-v1 / deploy: Браузер молчит — смотри server access log до диагностики сети

**Seen:** 1
**Adapted:** —
**Triad:** браузер показывает "не грузит" без ошибки → сразу проверить server access log → узнать реальный HTTP-статус до диагностики firewall/сети
**Context:** Пользователь видел пустой браузер и думал что порт заблокирован. Nginx access log показал 4 запроса с 401 — сервер работал, проблема была в неверном пароле Basic Auth.
**Scope:** universal
**Category:** recovery

### 2026-03-30 methodology-sync-sketch / session 1: агент-файл для multi-context — нейтральные сигналы завершения

**Seen:** 1 (methodology-sync-sketch / session 1)
**Adapted:** —
**Triad:** написание агент-файла, который используется и inline, и через spawn_agent → не использовать ссылки на родительский контекст ("return to Phase N"), давать нейтральный сигнал завершения ("task complete. [result]") → артефакт работает корректно в обоих execution environments
**Context:** sketch-interviewer.md написан с `"return to SKILL.md Phase 5"` — это работает в Claude Code (inline load), но ломается в Codex spawn_agent где агент не знает про родителя.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 employee-cabinet / session 1: Проверять overlap файлов внутри волны перед финализацией tech-spec

**Seen:** 2
**Adapted:** —
**Triad:** завершение секции Implementation Tasks в tech-spec → проверить "Files to modify" каждой задачи на пересечение внутри одной волны → предотвратить merge-конфликт при параллельном выполнении
**Context:** Tasks 7 и 8 в Wave 3 оба изменяли `cabinet/timesheet/page.tsx`. При параллельном выполнении — гарантированный конфликт. Поймал только template-validator. (Seen 2: panel-next-run — Tasks 3/4/5 все меняли `index.html`, поймал template-validator.)
**Scope:** universal
**Category:** sequencing

### 2026-04-01 employee-cabinet / session 1: File upload в архитектуре требует явного описания file download

**Seen:** 1
**Adapted:** —
**Triad:** проектирование фичи с загрузкой пользовательских файлов на диск → явно определить механизм доставки файлов (protected API endpoint с ownership check, не static) в Architecture секции → предотвратить IDOR через неавторизованный прямой доступ к файлам
**Context:** Tech-spec описывал POST для загрузки PDF-сертификатов, но не описывал как файлы отдаются клиенту. Файлы попали бы в `/uploads/` без auth-защиты. Поймал security-auditor — добавлен новый Task 5.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 employee-cabinet / session 1: Субагент сообщает о блокере — верифицировать самостоятельно

**Seen:** 2
**Adapted:** —
**Triad:** субагент сообщает о блокере (build failure, missing dep, broken env) как причине незавершённой задачи → запустить ту же команду самостоятельно → не принимать диагноз агента как факт без проверки
**Context:** Task 5 агент заявил "pre-existing build failure (missing admin/timesheets route, unrelated)" и пометил это как не-блокер. Верификация показала: build проходил нормально, никакого pre-existing failure не было. Диагноз агента был ложным. (Seen 2: 2026-06-09 cabinet-sources-api — агент Wave 4 вернул бессвязный финальный отчёт, оставив свой реальный результат незакоммиченным; lead обнаружил это через git-состояние, а не по отчёту.)
**Scope:** universal
**Category:** recovery

### 2026-04-01 employee-cabinet / session 1: Субагент не обновляет frontmatter статус задачи

**Seen:** 1
**Adapted:** —
**Triad:** завершение задачи субагентом → явно обновить `status: done` в frontmatter task-файла как финальный шаг → не накапливать задачи со статусом "planned" требующие ручного batch-обновления от лида
**Context:** Tasks 2, 4, 5, 6, 7 оставлены со статусом "planned" после выполнения — агенты обновляли decisions.md, но не трогали task frontmatter. Лид обнаружил при wave transition и обновлял вручную партиями.
**Scope:** universal
**Category:** sequencing

### 2026-03-31 dashboard-v1 / session 3: Local-first режим — уточнить среду деплоя до запуска deploy-pipeline

**Seen:** 1
**Adapted:** —
**Triad:** pre-deploy QA завершён, пользователь в local-first / sketch режиме → уточнить желаемую среду верификации ДО запуска deploy wave → не готовить VPS-деплой для пользователя который не планирует его сейчас
**Context:** Task 12 (Deploy) запустился по плану волны. Только после попытки настройки выяснилось: нет remote, нет GitHub, нет секретов — пользователь сказал "пока размещаем локально". Создан GitHub репо, код запушен, но VPS-деплой отложен. Волна 7-8 зафиксирована как deferred.
**Scope:** situational
**Situation:** sketch-mode или local-first фичи, где пользователь не заявил явного намерения деплоить
**Category:** communication

### 2026-03-26 shift-confirmation: Ошибки повторяются между волнами

**Seen:** 2
**Adapted:** —
**Triad:** ревью ИЛИ git-история выявили уже-отклонённый подход/паттерн ошибки на этом месте → вписать находку или историю отклонения в промт делегируемого агента → предотвратить повторение ошибки/переизобретение отклонённого подхода в следующих задачах
**Context:** В Task 1 ревьюер нашёл `confirmationStatus: string` вместо enum. Исправили. В Task 4 — ровно та же ошибка. Агент Task 4 не знал о находке Task 1, т.к. каждый teammate с чистым контекстом. (Seen 2, 2026-06-05 cabinet-clients-list/s2) Делегировал fixer-у тест для async-throw пути, не вписав в бриф, что прежний подход — `process`-listener на unhandledRejection — уже убирали в Session 1 из-за флакости; агент с чистым контекстом переизобрёл ровно его, потребовался лишний раунд ревью. Уже-отклонённый подход живёт в git-истории/соседнем коде, а не только в находке ревью текущей сессии.
**Scope:** situational
**Situation:** multi-agent feature execution с несколькими волнами
**Category:** communication

<!-- PROMOTED → code-writing (Seen: 2, 2026-03-30) -->

### 2026-03-26 shift-confirmation: Known-issues реестр для аудитов

**Seen:** 1
**Adapted:** —
**Triad:** security/code audit в multi-task feature → вести known-issues.md, аудитор читает перед ревью → не тратить время на повторный репорт известных проблем
**Context:** Security auditor нашёл IDOR в `markEvent()` при ревью Task 2. Та же находка повторилась в audit wave. Нет реестра известных проблем — тратит время на уже известное.
**Scope:** situational
**Situation:** multi-task features с security/code audit
**Category:** information-gathering

### 2026-03-28 mvp-pipeline-core + mvp-parser: Тесты на моках скрывают расхождение с реальным внешним процессом

**Seen:** 2
**Adapted:** —
**Triad:** unit-тесты с моками для внешнего процесса/API → провести минимум 1 live smoke-прогон перед объявлением QA passed → предотвратить ложное "all tests pass" при расхождении мока и реальности
**Context:** (1) mvp-parser: 75 тестов pass, но реальный API возвращал другую структуру. (2) mvp-pipeline-core: 77 тестов pass, QA passed — но реальный `claude -p` вернул JSON в envelope + markdown fences + свой формат полей. 7 fix-коммитов после "успешного" QA.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 mvp-parser / live-test: Программное создание документа — зачищай дефолтные артефакты

**Seen:** 1
**Adapted:** —
**Triad:** программное создание документа через API → после создания кастомного контента удалить дефолтные артефакты → не оставлять мусор в финальном документе
**Context:** При создании spreadsheet через API дефолтный лист остался пустым рядом с кастомными вкладками. Проверка пустоты по техническому свойству (row_count) не сработала — свойство имеет ненулевой default. Фикс: идентифицировать дефолтные артефакты по имени.
**Scope:** universal
**Category:** tool-selection

<!-- PROMOTED → feature-execution SKILL.md (2026-03-30, Seen: 2) -->

### 2026-03-28 bp-pipeline / skeleton-pipe: Язык пользователя, не профессиональный жаргон

**Seen:** 1
**Adapted:** —
**Triad:** обсуждение решений с пользователем → использовать язык и терминологию пользователя, расшифровывать каждый термин → ускорить принятие решений, не тратить время на "а что это значит?"
**Context:** Спорные пункты pipeline.md были описаны с аббревиатурами (T1/T2/T3, ICE, severity levels). Пользователь сказал: "я не знаю что такое Т1, ты знаешь, не сокращай ничего". После переформулирования простым языком — все 6 решений приняты за один раунд.
**Scope:** universal
**Category:** communication

### 2026-03-31 dashboard-v1 / session 3: CSS position:fixed провалился на React inline style — зеркаль JS-паттерн соседнего компонента

**Seen:** 1
**Adapted:** —
**Triad:** CSS `position: fixed` не применяется к компоненту с React inline `style={{ display: "none" }}` → использовать JS `isMobile` state с resize listener (зеркально существующему компоненту) → не тратить раунды на CSS, который не может надёжно переопределить React inline style
**Context:** mobile-nav в App.jsx имел `style={{ display: "none" }}` с переопределением через `@media { .mobile-nav { display: flex !important; position: fixed; } }`. Пользователь подтвердил: вкладка находится не внизу viewport, нужно прокрутить страницу. При этом ProjectModal уже использовал `isMobile = useState(() => window.innerWidth <= 640)` + useEffect resize listener. Фикс: применить тот же паттерн к nav div, убрав CSS-подход.
**Scope:** universal
**Category:** recovery

### 2026-03-27 mvp-parser / live-test: Проверить стоимость retry до включения

**Seen:** 1
**Adapted:** —
**Triad:** API с лимитом запросов + retry decorator → проверить считаются ли неудачные запросы в лимит ДО включения retry → не сжечь квоту на бессмысленные повторы
**Context:** retry_with_backoff на parser-api.com сжёг 51 запрос из 200/месяц за одну сессию. Каждый обрыв соединения (ConnectionError, ReadTimeout) = запрос списан. Документация не указывает, считаются ли failed requests. Предположение "считаются только успешные" оказалось ложным.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 mvp-parser / session 3: Согласуй структуру выходного артефакта до реализации

**Seen:** 1
**Adapted:** —
**Triad:** требования к формату выходных данных поступают итеративно → согласовать полную структуру на макете до написания кода → не переписывать реализацию на каждое уточнение
**Context:** Структура экспорта менялась 4 раза за сессию. Каждое изменение = переписывание export + query + тесты.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 design-pipeline-v2 / techspec: Verify-smoke для markdown — проверяй структуру, не ключевые слова

**Seen:** 1
**Adapted:** —
**Triad:** verify-smoke для markdown-артефакта (SKILL.md, шаблон) → проверять структурные элементы (фазы, ссылки на файлы, guard-ы), не просто ключевые слова → убедиться что артефакт полноценный, а не stub с нужными словами
**Context:** Изначально verify-smoke для ~180-строчного deep skill содержал 2 grep-проверки (имя скилла + слово "Phase"). Test reviewer справедливо указал: SKILL.md из одной строки с этими словами пройдёт проверку. После фикса — 6-8 проверок: Phase 0, Phase 2, ссылки на input-файлы, corruption guard.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 design-pipeline-v2 / userspec: Генерируй все шаги deliverable целиком, не только ближайший

**Seen:** 3
**Adapted:** —
**Triad:** создание multi-step deliverable (план, roadmap, серия промптов) → сгенерировать все шаги целиком, не только ближайший → не заставлять пользователя ловить недостающие части
**Context:** Создал промпт только для Session 1 из 6. Пользователь сразу заметил что промпт для Session 2 будет некорректным. Пришлось создавать session-roadmap.md со всеми промптами — то, что нужно было сделать сразу.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 analiticxxs / perf-fix: Проверяй дефолты библиотек до оптимизации кода

**Seen:** 1
**Adapted:** —
**Triad:** performance problem на сервере с низким трафиком → проверить дефолтные таймауты/лимиты connection pool и кэшей → найти root cause в конфигурации до оптимизации кода
**Context:** TTFB 7-23 секунд на Next.js SSR. Инстинкт — искать тяжёлые запросы, N+1, SSR complexity. Реальная причина: pg Pool `idleTimeoutMillis: 10000` (дефолт) — на low-traffic сервере ВСЕ соединения закрывались каждые 10 секунд, каждый запрос = DNS + TCP + PG handshake. Фикс: одно число `10000 → 60000` = TTFB с 7-23 сек до 196 мс.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / techspec: Файловые пути — верифицировать, не угадывать (PROMOTED)

**Seen:** 2 → PROMOTED → tech-spec-planning
**Adapted:** —
**Triad:** написание файловых путей в tech-spec или skill из памяти/docs → верифицировать через ls/glob или прочитать source-файл → не допустить неверных путей в artifacts
**Context:** (1) design-task-decompose: путь к session-plan.md указан по аналогии, реальный путь отличался. (2) methodology-sync-sketch: tech-spec написал `~/.claude/skills/shared/work-templates/`, реальный — `~/.claude/shared/work-templates/`. Оба поймал mirage detector в validation round 1.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 fix-knowledge-pipeline / decompose: Заменяй межзадачную зависимость на общий source of truth

**Seen:** 1
**Adapted:** —
**Triad:** задача в одной волне ссылается на результат другой задачи той же волны → заменить зависимость на чтение общего source of truth (decisions.md, tech-spec.md) → сохранить параллельность волны без рисков read-after-write
**Context:** Task 2 (align retrospective) ссылалась на quick-learning/SKILL.md "after Task 1 modifies it", но обе задачи в Wave 1 (параллельно). depends_on: [1] + wave: 1 — противоречие. Решение: Task 2 читает decisions.md напрямую (те же решения, но source of truth, а не output другой задачи). Зависимость убрана, параллельность сохранена.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 missing-ui-details / wave-2: Сверяй типографику с референсом ДО реализации

**Seen:** 2
**Adapted:** design-generate
**Triad:** фича с визуальным оригиналом (rebuild, redesign, visual polish) → сверить layout, цветовую схему и типографику с референсом ДО написания CSS, составить чеклист расхождений → избежать полного редизайна или серии fix-коммитов после деплоя
**Context:** (1) Visual polish — спек не описывал конкретный шрифт, 9 fix-коммитов. (2) Website rebuild — текстовое описание из code-research без скриншотов привело к полностью другому дизайну (тёмный gradient вместо белого фона, centered вместо two-column, слайдер отдельно вместо в hero). Обнаружено только после деплоя на VPS.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 pipeline-stabilization / session 1: Перед ревью — проверить артефакты удаления

**Seen:** 1
**Adapted:** —
**Triad:** задача на удаление фичи/константы/поля → перед отправкой на ревью проверить dead variables, stale comments, duplicate tests от удалённого кода → не тратить review-раунд на предсказуемые артефакты удаления
**Context:** Task 1 удалил MAX_OUTPUT_CHARS и два поля из REQUIRED_FIELDS. Task 2 удалил extended mode и wave-поля. Все 6 ревьюеров нашли только minor-находки: мёртвая переменная `missing` (ссылалась на удалённый check), stale-комментарии с "extended", дублирующийся тест (старый обновлён до пустого набора — совпал с новым TDD-тестом). Все предсказуемы.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 pipeline-stabilization / session 2: При редактировании AI-промтов — явно проверять emphasis-framing

**Seen:** 1
**Adapted:** —
**Triad:** редактирование/компрессия AI-промта → явно проверить все prohibition/caps формулировки ("НЕЛЬЗЯ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО") и заменить на motivation-framing → не тратить review-раунды на предсказуемую emphasis-ошибку
**Context:** Tasks 4, 5, 6 (компрессия agent-04..10) — три задачи подряд получили major-находку от prompt-reviewer: prohibition lists и капслок ("СТРОГО СОБЛЮДАЙ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО"). Паттерн повторился во всех трёх задачах. Все найдены в одном review-раунде и исправлены в одном коммите.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 fix-knowledge-pipeline: Overflow-политика при распределении в capped buckets

**Seen:** 1
**Adapted:** —
**Triad:** алгоритм распределяет записи по bucket-ам с max-cap → определить overflow-политику (куда идут записи сверх лимита) до реализации → не терять записи при заполнении bucket-а
**Context:** Task 5 генерировал per-skill quick-ref файлы с лимитом 10 записей. quick-ref-feature-execution.md заполнился (10 записей из sequencing/recovery/communication), запись #32 была молча отброшена. Reviewer обнаружил: #32 должна попасть в do-task (overflow bucket). Задача не описывала overflow-поведение.
**Scope:** universal
**Category:** tool-selection

### 2026-03-29 design-pipeline-v2 v2.3 / session 1: При cross-domain адаптации шаблона — проверять совместимость каждого поля

**Seen:** 1
**Adapted:** —
**Triad:** адаптация шаблона задачи из одного домена в другой → проверить каждое поле frontmatter на применимость к целевому домену → не исправлять domain-несовместимые defaults отдельной задачей после деплоя
**Context:** design-task.md.template был создан в v2.2 по образцу task.md.template. Поле `reviewers: [skill-checker]` скопировано из code-domain шаблона — там оно осмысленно. В design-domain quality gate — user visual review, не skill-checker. Несовместимость обнаружена при написании tech-spec v2.3 и потребовала отдельной Task 2 в следующей версии.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 design-pipeline-v2 v2.3 / task-decomposition: Пилотная задача перед массовой генерацией по новому шаблону

**Seen:** 1
**Adapted:** —
**Triad:** массовая генерация задач по шаблону, применяемому к новому домену впервые → сначала 1 пилотная задача → проверить и валидировать → масштабировать на все задачи → не накапливать 30+ правок при первом прогоне
**Context:** task-creator сгенерировал 8 задач по design-task.md.template за один прогон. Validation round 1 дал 30+ находок (несовместимые поля, неверные пути, domain-mismatch в reviewers). Если бы задача 1 была проверена первой — паттерн ошибок был бы найден до масштабирования на 7 оставшихся.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 pipeline-stabilization / session-3: Security severity привязывается к модели развёртывания

**Seen:** 3 → PROMOTED to security-auditor
**Adapted:** —
**Triad:** security audit находит medium-уязвимости в локальном CLI-инструменте → классифицировать как non-blocking с явным условием "до перехода на service/multi-user деплой" → не блокировать релиз по находкам нерелевантным текущей модели развёртывания
**Context:** Task 9 нашла 3 medium-находки (отсутствие hard-limit на --text, произвольный --data-dir, отсутствие size limits на validator fields). Все три реальны и требуют fix — но только перед service deployment. Для single-user CLI они не создают угрозы.
**Scope:** situational
**Situation:** инструмент развёртывается как локальный CLI для одного пользователя; есть планы перейти на service-модель
**Category:** scope-management

<!-- PROMOTED → task-decomposition (Seen: 2, 2026-03-30) -->

### 2026-03-29 pipeline-stabilization / session-3: QA разделяет failed и deferred

**Seen:** 1
**Adapted:** —
**Triad:** QA-критерий требует live-вызова внешнего сервиса (LLM, API, DB) недоступного в test-среде → отметить как deferred с явным условием, не как failed → получить чистый QA pass на автоматизируемых критериях без блокировки
**Context:** Task 11 (pre-deploy QA) прошла 20 из 22 критериев. 2 оставшихся требуют live Claude CLI вызова с активной подпиской. Вместо fail или skip — deferred с записью в deferredToPostDeploy, что даёт чёткий план для post-deploy verification.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 analiticxxs / recovery: Давай один шаг за раз при неизвестном внешнем состоянии

**Seen:** 2
**Adapted:** —
**Triad:** пользователь выполняет многошаговый процесс с неизвестной веткой или внешним состоянием → сначала задать уточняющий вопрос о ветке, затем давать по одному шагу с ожиданием результата → не давать инструкции для неизвестного или неактуального состояния
**Context:** Пользователь вставил весь блок команд прямо в psql вместо bash. Также: пользователь получил все 5 шагов SSH fix без уточнения способа доступа к VPS — инструкции могли быть нерелевантны.
**Scope:** universal
**Category:** communication

### 2026-03-30 design-pipeline-v2 v2.3: Граничное условие счётчика — верифицируй против спецификации

**Seen:** 2
**Adapted:** —
**Triad:** написание числовой логики с граничным условием (max N повторений, retry limit, iteration cap) → сразу подставить граничное значение и убедиться что условие выполняется ровно N раз → не пропустить off-by-one через code review
**Context:** Wave-итерации в design-session-execution: counter=1, условие `< 3` — вместо 3 re-spawn получилось 2. Decision 9 требовал max 3 итерации. Code audit (HIGH finding) поймал; обычный review не заметил бы. Fix: `< 3` → `<= 3`.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: git add scope должен покрывать все write locations скилла

**Seen:** 1
**Adapted:** —
**Triad:** скилл или агент делает commit и пишет файлы в несколько директорий → перечислить все write locations из тела скилла перед написанием git add → не потерять файлы вне основного дерева при коммите
**Context:** design-done: `git add work/completed/{feature}/` не захватывал `.design-system/` файлы, которые design-retrospective пишет в корне проекта. Архивный коммит был неполным. HIGH finding на code audit; fix: `git add -A`.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: TRIZ для выбора между равнозначными вариантами фикса

**Seen:** 1
**Adapted:** —
**Triad:** два варианта фикса дают одинаковый результат но отличаются по устойчивости к будущим изменениям → применить tradeoff-анализ (minimal diff vs systemic robustness) → выбрать вариант с меньшим coupling к текущим деталям реализации
**Context:** HIGH #1: `< 3` vs `counter=0` — оба дают 3 итерации, но `<= 3` семантически точнее и ближе к спецификации. HIGH #2: `git add work/completed/` vs `git add -A` — оба фиксируют текущие файлы, но `-A` устойчив к добавлению новых write locations. Оба выбора сделаны за один раунд без обсуждения.
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 agent-research-prompt-fix userspec: поведение агента после пропуска — логика, не маркер

**Seen:** 1
**Adapted:** —
**Triad:** описание skip-поведения агента при пустом user input → явно описать что агент ДЕЛАЕТ после пропуска (продолжает анализ), не только какой маркер ставит в поле → не допустить реализации label-swap без изменения логики
**Context:** Спек описывал [ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ] как замену [НЕТ ДАННЫХ]. Пользователь уточнил: агент должен реально завершить анализ с имеющимися данными, а не просто переименовать заглушку. Разница критическая для реализации.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix userspec: active + planned stubs для многочастного скопа

**Seen:** 1
**Adapted:** —
**Triad:** user spec вырастает до 3+ последовательно зависимых deliverable разного размера → оставить первый deliverable active draft, остальные создать как planned stubs → пользователь видит прогресс на каждой части и контекст постфич сохранён
**Context:** Спек начался как 3 пункта, вырос до 4, потом пользователь попросил разбить "чтобы видеть прогресс". Создали 3 отдельных файла: part1 (active/approved), part2+3 (planned). Части 2 и 3 полностью проработаны для контекста, но не запускаются сразу.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 design-v2 / session 1: Зона субъекта фото — до расстановки UI overlay

**Seen:** 1
**Adapted:** —
**Triad:** размещение текста/UI поверх full-bleed фото → определить зону субъекта в кропированном вьюпорте ДО расстановки элементов → не перекрыть лицо/объект текстом
**Context:** Hero с portrait фото в landscape viewport — текст был поставлен по центру экрана и накрыл лицо стилиста. Потребовался полный редизайн grid-структуры.
**Scope:** situational
**Situation:** Hero или full-bleed секция с фото, поверх которой размещаются текст или UI-блоки
**Category:** design-process

### 2026-06-05 cabinet-shell-login / session 1: spec-over-code illusion

**Seen:** 1
**Adapted:** —
**Cognitive Error:** spec-over-code illusion
**Triad:** оркестратор готовит бриф для исполнителя, опираясь на текст спека → прочитать реальный целевой код ДО формирования контракта в промте → не передавать контракт противоречащий живой реализации
**Context:** Спек Task 3/4/6 описывал поведение api.js (что refresh/login возвращают), но живой api.js не персистил токены — AuthContext обязан делать это явно. Аналогично: AuthContext не был экспортирован в живом файле. Lead прочитал реальный код до спавна агентов и скорректировал контракты в промтах; без этого агенты молча сломали бы bootstrap и тесты.
**Pattern:** Перед передачей контракта из спека исполнителю — прочитать реальный целевой файл и сверить заявленное поведение с кодом. Если расхождение найдено — скорректировать бриф до спавна, задокументировать как deviation.
**Scope:** universal
**Category:** information-gathering

### 2026-06-05 cabinet-shell-login / session 1: fix locality illusion

**Seen:** 1
**Adapted:** —
**Cognitive Error:** fix locality illusion
**Triad:** исполнитель применяет фикс в задаче N (добавляет/меняет контракт) → немедленно проверить downstream-задачи и зафиксировать обязательство в review note перед завершением → не передавать несогласованный контракт silent dependency следующим волнам
**Context:** Task 3 добавила новый код ошибки SESSION_INIT_FAILED. Task 4 (LoginScreen) должна была маппировать его в пользовательское сообщение — но это не было указано в исходном спеке Task 4. Фикс в Task 3 породил downstream-обязательство; оно было пронесено через round-2 review note RR-1 и корректно реализовано в Task 4. Без propagation — Task 4 молча проигнорировала бы новый код.
**Pattern:** Когда фикс в задаче N изменяет публичный контракт (добавляет код, меняет сигнатуру, добавляет export) — перед завершением задачи явно перечислить downstream-задачи и добавить в review notes обязательство для каждой из них.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-v2 / session 1: Редизайн = независимый выбор layout, не наследование структуры

**Seen:** 1
**Adapted:** —
**Triad:** задача "альтернативный дизайн" или "редизайн существующей страницы" → выбирать layout pattern независимо от существующей верстки → получить реальную альтернативу, а не ресайн с другими цветами
**Context:** Первый preview был отклонён ("всё ещё сильно основан на прошлой версии") — структура 50/50 split была перенесена из v1, изменены только шрифты и цвета.
**Scope:** situational
**Situation:** Задача создать v2, альтернативный вариант или редизайн существующей страницы
**Category:** design-iteration

### 2026-03-30 methodology-sync-sketch / session 1: Классификация глубины diff до написания sync scope

**Seen:** 1
**Adapted:** —
**Triad:** планирование синка файлов между двумя версиями одного репо → запустить code-research для классификации глубины различий до написания scope → не описывать в AC механический синк который требует ручного ревью каждого файла
**Context:** Планировали синк 26 скиллов в Codex через замену путей (.claude/→.agents/). Code-research показал что 24 из 26 имеют реальные content-различия (feature-execution переписан под spawn_agent API) — scope пришлось полностью переписать.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / session 1: Итеративная классификация доменов в mono-repo

**Seen:** 1
**Adapted:** —
**Triad:** репо содержит скиллы из нескольких доменов → явно перечислить каждый домен и получить is_in_scope per domain до написания спека → не переписывать scope в 3 итерации из-за постепенного уточнения границ
**Context:** Один репо содержит методологию, дизайн-пайплайн, promoter, skeleton-pipe, sketch. Уточнения "это отдельный пайплайн" происходили трижды (design → promoter/skeleton → уточнение что sketch ВХОДИТ). Каждый раз — реакция на вопрос.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 agent-research-prompt-fix / session 2: верифицировать содержимое каждого целевого файла перед описанием операции

**Seen:** 2 (agent-research-prompt-fix × 2)
**Adapted:** —
**Triad:** spec (user, tech, task) называет набор файлов и описывает трансформацию → верифицировать каждый файл на наличие изменяемого элемента → не допустить ошибочный тип операции (replace вместо add)
**Context:** (1) User-spec назвал "runner.py" и "счётчик уже есть" — неточные утверждения, пойманы code-research. (2) Tech-spec описал "убрать [НЕТ ДАННЫХ] из всех 9 промптов" — agent-03 этой строки не содержит, нужна другая операция (add instruction). Поймано reality-checker при декомпозиции.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix / session 2: тест с точной строкой-маркером создаёт неявный depends_on

**Seen:** 1 (agent-research-prompt-fix)
**Adapted:** —
**Triad:** задача содержит тест с точной строкой-маркером определённой в другой задаче → объявить depends_on на задачу-источник даже если строка — литерал → не пропустить неявную зависимость через разделённый дизайн-маркер
**Context:** Task 4 содержала `test_propushcheno_not_pipeline_defect` ассертящий на `"[ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ]"`. Строка определяется в Task 2 (pipeline.py). Task 4 объявила only `depends_on: [1]`. Индивидуальные валидаторы пропустили — cross-task валидатор поймал.
**Scope:** situational
**Situation:** multi-task декомпозиция с sentinel strings / protocol markers общими между задачами
**Category:** problem-decomposition

### 2026-04-02 moneymaker / techspec: Каталог скиллов — читай ДО написания задач И при исправлении

**Seen:** 2
**Adapted:** n/a
**Triad:** написание ИЛИ исправление полей Skill/Reviewers в Implementation Tasks → сверить ВСЕ значения в списке с `skills-and-reviewers.md`, не только сообщённый → не вносить новые миражи при починке известных
**Context:** Tasks 1-5 использовали `write-code` (wrapper) — поймано в round 1. При исправлении был введён `test-reviewer` (не существует) — поймано skeptic в round 2. Оба раза ошибка = интуитивный псевдоним вместо проверки каталога.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 pipeline-report / decompose: TDD Anchor для private метода — вызов через инстанс

**Seen:** 1
**Adapted:** —
**Triad:** TDD Anchor описывает тест для private метода класса → указывать вызов через инстанс объекта, не через прямой импорт → тесты не падают с ImportError до запуска реальной логики
**Context:** task-creator написал TDD Anchor с инструкцией `import _generate_report from bp_pipeline.pipeline`. Private метод нельзя импортировать напрямую — reality-checker поймал как critical. Правка: `pipeline_instance._generate_report(session, session_dir)`.
**Scope:** situational
**Situation:** task-creator генерирует TDD Anchor для private метода класса
**Category:** problem-decomposition

### 2026-03-30 design-v2-stylist / session 2: Совместимость фото с контейнером — проверять до CSS

**Seen:** 1
**Adapted:** —
**Triad:** выбор лейаута с full-bleed фото → проверить ориентацию фото и кадрирование субъекта против формы контейнера ДО написания CSS → не тратить итерации на геометрически невозможный кроп
**Context:** Портретное фото стилиста (субъект стоит в полный рост на фоне яркого окна) поставили в 50vh landscape-баннер. Ни один Y не мог показать субъекта — это геометрический факт определяемый до верстки. Понадобилось 3 итерации и полная переделка лейаута.
**Scope:** situational
**Situation:** верстка секций с фотографиями в фиксированных контейнерах (hero, banner, split)
**Category:** design-process

### 2026-03-30 design-v2-stylist / session 2: Структурированные данные → UI напрямую

**Seen:** 1
**Adapted:** —
**Triad:** верстка контентной секции из структурированных данных пользователя → маппировать каждое поле данных в UI-элемент напрямую → не изобретать структуру отображения которая расходится с источником
**Context:** Пользователь прислал услуги в формате: название → суть → цена → буллеты. Вместо прямого маппинга была создана отдельная таблица-индекс + аккордеон с другими именами. Потребовались 2 раунда переделки пока структура не совпала с источником.
**Scope:** universal
**Category:** design-process

### 2026-03-30 methodology-sync-sketch / code-audit: Граница ответственности SKILL.md vs. agent-file

**Seen:** 1
**Adapted:** —
**Triad:** создание скилла с companion agent-file (SKILL.md + agents/{name}.md) → явно разграничить что делает SKILL.md (оркестрация фаз) и что делает agent-file (протокол одного шага) → избежать дублирования одного действия в обоих файлах
**Context:** sketch/SKILL.md Phase 3 и sketch-interviewer.md оба описывали сохранение sketch.md. Code audit поймал дублирование как minor finding — execution model оказалась неоднозначной: кто реально выполняет save?
**Scope:** situational
**Situation:** Новый скилл делегирует часть логики в отдельный agents/{name}.md файл
**Category:** problem-decomposition

### 2026-03-30 pipeline-report / techspec: AC — единственная верификационная рамка при противоречии с описательным блоком

**Seen:** 1
**Adapted:** —
**Triad:** user-spec содержит описательный блок с требованием не отражённым в AC → следовать только AC как источнику истины; противоречие зафиксировать decision-записью и обновить user-spec → не тащить неопределённость из описательного блока в реализацию
**Context:** pipeline-report: описательный блок говорил "стандартный запрос по шаблону поля" — AC этого не содержал. tech-spec принял AC за истину, оформил разрыв решением, обновил user-spec. Без этого разрыв дошёл бы до реализации как неоднозначность.
**Scope:** universal
**Category:** scope-management

<!-- PROMOTED → code-writing (Seen: 2, 2026-03-30 pipeline-report retro — merged: session_id user-provided input added to trigger) -->

### 2026-03-30 methodology-sync-sketch / test-audit: grep в AVP чувствителен к регистру

**Seen:** 1
**Adapted:** —
**Triad:** написание grep-based smoke check для markdown-контента → проверить фактический регистр строки в целевом файле перед финализацией команды → предотвратить ложно-отрицательный AVP check при несовпадении регистра
**Context:** AVP step 2 искал `'decision gate'` (lowercase), SKILL.md содержал `## Phase 6: Decision Gate` (Title Case). grep -c вернул бы 0 вместо ожидаемого ≥ 2. Поймано в test audit, не в момент написания AVP.
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 methodology-sync-sketch / done: Атомарная запись в shared-файл при конкурентных сессиях

**Seen:** 1
**Adapted:** —
**Triad:** Edit tool возвращает "File has been unexpectedly modified" на shared файле методологии → переключиться на атомарный read-modify-write через скрипт, не повторять Edit → избежать накопления partial writes и дублирующихся записей
**Context:** При исправлении дублирующихся номеров в triad-index.md Edit tool 3 раза падал с "unexpectedly modified" — файл одновременно изменялся другими сессиями. Python-скрипт с прямой записью решил за 1 попытку.
**Scope:** situational
**Situation:** Shared файлы методологии (triad-index.md, reasoning-patterns.md), редактируемые из нескольких сессий одновременно
**Category:** recovery

### 2026-03-30 pipeline-report / session 1: параллельный запуск ломает смысловой порядок

**Seen:** 1
**Adapted:** —
**Triad:** два шага процесса связаны по смыслу (A должен завершиться до показа B) → запускать A синхронно, ждать завершения, только потом выполнять B → гарантировать смысловой порядок — фоновый запуск A не означает A < B
**Context:** quick-learning запущен в фоне одновременно с генерацией next-session prompt — уведомление пришло после, нарушив ожидаемый порядок "сначала анализ, потом промт".
**Scope:** universal
**Category:** sequencing

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30 pipeline-report retro) -->
<!-- PROMOTED → task-decomposition (Seen: 2, 2026-03-30 pipeline-report retro) -->

### 2026-04-02 content-card / marketplace: Вырезать фон товара ДО генерации карточки

**Seen:** 1
**Adapted:** —
**Triad:** marketplace карточка с фото товара на нежелательном фоне → запустить rembg и получить PNG с прозрачностью ДО генерации HTML → избежать прямоугольного "кирпича" фото в дизайне карточки
**Context:** Первая версия карточки для бейсболки показала кепку с серым градиентным фоном на кремовом фоне карточки — пользователь оценил как "очень слабо". Фоновый прямоугольник уничтожил весь дизайн. Переделка потребовала установки rembg, вырезки фона и полного перепроектирования photo-зоны.
**Scope:** situational
**Situation:** content-card / marketplace режим, фото товара с ненейтральным фоном
**Category:** design-process

### 2026-04-02 content-card / marketplace: Прозрачное пространство в PNG — учитывать при посадке на поверхность

**Seen:** 1
**Adapted:** —
**Triad:** PNG с вырезанным фоном (product shot) позиционируется CSS-bottom на платформу или поверхность → рассчитать bottom = platform_top_px - transparent_space_bottom_px → предмет визуально стоит на поверхности, не парит
**Context:** После вырезки фона кепка при bottom: 90-112px продолжала парить над платформой. Причина: rembg убрал серую поверхность-отражение оригинального фото — снизу PNG остался прозрачный блок ~30% высоты изображения. Реальный brim кепки находится на 255px выше низа PNG при max-height: 851px.
**Scope:** situational
**Situation:** HTML/CSS карточка с CSS-платформой и PNG-товаром с вырезанным фоном
**Category:** design-process

### 2026-03-30 freelance-dashboard / session 1: scope-impact check перед добавлением фичи в спек

**Seen:** 1
**Adapted:** —
**Triad:** пользователь говорит "встроить" / "добавить" на вопрос о новой фиче в середине user-spec интервью → задать scope-impact вопрос ("это v1 или отдельная фича?") до обновления спека → не добавить в текущий спек фичу, которая утроит объём и потребует другой архитектуры
**Context:** Пользователь подтвердил включение sync-агента в dashboard-v1 ("это нужно в первый заход встроить"). Я начал перестраивать архитектуру (localStorage → backend). Пользователь сам откатил через 2 сообщения. Потерял 1 цикл интервью.
**Scope:** situational
**Situation:** user-spec интервью, пользователь предлагает добавить фичу которая меняет архитектурный слой или удваивает объём задач
**Category:** scope-management

### 2026-03-30 freelance-dashboard / session 1: client-only storage + серверная автоматизация — проверять совместимость сразу

**Seen:** 1
**Adapted:** —
**Triad:** в одной фиче сочетаются client-only хранилище (localStorage, IndexedDB, cookies) и серверная автоматизация (cron, background script, webhook) → до финализации архитектуры проверить: может ли серверный процесс читать/писать в это хранилище → не обнаружить data-access конфликт в середине tech-spec
**Context:** localStorage + ежедневный sync-скрипт были предложены как v1. Поймал конфликт до спека: серверный скрипт не имеет доступа к browser storage — потребовался бы полный backend. Предотвратил ошибочную архитектуру.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-30 photo-crop / session 1: структурные gate-вопросы при конвертации алгоритма в процедурный скилл

**Seen:** 1
**Adapted:** —
**Triad:** конвертация пользовательского алгоритма (список шагов) в процедурный SKILL.md → добавить gate-вопрос («перечисли что определил на этом шаге») в конце каждой фазы, даже если его нет в оригинале → удовлетворить структурные требования процедурного скилла без повторного прогона валидатора
**Context:** пользователь передал 4-шаговый алгоритм для расчёта object-position; первый черновик точно воспроизвёл шаги, но пропустил межфазовые чекпоинты — skill-checker потребовал второй прогон.
**Scope:** situational
**Situation:** создание нового процедурного SKILL.md на основе алгоритма, предоставленного пользователем или взятого из документации
**Category:** sequencing

### 2026-03-30 export-contacts-filter / session 1: Деструктивная операция в пайплайне — фильтр по статусу, не по полю

**Seen:** 1
**Adapted:** —
**Triad:** user-spec описывает delete/cleanup в системе с pipeline-статусами → ограничивать удаление терминальными статусами (enriched/done), не значением поля → не удалить записи ещё в обработке (pending/in-progress)
**Context:** Предложение "удалять дела без телефона при каждом запуске" удалило бы pending-записи, которые просто не дошли до обогащения (квота ofdata исчерпана на середине цикла). Adequacy validator поймал это как critical data loss риск.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 export-contacts-filter / session 1: Сужение фильтра в спеке — документируй исключение явно

**Seen:** 1
**Adapted:** —
**Triad:** spec сужает критерий от обсуждённого в интервью (A or B → только A) → добавить в Технические решения "решили НЕ включать B, потому что..." → не тратить дополнительные раунды валидации на задокументирование очевидного для автора решения
**Context:** В интервью обсуждался фильтр "phone OR email". Spec молча сузил до "только phone". Quality validator 3 раза подряд флажил это как undocumented decision, пока не появилась явная строка "решили не фильтровать по email, потому что нужен отзвон".
**Scope:** universal
**Category:** scope-management

### 2026-04-07 website-design-match / session 1: Визуальная фича — один экран за раз

**Seen:** 2
**Adapted:** —
**Triad:** визуальная фича с несколькими экранами/блоками → показать один экран/блок полностью → дождаться одобрения перед следующим
**Context:** (1) admin-demo сгенерирован за один проход (3 блока × 3 вкладки) — 700+ строк без раннего фидбэка. (2) website-design-match tech-spec поставил 3 страницы в параллельную волну — пользователь сказал "один экран за раз", перестройка волн.
**Scope:** universal
**Category:** design-iteration

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30): Флаг-файл run-once — путь от якоря, не от CWD -->

### 2026-03-30 pipeline-report / session 2: checkpoint.yml не создан при старте второй сессии

**Seen:** 1
**Adapted:** —
**Triad:** многосессионная фича с session-plan → создавать/коммитить checkpoint.yml в конце каждой сессии, не только читать его в начале следующей → предотвратить ситуацию «ожидаемый файл состояния отсутствует» при старте сессии 2+
**Context:** При старте сессии 2 pipeline-report ожидался checkpoint.yml, но файл не был создан в конце сессии 1. Сессия 1 завершилась коммитом кода, но без явного шага создания state-файла — checkpoint.yml не входил в outputs сессии 1 по session-plan.
**Scope:** situational
**Situation:** multi-session feature execution с явным session-plan и передачей состояния между сессиями
**Category:** sequencing

### 2026-03-30 export-contacts-filter / session 2: Audit-волна ловит cross-task баги невидимые per-task ревьюеру

**Seen:** 1
**Adapted:** —
**Triad:** завершение implementation-волн в multi-task фиче → запустить code + security + test аудиты параллельно в отдельной волне → поймать баги из взаимодействия задач, невидимые для ревьюера отдельного diff-а
**Context:** Per-task ревьюеры одобрили Task 1 (флаг-файл создан). Audit-волна нашла major finding: путь к флаг-файлу CWD-relative — проблема возникает из контекста deployment, а не из diff отдельной задачи.
**Scope:** situational
**Situation:** multi-task feature с 3+ implementation задачами в разных файлах
**Category:** sequencing

### 2026-03-30 juridical-parser / deploy: Метрика в статус-дашборде — уточни временной горизонт

**Seen:** 1
**Adapted:** —
**Triad:** добавление метрики в status/dashboard без явного требования → уточнить у пользователя: за текущий запуск или за всё время → не додумывать горизонт самостоятельно, он варьируется
**Context:** Реализовал счётчики обогащения как SQL-агрегат по всей БД. Пользователь поправил: нужно за текущий запуск. Разные метрики могут требовать разных горизонтов в зависимости от задачи.
**Scope:** universal
**Category:** scope-management

### 2026-03-31 juridical-parser / session: clear() не сбрасывает форматирование во внешних сервисах

**Seen:** 1
**Adapted:** —
**Triad:** вызов clear()/reset() на внешнем сервисе перед записью новых данных → явно сбрасывать ВСЕ слои состояния (контент + форматирование + кэш) → предотвратить проявление предыдущего состояния после "очистки"
**Context:** ws.clear() в Google Sheets очищает ячейки, но не форматирование — красные цвета от предыдущего вызова оставались на новых строках.
**Scope:** universal
**Category:** tool-selection

### 2026-03-31 juridical-parser / session: production-аномалия может объясняться старой версией кода

**Seen:** 1
**Adapted:** —
**Triad:** production данные не соответствуют поведению текущего кода → сверить timestamp задеплоенного файла с временем запуска → не искать баг в коде который уже правильный
**Context:** was_incomplete=1 в БД при корректном коде — оказалось, фикс был задеплоен ПОСЛЕ прогона, т.е. прогон выполнялся на старом коде.
**Scope:** universal
**Category:** recovery

### 2026-03-31 juridical-parser / session: уточни ownership сервера до деплоя

**Seen:** 1
**Adapted:** —
**Triad:** выполнение deploy-команды в проекте клиента → уточнить чей сервер и кто контролирует деплой-процесс ДО выполнения → не произвести несогласованное изменение на продакшене клиента
**Context:** Задеплоил файлы напрямую на VPS через scp, не уточнив что это продакшен клиента, а не тестовый сервер разработчика.
**Scope:** situational
**Situation:** Работа над проектами внешних клиентов, где deploy-инфраструктура принадлежит клиенту
**Category:** communication

### 2026-03-31 juridical-parser / session ad-hoc: изолированный вызов компонента вместо полного пайплайна

**Seen:** 1
**Adapted:** —
**Triad:** запрос на обновление одного компонента системы (статус, отчёт, вкладка) → вызвать только этот компонент изолированно через минимальный скрипт → не тратить ресурсы полного пайплайна и не вызывать побочных эффектов
**Context:** Пользователь попросил обновить статус-вкладку — запустил полный пайплайн с парсером, сжёг API-квоту клиента.
**Scope:** universal
**Category:** scope-management

### 2026-03-31 dashboard-v1 / task-decomposition: stub-ownership gap при межзадачных placeholder-ах

**Seen:** 1
**Adapted:** —
**Triad:** задача N создаёт no-op stubs "для следующих задач" → в бриф каждой заполняющей задачи явно добавить шаг "замени no-op stub на реализацию" → гарантировать что placeholder не останется no-op в рабочем коде
**Context:** Task 4 создала 6 handler-стабов в App.jsx "для Wave 4". Tasks 5 и 6 описывали как вызывать хендлеры, но не содержали шага замены стаба реальной имплементацией. Cross-task ревьюер поймал это: verify-user провалился бы — reload → данные не сохраняются.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 dashboard-v1 / deploy: SSH + sudo в GitHub Actions CI деплое

**Seen:** 1
**Adapted:** —
**Triad:** GitHub Actions SSH step выполняет `sudo service-name reload` от deploy-пользователя → убрать sudo из reload-команды (или настроить NOPASSWD в sudoers заранее), добавить `-o StrictHostKeyChecking=no` в SSH-команду → не получать permission denied на первом CI деплое
**Context:** deploy.yml использовал `sudo nginx -s reload` — deploy user не имел sudo. Плюс StrictHostKeyChecking блокировал first-time connect в CI. Итого 8 fix-коммитов.
**Scope:** universal
**Category:** sequencing

### 2026-03-31 employee-cabinet / session 1: уточнять регион и регуляторику ДО предложения стека

**Seen:** 1 (employee-cabinet/session 1)
**Adapted:** —
**Triad:** предложение хостинг/стека для нового проекта → уточнить регион развёртывания и регуляторные ограничения ДО предложения решений → не переписывать архитектурный стек после обсуждения
**Context:** Предложил Supabase+Railway, затем узнал что проект в России (152-ФЗ, данные граждан РФ) — пришлось полностью менять стек на PostgreSQL+Timeweb VPS.
**Scope:** universal
**Category:** information-gathering

## Universal

### 2026-03-31 employee-cabinet / session 1: проверять тип БД-объекта до init-кода адаптера

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** подключение адаптера внешней библиотеки к БД → проверить ожидаемый тип объекта (raw driver vs query builder) в docs ДО написания init-кода → не получить runtime ошибку несовместимости адаптера на первом запросе
**Context:** better-auth принимает Kysely-инстанс, мы передали pg.Pool → `db.selectFrom is not a function` при первом login
**Scope:** universal
**Category:** tool-selection

### 2026-03-31 employee-cabinet / session 2: новая роль mid-interview → немедленная матрица прав

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** новая роль появляется в середине user-spec интервью → немедленно составить матрицу "роль × ключевые возможности" и согласовать с пользователем до продолжения → не тратить 3+ батча на выяснение пересечений между ролями
**Context:** Пользователь ввёл роль "руководитель" mid-interview — потребовалось 3 батча чтобы выяснить что она почти совпадает с admin, после чего роль вынесли в отдельную фичу.
**Scope:** situational
**Situation:** user-spec интервью для приложений с несколькими ролями пользователей
**Category:** scope-management

### 2026-03-31 employee-cabinet / session 1: мокировать инфраструктурную зависимость чтобы разблокировать демо

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** демонстрация UI застряла из-за нерабочей инфраструктурной зависимости (auth, БД, API) → замокировать зависимость локально в компоненте → не блокировать оценку UX из-за инфраструктурной проблемы
**Context:** better-auth не работал локально, пользователь не мог увидеть кабинет → подставили mock-session прямо в компонент и убрали guard в middleware
**Scope:** universal
**Category:** recovery

### 2026-04-01 dashboard-v1 / session post-deploy: nginx server_name conflict detection

**Seen:** 1
**Adapted:** —
**Triad:** диагностика недоступности nginx снаружи → запустить `nginx -T | grep -B2 -A10 server_name` → обнаружить конфликт server blocks за один шаг
**Context:** два server block претендовали на server_name 217.114.2.159 — dashboard и levelupme (certbot). Ручной просмотр каждого конфига занял бы несколько шагов.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 dashboard-v1 / session post-deploy: мобильный оператор блокирует HTTP по IP

**Seen:** 1
**Adapted:** —
**Triad:** сервис доступен через curl с сервера (порт 80), но браузер на мобильном зависает → уточнить "по домену или по IP" до диагностики nginx/сети → не тратить время на network-диагностику
**Context:** nginx отвечал 401 на curl, curl с ноутбука работал, а с телефона через 4G зависал без ошибки — причина в блокировке прямых HTTP-запросов по IP у мобильного оператора.
**Scope:** situational
**Situation:** мобильный интернет российских операторов, сервис доступен только по IP
**Category:** recovery

### 2026-04-01 employee-cabinet / session decompose: параллельные тесты — изолировать seed по email

**Seen:** 1
**Adapted:** —
**Triad:** два параллельных теста пишут в общую тестовую БД через одного seed-пользователя → использовать разные email-константы для каждой тестовой задачи → избежать teardown race condition при параллельном выполнении
**Context:** Tasks 9 (integration) и 10 (E2E) в одной волне оба пишут в TEST_DATABASE_URL. globalSetup Task 10 чистил timesheets seeded-user в момент когда integration-тесты Task 9 могли ещё работать.
**Scope:** situational
**Situation:** параллельное выполнение нескольких тестовых задач против одной тестовой БД
**Category:** problem-decomposition

### 2026-04-01 dashboard-progress-sync / userspec: подтвердить порядок фич до инициализации папки

**Seen:** 1
**Adapted:** —
**Triad:** пользователь описывает несколько взаимосвязанных фич для реализации → явно уточнить порядок реализации ДО инициализации папки первой фичи → не создавать и переименовывать артефакты под неправильную фичу
**Context:** Сессия стартовала с `/new-user-spec dashboard-crm`, папка создана — но пользователь уточнил что первой фичей должен быть progress-sync, а не CRM. Папку пришлось переименовывать.
**Scope:** situational
**Situation:** пользователь приносит несколько готовых спеков или модулей в одной сессии
**Category:** scope-management

### 2026-04-01 dashboard-progress-sync / userspec: проверять наличие файлов в git до GitHub API в AC

**Seen:** 1
**Adapted:** —
**Triad:** фича читает файлы методологии (work/, checkpoint.yml) через GitHub Contents API → уточнить у пользователя закоммичены ли эти файлы в репозитории ДО написания AC → не получить "прогресс не отслеживается" для всех проектов из-за .gitignore
**Context:** В спеке предполагалось читать checkpoint.yml через GitHub API для % прогресса — но пользователь подтвердил что work/ нередко в .gitignore. Потребовалось добавить fallback-ветку "прогресс не отслеживается".
**Scope:** situational
**Situation:** планирование фичи с GitHub API доступом к файлам в репозиториях пользователя
**Category:** information-gathering

## Universal

### 2026-04-01 freelance-dashboard / session design-refactor: JS viewport state — признак отсутствия CSS architecture

**Seen:** 1
**Adapted:** —
**Triad:** JS state существует только для переключения CSS-значений по viewport → заменить state+listener на CSS media queries + className → убрать re-renders и сделать layout управляемым CSS
**Context:** App.jsx и ProjectModal.jsx содержали `isMobile` state + resize listener только для выбора между двумя наборами inline styles
**Scope:** universal
**Category:** tool-selection

### 2026-04-07 website-design-match / session 1: Пропуск тяжёлой валидации при чётком style-only scope

**Seen:** 1
**Adapted:** —
**Triad:** user-spec для style-only рефакторинга с полным аудитом параметров → пропустить тяжёлых валидаторов (opus) или запускать только лёгкий (sonnet) → не терять часы на зависшие агенты при нулевом риске архитектурных ошибок
**Context:** Запуск двух валидаторов (quality-sonnet + adequacy-opus) для CSS-only user-spec привёл к зависанию на 3+ часа. Пользователь перезапускал сессию 5 раз. Валидация была пропущена без последствий — scope очевиден.
**Scope:** universal
**Category:** scope-management

### 2026-04-09 multi-trees-sharing / techspec: cross-check edge case descriptions across tasks

**Seen:** 2
**Adapted:** —
**Triad:** две задачи описывают поведение/scope для одного ресурса или edge case → cross-check описания обеих задач на консистентность до коммита → предотвратить противоречие пойманное только валидатором
**Context:** (1) multi-trees-sharing: Task 5 (store) "deleteTree creates 'Моё дерево'" vs Task 7 (UI) "show EmptyState when last deleted". Completeness validator round 2. (2) shared-whisper-service: Task 4 "no hardening for said-done-bot.service" vs Task 6 AC "all systemd units have PrivateTmp". Tech-spec TAC10 generic term "systemd units" → task-creators интерпретировали scope по-разному. Reality-checker cross-task check.
**Scope:** universal
**Category:** sequencing

### 2026-04-12 responsive-layout / decompose: Вычислять relative paths для каждого task-creator, не копировать

**Seen:** 2 (merged from #187)
**Adapted:** —
**Triad:** параллельные task-creator'ы используют relative paths (import, @use, context files), файлы на разной глубине вложенности → вычислить и передать конкретный путь в каждом брифе → предотвратить нерабочие пути из-за разной глубины файлов
**Context:** (1) responsive-layout: Task 3 задокументировал `@use '../../app/globals.scss'`, но Tasks 5, 6, 8 модифицируют файлы на глубине 3-4 уровня. Cross-task reality checker поймал 4 неверных пути. (2) предыдущий: app-relative paths в tech-spec при вложенной app директории.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 freelance-dashboard / session design-refactor: дизайн-пайплайн на приложении с inline styles → CSS migration приоритет

**Seen:** 1
**Adapted:** —
**Triad:** design-system-init запущен на существующем приложении с inline styles → пропустить interview, экстрактировать токены из кода, выполнить CSS migration → переключить source-of-truth стилей, а не задокументировать существующие значения
**Context:** дизайн-пайплайн вызван для React-дашборда с 200+ inline styles; пользователь сказал "всё нравится, просто сделай как надо"
**Scope:** situational
**Situation:** существующий React/Vue/Svelte проект с inline styles + пользователь одобрил текущую эстетику
**Category:** design-process

### 2026-04-01 dashboard-progress-sync / session 1: Верификационный curl без auth = ложный положительный

**Seen:** 1 (this feature/session)
**Adapted:** —
**Triad:** curl-команда в AVP/user-spec для endpoint с auth → проверить что команда включает auth header + добавить отдельный тест без ключа → 401 → не получить false QA pass при сломанной авторизации
**Context:** user-spec содержал curl POST без X-Api-Key; если бы auth middleware был сломан, команда вернула 200 — агент зафиксировал бы успех, не обнаружив проблему
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 juridical-parser / ops: изменение расписания «с завтрашнего дня»

**Seen:** 1
**Adapted:** —
**Triad:** пользователь просит изменить расписание «с завтрашнего дня» при наличии ближайшего запуска → проверить время ближайшего запуска и применить изменение ПОСЛЕ него → не потерять плановый прогон из-за немедленного переключения
**Context:** Крон стоял на 00:30 UTC, пользователь попросил переключить на 21:30 UTC «с завтрашнего дня» — изменение применили немедленно, ближайший запуск через 13 минут был пропущен.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 1: HTTP-сервер с API key auth — security must-have в первой реализации

**Seen:** 1
**Adapted:** —
**Triad:** реализация HTTP-сервера с API key auth → включить timing-safe comparison (`crypto.timingSafeEqual`) и явный body size limit в первоначальную реализацию → не тратить review-раунд на предсказуемые security best practices
**Context:** Task 1 — первая реализация server/index.js сравнивала API key через `===`. Review round 1 нашла timing attack и отсутствие body limit. Пришлось коммитить fix-раунд. Обе находки предсказуемы для любого auth middleware.
**Scope:** situational
**Situation:** реализация HTTP-сервера с токен/key-based auth
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 1: Helper с null/undefined — верифицируй граничные значения до review

**Seen:** 1
**Adapted:** —
**Triad:** helper-функция принимает значение из внешнего источника (API-ответ, env var, user input) → вручную проверить edge cases (null, undefined, пустая строка, 0) перед первым review → не получать post-review fix на предсказуемые null/boundary guards
**Context:** Task 4 — `calcCommitDays(isoDateString, now)` принимала значение из GitHub API. Review нашло: при `null` передаётся в `new Date(null)`, что возвращает epoch (0 ms). Исправление: добавить `typeof isoDateString !== 'string'` guard. Предсказуемый граничный случай для любой функции, работающей с внешними данными.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 2: вынести числовые threshold в константы до review

**Seen:** 1
**Adapted:** —
**Triad:** задача с числовым threshold в коде → вынести magic numbers в именованные константы до первого review → не тратить review-раунд на предсказуемые hardcoded value замечания
**Context:** Task 3 (Frontend Progress column) — reviewer нашёл magic number `3` (stale days threshold). Понадобился дополнительный fix-коммит и второй review-раунд.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 juridical-parser / ops-2: позиция фильтра в pipeline

**Seen:** 1
**Adapted:** —
**Triad:** конфиг содержит whitelist/фильтр для ограничения обработки → явно уточнить на каком этапе pipeline применяется фильтр (сбор данных vs экспорт) и согласовать с пользователем → не тратить ресурсы (квоту/время) на обработку данных которые всё равно отфильтруются
**Context:** Whitelist по судам фильтровал только экспорт в Sheets, но не парсинг — квота тратилась на все 54 суда, хотя пользователь обсуждал ограничение до 2.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 juridical-parser / session fix-status: семантика метрики перед патчем симптома

**Seen:** 1
**Adapted:** —
**Triad:** метрика показывает логически невозможное значение (A < B где A должно быть ≥ B) → установить семантическое определение каждой метрики ДО трейсинга кода → найти структурный баг вместо маскировки симптома
**Context:** found=0 при exported=2 — предложил `found = max(found, exported)` как фикс, пользователь поймал что логика неверна; оказалось found и exported считались из разных pipeline-стадий с разной семантикой.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 juridical-parser / session fix-status: некорректное значение в БД — трейс write paths

**Seen:** 1
**Adapted:** —
**Triad:** поле БД содержит значение неверного формата (не NULL и не ожидаемый тип) → найти ВСЕ пути записи в это поле включая legacy-код и дефолты схемы → не создавать cleanup под гипотезу без верификации причины
**Context:** exported_to_sheets = '0' блокировало дела в очереди; гипотеза "whitespace phone" оказалась неверной — причина в legacy формате (булево 0 вместо NULL из старого кода).
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 juridical-parser / session fix-status-2: формулировка остаточной проблемы через user-observable state

**Seen:** 1
**Adapted:** —
**Triad:** формулировка остаточной проблемы в session-end промте → верифицировать каждую проблему против того что пользователь видит в UI/выводе, а не против внутреннего состояния кода → не направить следующую сессию решать неверно идентифицированную проблему
**Context:** В промте описал проблему как "found/exported semantics в export_log" (code-internal), пользователь поправил: реальная проблема — "цифры в статусе не совпадают с содержимым таблицы" (user-observable).
**Scope:** universal
**Category:** communication

### 2026-04-01 employee-cabinet / userspec-amendment: Правки клиента после одобрения спека — точечный амендмент

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** клиент присылает правки к user-spec со статусом approved → задать вопросы только по неоднозначным пунктам, обновить существующий spec напрямую → не запускать полный интервью-цикл заново
**Context:** Клиент прислал 4 уточнения к уже одобренной спеке. Правильным шагом была не новая спека, а точечное мини-интервью и прямое обновление документа.
**Scope:** situational
**Situation:** client feedback arrives after user-spec is already approved
**Category:** scope-management

### 2026-04-01 employee-cabinet / userspec-amendment: UI микро-детали в spec — предлагать стандартный паттерн

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** user-spec интервью требует уточнения UI-расположения элемента (где/как панель, тулбар, диалог) → применить стандартный UX паттерн без вопроса к пользователю → не блокировать интервью на деталях, которые пользователь не может сформулировать
**Context:** Задал абстрактный вопрос "панель или диалог?" — пользователь ответил "не понял вопроса, посоветуйся с дизайн-пайплайном". Нужно было выбрать стандартный паттерн самостоятельно.
**Scope:** situational
**Situation:** уточнение UI-деталей в ходе user-spec или design-spec интервью
**Category:** scope-management

### 2026-04-01 employee-cabinet / techspec-update: Gap-анализ перед написанием задач на обновлённый спек

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** обновление user-spec к уже реализованной фиче → запустить code-researcher для diff новых требований против существующего кода перед написанием задач → не создавать задачи для уже реализованного функционала
**Context:** `/new-tech-spec` запустили после завершения реализации всех 15 задач. User-spec обновили с клиентским фидбеком. Без code-researcher gap-анализа риск — написать 5-7 задач из которых 3-4 уже реализованы.
**Scope:** situational
**Situation:** обновление tech-spec для фичи, реализация которой уже завершена (есть решённые задачи)

### 2026-04-01 employee-cabinet / task-decomposition: Implementation hints должны отражать реальный код, а не идеальный

**Seen:** 2 (employee-cabinet, court-flags-separation)
**Adapted:** —
**Triad:** task-creator пишет hints для файла, который уже реализован в кодовой базе → прочитать фактический код файла ДО написания hints → не создавать hints противоречащие существующей реализации
**Context:** task-creator для Task 5 написал hint про `fs.createReadStream+Readable.toWeb()`, хотя реальный файл использовал `fs.readFile+NextResponse(buffer)`. Task 6 имел `authClient.forgetPassword()` вместо реального `authClient.requestPasswordReset()`. Reality-checker поймал оба в round 1. Повтор: court-flags-separation task 1 — hints ссылались на `self.base_url` и `self.public_key` (не существуют), тогда как реальные атрибуты `self._session`, `self._public_key` (private). Task 12 — SQLite path `/src/db/juridical.db` вместо реального `/data/cases.db`. Паттерн устойчив: orchestrator не читает код перед брифингом task-creator → hints генерируются по аналогии с типичными паттернами.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 employee-cabinet / task-decomposition: TDD Anchor не должен называть файл, являющийся deliverable другой задачи

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** TDD Anchor задачи A называет тестовый файл, который является primary deliverable задачи B → убрать тест из TDD Anchor A, добавить "интеграционное покрытие в задаче B" → один файл — один владелец, нет конфликта владения при параллельном выполнении
**Context:** Task 5 имел TDD Anchor с двумя тестами в `tests/integration/certificates.test.ts`. Но этот файл — primary deliverable Task 9. Кросс-задачная проверка обнаружила конфликт: Task 9 мог перезаписать нуль файла при создании с нуля.
**Scope:** situational
**Situation:** multi-task фича с разделёнными задачами реализации и тестирования (задача X делает API, задача Y делает тесты для него)
**Category:** information-gathering

### 2026-04-01 employee-cabinet / session 2: auth-библиотека возвращает 200 на duplicate flow — тестировать через side effect

**Seen:** 1 (employee-cabinet/session 2)
**Adapted:** —
**Triad:** интеграционный тест проверяет ошибочный сценарий (duplicate signup) через auth-библиотеку → проверять через side effect (DB row count), не HTTP статус → не получить false-negative когда библиотека возвращает 200 с resend-flow вместо 400
**Context:** better-auth v1.5.6 при повторном signup возвращает 200 (resend verification), а не 400. Тест ожидал 400 → упал; исправление — проверять count строк в users.
**Scope:** universal
**Category:** tool-selection

### 2026-04-01 employee-cabinet / session 2: E2E global-setup — прямой INSERT вместо sign-up через API

**Seen:** 2 (employee-cabinet/session 2, cert-report/session 1)
**Adapted:** —
**Triad:** integration/E2E setup требует seeded users → прямой INSERT в DB вместо sign-up API → устранить зависимость от application layer и избежать rate-limit (4+ signup за сессию бьёт better-auth 429)
**Context:** employee-cabinet/session 2: Task 10 global-setup делал POST /api/auth/sign-up + SQL UPDATE — переписан на прямой INSERT. cert-report/session 1: Task 8 — 4 тестовых пользователя через seedUser + getSessionCookies хитили better-auth rate-limit; no-cert user добавлен прямым DB INSERT как обходной путь.
**Scope:** situational
**Situation:** integration/E2E-тесты с 3+ pre-seeded users при auth-библиотеке с rate-limiting
**Category:** tool-selection

### 2026-04-01 juridical-parser / diagnostic session: Смена параметра API меняет nullable fields ответа

**Seen:** 1
**Adapted:** —
**Triad:** добавление нового параметра к существующему API-запросу → проверить nullable поля ответа при новом параметре на реальных данных → не получить TypeError на production-прогоне
**Context:** После добавления `Court=` фильтра в поиск parser-api.com ответ стал возвращать `Respondents: null` вместо `[]` — мок-тесты не покрывали этот кейс, `TypeError` проявился только на production.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 juridical-parser / diagnostic session: Многострочный скрипт на удалённом VPS — записать в файл, не инлайн

**Seen:** 2
**Adapted:** —
**Triad:** выполнение нетривиального Python-скрипта на удалённом сервере через SSH → записать скрипт в локальный файл, залить по SFTP, выполнить через `python3 -u` → избежать ошибок экранирования и буферизации вывода
**Context:** 3 попытки запустить Python через inline heredoc/параметры shell — каждый раз ошибки экранирования кавычек или пустой output из-за буферизации. Фикс: Write tool в локальный файл → sftp.put() → запуск с `-u`. (Seen 2: 2026-04-18 juridical-parser recovery session — снова множественные SyntaxError через `python3 -c`, пользователь прямо указал на паттерн.)
**Scope:** situational
**Situation:** выполнение скриптов на удалённом VPS через paramiko/SSH
**Category:** tool-selection

### 2026-04-01 methodology-cleanup / session 1: разграничить "убрать из репо" и "удалить с диска"

**Seen:** 1
**Adapted:** —
**Triad:** запрос "удалить X из репозитория" для локального git-репо → уточнить: git untrack (git rm --cached + .gitignore) или физическое удаление с диска → не уничтожить локальные файлы при git-операции
**Context:** Попросили убрать 4 скилла из репозитория; выполнил rm -rf вместо git rm --cached — пришлось восстанавливать из git-истории
**Scope:** universal
**Category:** recovery

### 2026-04-02 geologist-cabinet / planning session: Конфиг у провайдера — спросить клиента раньше поддержки

**Seen:** 1
**Adapted:** —
**Triad:** нужно получить конфигурацию у провайдера (DNS, настройки) → сначала спросить клиента — есть ли доступ к панели управления → избежать ожидания support-ответа если клиент может получить данные сам
**Context:** Подготовил развёрнутое письмо в поддержку Creatium для получения DNS-записей. Клиент сам открыл панель и прислал скриншот со всеми записями — ответ поддержки не понадобился.
**Scope:** situational
**Situation:** получение конфигурационных данных (DNS, API-ключи, настройки) у стороннего провайдера через клиента-посредника
**Category:** information-gathering

### 2026-04-02 moneymaker / session 1: числовой атрибут AI-генерируемых элементов — источник должен быть в интервью

**Seen:** 1
**Adapted:** —
**Triad:** фича генерирует список элементов и каждый имеет числовой атрибут (цена, оценка, балл) → в интервью явно задать вопрос "кто/что устанавливает это значение: LLM-оценка, каталог пользователя или ручной ввод?" → не допустить CRITICAL gap в архитектуре вычислений, обнаруживаемый только на валидации
**Context:** Moneymaker user-spec: /expand показывает апсейл-предложения с ценами и маржой. Интервью не спросило откуда берётся цена для LLM-генерируемых позиций. Adequacy validator вернул CRITICAL: "модель ценообразования не определена". Ответ (каталог блоков × ставка) получен только в батче Q20–Q21 после валидации.
**Scope:** situational
**Situation:** user-spec интервью для фичи где AI генерирует элементы с ценой, рейтингом или любым числовым атрибутом, который будет показан пользователю
**Category:** information-gathering

### 2026-04-02 dashboard-progress-sync / session 3: Pre-flight SSH smoke перед VPS deploy

**Seen:** 1
**Adapted:** —
**Triad:** деплой на VPS впервые или после смены домена/secrets → запустить SSH smoke (`ssh -i deploy_key user@host echo ok`) локально ДО push в main → не тратить N trigger-redeploy циклов на последовательные инфраструктурные блокеры
**Context:** Task 12 заблокировался 4 последовательными блокерами: неверный URL, отсутствующий secret, fail2ban, отсутствующий authorized_keys. Каждый обнаруживался только после fix предыдущего через failed CI run — итого 3 trigger-redeploy коммита, задача не завершена.
**Scope:** universal
**Category:** sequencing

### 2026-04-02 moneymaker / session 2 (tech-spec): Решение, сужающее утверждённый AC — проверить до написания

**Seen:** 3
**Adapted:** —
**Triad:** tech-spec decision сужает или откладывает требование из user-spec → перед написанием Decision проверить AC user-spec; если отклонение согласовано — обновить AC user-spec в том же шаге, не оставлять рассинхрон → не вводить scope reduction без согласования и не оставлять upstream-доку противоречащей
**Context:** Tech-spec Decision 6 отложил "free-form rate update" в Phase 2, мотивируя тем что это "не в AC". Completeness-validator вернул CRITICAL: AC явно есть. (Seen 2: panel-next-run — Decision 4 изменил код ответа batch с 409 на 200+skipped; таблица проверки в user-spec указывала 409. Поймал skeptic.) (Seen 3: cabinet-sources-api — tech-spec Decision 5 отложил product_feed.auth; отклонение БЫЛО согласовано с владельцем, но AC user-spec не обновили → completeness FAIL + skeptic + security сошлись на конфликте доков. Урок: даже согласованное отклонение требует синка upstream-AC в том же шаге.)
**Scope:** universal
**Category:** scope-management

### 2026-04-02 moneymaker / session 2 (tech-spec): Задача создаёт SKILL.md — skill-master, не code-writing

**Seen:** 1
**Adapted:** —
**Triad:** deliverable задачи — SKILL.md файл(ы) → назначить skill: skill-master и reviewers: skill-checker → не получить неверный skill/reviewer замеченный только валидаторами
**Context:** Первый черновик tech-spec для moneymaker назначил `write-code` (затем `code-writing`) для задач 1–5, создающих SKILL.md. Skeptic и template-validator поймали: для создания скиллов в skills-and-reviewers каталоге прописан `skill-master` + `skill-checker`.
**Scope:** situational
**Situation:** tech-spec для фичи, deliverable которой является набор Claude Code skills (SKILL.md файлы)
**Category:** tool-selection

### 2026-04-02 geologist-cabinet / deploy session: better-auth 404 при неверном BETTER_AUTH_URL prefix

**Seen:** 1
**Adapted:** —
**Triad:** better-auth handler возвращает 404 для корректного пути → проверить BETTER_AUTH_URL на наличие лишнего path prefix → не тратить часы на отладку webpack и маршрутизации
**Context:** BETTER_AUTH_URL был установлен как `http://host/cabinet` в прошлой сессии; better-auth добавлял `/cabinet` к своему basePath и не находил `/api/auth/sign-in/email`.
**Scope:** situational
**Situation:** деплой приложения с better-auth за nginx reverse proxy с subpath (например `/cabinet`)
**Category:** recovery

### 2026-04-02 geologist-cabinet / deploy session: Next.js API route молча возвращает 404 из-за async webpack модуля

**Seen:** 1
**Adapted:** —
**Triad:** Next.js API route возвращает 404 с RSC headers, console.error не срабатывает → проверить compiled route.js на `import("dependency")` и `t.a(e,` async factory → диагностировать silent module initialization failure
**Context:** better-auth внутри использует `import("pg")` (dynamic ESM import); webpack компилировал это как async module factory; Next.js 14 не мог загрузить route handler и возвращал App Router 404 без каких-либо логов.
**Scope:** situational
**Situation:** Next.js 14 App Router, серверный route handler использует библиотеку (better-auth, prisma и др.) с внутренними dynamic ESM imports
**Category:** recovery

### 2026-04-02 geologist-cabinet / certificates-ui: директории для файлов не создаются при деплое автоматически

**Seen:** 1
**Adapted:** —
**Triad:** фича пишет файлы на диск в директорию которой нет -> явно включить mkdir директории в деплой-чеклист -> не получить ENOENT на первом upload после деплоя
**Context:** API загрузки PDF-сертификатов писал файлы в uploads/. Директория не существовала на сервере — git-клон не создаёт пустые директории. Первый upload упал с ENOENT, пришлось создавать вручную через SSH.
**Scope:** universal
**Category:** sequencing

### 2026-04-02 employee-cabinet / session certificates-ux: Уточнять ожидание перед диагностикой UI-feedback

**Seen:** 1
**Adapted:** —
**Triad:** пользователь говорит "название/значение кривое" без указания поля или ожидаемого вида → переспросить "что именно ожидаешь увидеть и где" → не тратить итерацию на ложную версию проблемы
**Context:** Пользователь сказал "название кривое" — предположили что речь про имя файла на диске, начали объяснять. Оказалось речь про отображение в таблице в UI. Потребовалось 3 сообщения для диагностики.
**Scope:** universal
**Category:** communication

### PROMOTED → skill-master: pre-submission SKILL.md structural checks

### 2026-04-02 employee-cabinet / session Wave5-deploy: Next.js build cache маскирует "module not found"

**Seen:** 1
**Adapted:** —
**Triad:** Next.js dev-сервер возвращает 500 "Cannot find module vendor-chunks/X" → удалить .next и перезапустить сервер → не тратить время на диагностику зависимостей которых нет
**Context:** Интеграционные тесты упали с 500 на всех auth-эндпоинтах. Ошибка выглядела как отсутствующая зависимость better-auth. Реальная причина — сталый .next кеш от предыдущего билда другой ветки.
**Scope:** situational
**Situation:** Next.js проект, dev-сервер запущен без предварительного rm -rf .next после смены ветки или обновления зависимостей
**Category:** recovery

### 2026-04-02 employee-cabinet / session Wave5-tasks: Проверять реализацию до кодирования задачи

**Seen:** 1
**Adapted:** —
**Triad:** задача бэклога описывает добавление guard/validation в существующий файл → прочитать целевой файл до написания кода → не дублировать уже существующую реализацию
**Context:** Task 17 (client-side валидация PDF) значилась как "to implement". Чтение cabinet/page.tsx показало что оба гарда (type + size) уже присутствовали — добавлены как byproduct предыдущей волны. Задача свелась только к написанию теста.
**Scope:** universal
**Category:** information-gathering

### 2026-04-02 moneymaker / session 2: Bash path-substitution в аргументе флага — вынести в переменную

**Seen:** 1
**Adapted:** —
**Triad:** bash команда передаёт `$(find ... | cut ...)` как путь в флаг принимающий файловый путь (-newer, -nt, аналогичные) → вынести подстановку в именованную переменную отдельной командой → избежать молчаливого false-result при путях с пробелами
**Context:** В moneymaker-expand SKILL.md staleness check сравнивал mtime через `find -newer "$(find ... | cut ...)"`. skill-checker поймал: если путь материала содержит пробел, вложенная подстановка обрезается и флаг -newer получает неверный путь — всегда возвращая STALE без ошибки.
**Scope:** universal
**Category:** tool-selection

### 2026-04-02 moneymaker / session 2: Embedded LLM prompts в SKILL.md подпадают под правило positive instructions

**Seen:** 1
**Adapted:** —
**Triad:** SKILL.md содержит inline LLM-промт (блок текста как инструкция для LLM внутри фазы) → проверить весь текст промта на "do not / don't / не делай" и переформулировать позитивно → не тратить review-раунд на нарушение skill-master правила внутри вложенного промта
**Context:** moneymaker-expand Phase 5 содержал LLM-промт с "Do not produce a generic checklist". skill-checker поймал три места с негативными формулировками внутри промтов. Авторы воспринимают вложенный промт как "данные", а не инструкции, и не применяют к нему skill-master правило.
**Scope:** situational
**Situation:** Написание SKILL.md содержащего встроенные LLM-промты как часть фаз
**Category:** sequencing

### 2026-04-02 moneymaker / session 3: OPEN security risk в audit wave → fix before QA

**Seen:** 1
**Adapted:** —
**Triad:** audit wave находит OPEN security risk в продукте работающем с чувствительными данными → создать ad-hoc fix task и починить ДО запуска QA волны → не деплоить с известной утечкой чувствительных данных и не тратить QA на устранимый fail
**Context:** Security audit moneymaker нашёл 2 OPEN риска: billing exposure (INN/банк в чат-истории при setup) и отсутствие chmod на config.yml. Встал выбор: deferred known issues или fix перед QA. QA шаг 2 (`cat config.yml`) показал бы INN в чате — QA упал бы на устранимом риске.
**Scope:** situational
**Situation:** audit wave завершена, найдены OPEN security risks, следующий шаг — QA волна
**Category:** sequencing

### 2026-04-02 moneymaker-case / session 1: первый пример раскрывает категориальную структуру

**Seen:** 1
**Adapted:** —
**Triad:** проектирование хранилища знаний / экспертного инструмента, пользователь даёт первый реальный пример → спросить "какую логическую категорию/паттерн представляет этот пример?" до финализации полей данных → создать модель данных, захватывающую переносимую структуру, а не только данные экземпляра
**Context:** Скилл moneymaker-case начинался как простое хранилище кейсов. Первый же пример от пользователя (кабинет геолога) содержал прогрессию ролей. Только уточняющий вопрос "что важно выявлять в логике?" вскрыл необходимость patterns/ слоя и трёхслойной архитектуры.
**Scope:** situational
**Situation:** проектирование knowledge storage, expert tool, или любого инструмента накопления опыта
**Category:** problem-decomposition

### 2026-04-02 moneymaker-case / session 1: "нельзя упрощать" = сигнал пропущей абстракции

**Seen:** 1
**Adapted:** —
**Triad:** пользователь отвергает предложенное упрощение архитектуры ("нельзя упрощать", "нужно качественнее") → переспросить "какое различие теряется при упрощении?" до продолжения → выявить пропущую ключевую абстракцию до реализации
**Context:** Предложил Option A (cases only, LLM выводит паттерны сам) как более простой вариант. Пользователь отверг: "упрощать нельзя". Это сигнализировало о том, что явные цепочки прогрессии — не nice-to-have, а ключевое различие в ментальной модели пользователя.
**Scope:** universal
**Category:** information-gathering

### 2026-04-02 moneymaker-setup / session 4: свободный бизнес-текст → выяснить намерение до вызова скилла

**Seen:** 1
**Adapted:** —
**Triad:** пользователь описывает бизнес-практику в свободной форме без вызова скилла, потенциально затрагивая несколько инструментов → задать 3 целевых вопроса (тип: факт/гипотеза; область: какие проекты; цена: формула/якорь/реализованная) ДО вызова любого скилла → не записать в неверный формат и не упустить второй нужный target
**Context:** Пользователь написал "можно предложить брендбук за 20% от проекта" — без указания скилла. Вопросы выявили: гипотеза (не кейс) + любой проект с дизайном + психологический якорь цены. Итог: изменение SKILL.md (hypothesis type) И запись в каталог.
**Scope:** situational
**Situation:** пользователь пишет о бизнес-практике/апселле без явного вызова moneymaker-скилла
**Category:** information-gathering

### 2026-04-02 moneymaker-setup / session 4: все данные в задании → пропустить interview-фазы

**Seen:** 1
**Adapted:** —
**Triad:** скилл предполагает интерактивный сбор данных, но задание уже содержит все необходимые поля → пропустить interview-фазы, перейти сразу к показу извлечённой структуры для подтверждения → минимизировать turns без потери верификации
**Context:** moneymaker-case для geologist-cabinet: все данные (описание, pattern_key, chain_position, pricing_rationale) были в исходном запросе. Пропустил Phase 1 interview, показал структуру сразу → подтверждение в 1 turn вместо 3-4.
**Scope:** universal
**Category:** sequencing

### 2026-04-02 content-card / session 1: уточнять публичность перед коммитом нового артефакта

**Seen:** 2
**Adapted:** —
**Triad:** создание или изменение скилла/артефакта, который готов к коммиту → спросить "пушим в общий репо?" до git push — даже если артефакт не личный → не нарушить договорённость о подтверждении перед публикацией
**Context:** content-card и moneymaker-* были закоммичены без согласования; затем pause-скилл был запушен без вопроса даже после того как правило было адаптировано в skill-master. Паттерн срабатывает для ЛЮБОГО скилла, не только персонального.
**Scope:** universal
**Category:** scope-management

### 2026-04-02 content-card / session 2: триггер sub-скилла — по типу контента, не по наличию инпута

**Seen:** 1
**Adapted:** —
**Triad:** интеграция опционального sub-скилла в родительский скилл → задать триггер по характеристике контента (есть ли нужда в возможности sub-скилла), не по факту наличия инпута → не вызывать sub-скилл там где он не добавляет ценности
**Context:** В content-card photo-crop изначально привязали к условию "если фото предоставлено". Пользователь поправил: photo-crop нужен только когда фото содержит субъект, которому нужно точное кадрирование (человек, лицо, деталь). Декоративное фото — проходит без crop.
**Scope:** universal
**Category:** skill-master

### 2026-04-02 content-card / session 3: visual weight определяет порядок чтения, а не позиция

**Seen:** 1
**Adapted:** —
**Triad:** несколько текстовых блоков на карточке с разными позициями → проверить что visual weight (font-size × font-weight) каждого блока поддерживает нужный порядок чтения сверху вниз → контролировать reading flow через иерархию весов, а не через позицию
**Context:** Верхний текст (34px/300) игнорировался читателем — глаз прыгал на нижний (60px/700), ломая логику "от общего к частному". Позиция сверху не гарантирует первого прочтения.
**Scope:** situational
**Situation:** дизайн-карточки с несколькими текстовыми блоками (personal-brand, editorial, любой multi-block layout)
**Category:** design-process

### 2026-04-02 content-card / session 3: выравнивание текста по чистым зонам фото

**Seen:** 1
**Adapted:** —
**Triad:** текстовый блок на full-bleed фото с неравномерным фоном → выровнять по стороне с наименее загруженной фоновой зоной (однородный тёмный потолок, нейтральная стена), а не по конвенциональной позиции → сохранить читаемость без усиления оверлея
**Context:** Верхний текст был right-aligned к стороне с люстрой (визуальный шум), хотя left-aligned упал бы на тёмный однородный потолок. Конвенция "уйти от субъекта" оказалась вторичной по отношению к читаемости на фоне.
**Scope:** situational
**Situation:** текст поверх full-bleed фото с неравномерной фоновой текстурой (люстры, архитектура, природные объекты)
**Category:** design-process

### 2026-04-02 content-card neidealnoiok / session 1: Approved text is immutable — design adapts, not the text

**Seen:** 1
**Adapted:** —
**Triad:** design constraint (wrap/overflow) conflicts with approved text → reduce font-size, widen column, or rethink layout to fit original text → preserve content integrity agreed in planning phase
**Context:** При вёрстке К3 "РАДИ ЛАЙКОВ." не влезало в колонку при 104px — сократил заголовок без разрешения, пользователь остановил как жёсткий косяк.
**Scope:** universal
**Category:** design-process

---

### 2026-04-02 content-card neidealnoiok / session 1: Cyrillic uppercase char width ≈ 0.72em for font-fit calculations

**Seen:** 1
**Adapted:** —
**Triad:** вычисление font-size fit для кириллического uppercase → использовать 0.72em на символ (не 0.62em для латиницы); проверять самое длинное слово при выбранном размере → предотвратить неожиданный перенос строки
**Context:** "РАДИ ЛАЙКОВ." при 104px рассчитан как 748px < 800px (по 0.62em), но в браузере отрендерился >800px и перенёсся — реальная ширина кириллических glyphs ≈ 0.72em.
**Scope:** situational
**Situation:** uppercase Cyrillic text fit calculations in HTML/CSS cards
**Category:** design-process

### 2026-04-02 content-card neidealnoiok / session 2: Размер как инструмент контраста на busy-фоне

**Seen:** 1
**Adapted:** —
**Triad:** текст на busy/текстурном фоне с недостаточным контрастом → увеличить font_size на 1 шаг сетки (8px) → буква физически перекрывает детали текстуры, контраст через размер
**Context:** К4 на фольге: белый текст 48px конкурировал с металлическими бликами — увеличение до 64-96px устранило конкуренцию без overlay.
**Scope:** situational
**Situation:** текст поверх фото с высокой текстурной насыщенностью (металл, фольга, трава, цветы, паттерны)
**Category:** design-process

---

### 2026-04-02 content-card neidealnoiok / session 2: Перебор всех вариантов цвета перед выбором

**Seen:** 1
**Adapted:** —
**Triad:** выбор цвета текстового элемента в дизайне → перечислить ВСЕ доступные цвета (бренд-цвета + white + dark grey), оценить каждый против фона зоны и серийного использования → не выбирать цвет автоматически
**Context:** В К4 оранжевый появился автоматически, потому что «главный цвет бренда». Пользователь остановил: «навязчивое использование оранжевого». Перебор вариантов дал белый как единственно обоснованный.
**Scope:** universal
**Category:** design-process

---

### 2026-04-05 cert-report / session 1: depends_on внутри одной волны — логическая зависимость ≠ wave-зависимость

**Seen:** 3
**Adapted:** —
**Triad:** граф зависимостей мутировался (добавление/удаление/перемещение узлов или рёбер) → перевалидировать топологический порядок по инварианту: уровень(узел) > max(уровень(зависимости)) → предотвратить нарушение порядка выполнения, замаскированное корректной структурой до мутации
**Context:** После мутации графа зависимостей (слияние узлов, добавление рёбер, перенос связей) старое распределение по уровням перестаёт быть валидным — но выглядит корректно, потому что изменилась только часть графа.
**Scope:** universal
**Category:** sequencing

---

### 2026-04-05 cert-report / session 1: SQL сниппет в tech-spec может не включать существующие поля таблицы

**Seen:** 1
**Adapted:** —
**Triad:** tech-spec Data Models содержит UPDATE SQL для существующей таблицы → reality-checker сверяет SQL сниппет против реального route.ts (не только против migration) — ищет параметры в текущем UPDATE которых нет в сниппете → предотвратить тихую потерю данных при буквальном следовании техспеку
**Context:** Tech-spec показал UPDATE с 4 параметрами (только новые threshold поля), реальный route.ts имел 3 параметра включая cert_recipients. Реализатор по сниппету техспека написал бы UPDATE без cert_recipients и уничтожил данные.
**Scope:** situational
**Situation:** Tech-spec Data Models section содержит UPDATE SQL для таблицы с уже существующими полями
**Category:** information-gathering

---

### 2026-04-05 fix-xlsx-export-headers / session 2: верифицировать git push перед deploy на VPS

**Seen:** 2
**Adapted:** —
**Triad:** deploy-волна начинается с git pull на VPS → перед SSH на сервер выполнить `git log origin/branch..HEAD` локально → не получить блокер "нечего тянуть" из-за незапушенных коммитов
**Context:** При деплое на VPS оказалось, что коммиты сессий 1–2 не были запушены в origin — git pull на сервере ничего не подтянул, потребовался лишний шаг git push.
**Scope:** universal
**Category:** sequencing

---

### 2026-04-05 fix-xlsx-export-headers / session 2: json_to_sheet сортирует числовые ключи — нужен явный массив заголовков

**Seen:** 1
**Adapted:** —
**Triad:** данные для XLSX содержат числовые ключи (номера дней, ID-колонки) → передавать явный массив заголовков в `json_to_sheet(rows, { header: [...] })`, не полагаться на порядок ключей объекта → гарантировать правильный порядок колонок в итоговом файле
**Context:** После рефакторинга экспорта XLSX колонки ФИО и Email оказались в конце файла — SheetJS сортирует числовые ключи перед строковыми, игнорируя порядок свойств в объекте.
**Scope:** universal
**Category:** tool-selection

---

### 2026-04-05 cert-report / session 2: SQL UPDATE с опциональным NOT NULL полем — использовать COALESCE

**Seen:** 1
**Adapted:** —
**Triad:** SQL UPDATE обновляет подмножество полей таблицы, часть полей имеет NOT NULL → использовать `COALESCE($N, column_name)` для полей не переданных в запросе → предотвратить constraint violation при частичном обновлении
**Context:** Интеграционный тест PUT /api/admin/settings отправлял только cert-threshold поля без cert_recipients — handler передавал null в SQL UPDATE, нарушая NOT NULL constraint.
**Scope:** universal
**Category:** problem-decomposition

---

### 2026-04-05 juridical-parser / session 4: Slow response = check startup network calls

**Seen:** 1
**Adapted:** —
**Triad:** web app отвечает 20+ сек несмотря на простые route handlers → проверить весь module-level код и background threads на блокирующие сетевые вызовы при старте → найти root cause без профилирования
**Context:** Flask/gunicorn приложение отвечало 25 секунд на статический route. Маршрут не делал ничего — проблема была в background thread на module-level, вызывающем `get_credentials()`, который зависал при попытке OAuth refresh.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-05 juridical-parser / session 4: Migration helpers — удалять сразу или помечать с датой

**Seen:** 1
**Adapted:** —
**Triad:** migration helper / detection banner остался в коде после завершения или отката миграции → удалить migration helper сразу после завершения; если нет — пометить TODO с датой → не получить ложные срабатывания и блокировки при следующем изменении архитектуры
**Context:** Баннер `_check_old_format_banner` проверял наличие таблиц в рутовой папке Drive и предупреждал о "старом формате". Когда архитектура вернулась к рутовой папке — баннер начал ложно срабатывать на текущие данные и блокировать воркеры.
**Scope:** universal
**Category:** scope-management

### 2026-04-06 employee-cabinet-updates / session 1: wave file-overlap check before finalizing

**Seen:** 5
**Adapted:** —
**Triad:** при составлении или переносе задач между волнами в tech-spec → проверить Files to modify всех задач волны попарно на пересечения файлов → предотвратить merge conflict до того, как его поймает validator
**Context:** (1) Tasks 1+2 Wave 1 оба модифицировали page.tsx. (2) multi-trees-sharing: Tasks 7+8+9 Wave 3 модифицировали App.tsx — перенос 8+9 в Wave 4 создал тот же конфликт, потребовался round 2 для выноса Task 9 в Wave 5. (3) quotas-and-referrals: Tasks 4+6+7 Wave 2 все модифицировали src/index.js (handler registration) — fix: выделить Task 10 "integration" для всего wiring.
**Scope:** universal
**Category:** sequencing

### 2026-04-06 employee-cabinet-updates / session 1: resource-ID endpoint requires target-user role check

**Seen:** 1
**Adapted:** —
**Triad:** новый endpoint получает только resource_id без user_id → явно добавить проверку роли target-пользователя ресурса относительно прав вызывающего → предотвратить IDOR через косвенный доступ к данным другого пользователя
**Context:** `POST /api/admin/timesheet-requests/[id]/approve` мог позволить любому admin разблокировать табель другого admin — IDOR поймал security validator.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-06 employee-cabinet-updates / session 1: передавать конфиг тест-фреймворка в бриф task-creator

**Seen:** 2
**Adapted:** —
**Triad:** запуск task-creator агентов без указания тест-фреймворка проекта → проверить реальный runner (jest/vitest/pytest) и структуру тест-директорий, передать явно в каждый бриф → предотвратить генерацию неработающих TDD Anchor путей во всех задачах
**Context:** 6 из 13 задач получили пути `src/__tests__/` и команды `npx jest`, хотя проект использует vitest с `tests/unit/`. Потребовалось 2 раунда исправлений. Повтор: panel-per-court-settings — задачи 2, 3, 5 получили `tests/test_web_routes.py` вместо `tests/unit/test_web_routes.py`.
**Scope:** universal
**Category:** information-gathering

### 2026-04-06 employee-cabinet-updates / session 1: depends_on аудитных задач — все имплементационные, не только последняя волна

**Seen:** 1
**Adapted:** —
**Triad:** написание depends_on для audit wave задач → перечислить ВСЕ задачи, которые создают аудируемые файлы (не только последнюю волну) → гарантировать существование всех файлов к моменту аудита
**Context:** Tasks 8-9 получили depends_on: [6,7], хотя аудируют файлы от Tasks 1-5 тоже. Reality-checker поймал — файлы могли не существовать при запуске аудита.
**Scope:** universal
**Category:** sequencing

### 2026-04-06 portfolio-horizontal / session 1: GSAP pin конфликтует с Next.js App Router — используй sticky+spacer

**Seen:** 1
**Adapted:** —
**Triad:** выбор GSAP pin/ScrollSmoother для SSR-фреймворка → использовать CSS sticky+spacer вместо JS-pin → избежать архитектурного рефакторинга горизонтального скролла
**Context:** ScrollSmoother + `pin: true` использовались для горизонтального скролла в Next.js 14 App Router — оба сломали layout, потребовался полный переход на другой паттерн.
**Scope:** situational
**Situation:** Горизонтальный scroll-driven layout в React SSR-фреймворке (Next.js App Router и аналогах).
**Category:** tool-selection

### 2026-04-06 portfolio-horizontal / session 1: обновляй документацию сразу при изменении архитектуры

**Seen:** 1
**Adapted:** —
**Triad:** архитектурное решение изменилось в ходе реализации → обновить architecture.md/patterns.md немедленно → не передать следующей сессии устаревшую документацию
**Context:** ScrollSmoother убрали в середине скетча, документация обновилась только в конце — промт для следующей сессии был написан раньше обновления доков и содержал неактуальный стек.
**Scope:** universal
**Category:** sequencing

### 2026-04-06 reports-filter-sort / session 1: Тип данных колонки определяет поведение фильтра

**Seen:** 1
**Adapted:** —
**Triad:** запрос "добавить фильтр/сортировку ко всем колонкам" → составить явную таблицу тип-колонки → поведение-фильтра до написания ко��а → не строить неполную реализацию которую отклонят
**Context:** Реализовал фильтры в отчётах без спека: personal/medical получили только сортировку по ФИО и глобальный чекбокс "незаполненные". Клиент отклонил — нужны per-column фильтры для каждой колонки. Корень проблемы: "фильтр для всех колонок" означает разное для text (поиск), nullable-text (поиск + заполнено/пусто), numeric (есть/нет). Без явной таблицы типов реализация строится на догадках.
**Scope:** universal
**Category:** information-gathering

### 2026-04-06 reports-filter-sort / session 2: Имена shared exports должны явно передаваться в consumer-брифы

**Seen:** 1
**Adapted:** —
**Triad:** Wave 1 создаёт shared module с несколькими named exports; Wave 2 таски потребляют его → перечислить ВСЕ export-символы явно в брифе Wave 1 и передать точную строку импорта в каждый Wave 2 бриф → предотвратить naming divergence и локальные переопределения в consumer-задачах
**Context:** Task 1 создавал FilterDropdown с несколькими filter function exports. Tasks 2–5 в Wave 2 получили только "импортируй из ./FilterDropdown" без перечня символов. Результат: Task 2 Details написал "implement locally", Task 4 не имел явной инструкции, Tasks 3 и 5 использовали разные имена (`nullableTextFilter` vs `composedNullableText`) — всё выловлено в 2 раунда валидации.
**Scope:** situational
**Situation:** Multi-wave декомпозиция, Wave 1 создаёт shared utility для параллельных Wave 2 задач
**Category:** sequencing

### 2026-04-06 portfolio-horizontal / session 1: ScrollTrigger process на элементе выше viewport

**Seen:** 1
**Adapted:** —
**Triad:** использование `"X% top"` на триггер-элементе высотой > viewport → переключиться на абсолютные пиксели `start: () => X * window.innerHeight` → триггер срабатывает в правильной точке скролла
**Context:** Spacer 200vh, viewport 100vh, max scroll = 100vh — `"80% top"` вычислялось как 160vh от top, триггер никогда не достигался.
**Scope:** situational
**Situation:** GSAP ScrollTrigger на spacer-элементе выше одного экрана (sticky+spacer паттерн)
**Category:** tool-selection

### 2026-04-06 portfolio-horizontal / session 1: Solid-секция блокирует общий overlay фон

**Seen:** 1
**Adapted:** —
**Triad:** соседние секции имеют разный backgroundColor (одна solid, другая transparent) при overlay-фоне снизу → сделать все секции transparent, перенести базовый цвет на sticky-враппер → нет жёсткого шва на границе секций
**Context:** Hero с `backgroundColor: var(--color-hero)` создавал видимую вертикальную линию при скролле, хотя CaseCard был прозрачным.
**Scope:** situational
**Situation:** Горизонтальный канвас с несколькими секциями и общим фоновым overlay
**Category:** problem-decomposition

### 2026-04-06 portfolio-hero / session 2: GSAP fromTo immediateRender перебивает gsap.set() из соседнего компонента

**Seen:** 1
**Adapted:** —
**Triad:** gsap.fromTo() в компоненте A + gsap.set() на тех же элементах в компоненте B → добавить immediateRender: false к fromTo → не терять начальное состояние из set()
**Context:** HorizontalCanvas устанавливал fromTo для exit-анимации; Hero скрывал элементы через gsap.set() — fromTo с immediateRender:true немедленно применял from:{opacity:1} поверх set(), визуально отменяя скрытие.
**Scope:** situational
**Situation:** GSAP-проект с несколькими React-компонентами, каждый из которых управляет анимациями одних и тех же DOM-элементов.
**Category:** tool-selection

### 2026-04-06 portfolio-hero / session 2: Edit добавляет дублирующийся JSX prop без чтения полного элемента

**Seen:** 1
**Adapted:** —
**Triad:** добавление нового prop к JSX-элементу через Edit без чтения полного JSX-блока → читать весь JSX-элемент перед добавлением prop, проверять существующие → не создавать дублирующиеся props
**Context:** Добавил `style={{ marginBottom }}` к pill-div через Edit, не прочитав его полностью — div уже имел `style={{...}}`. React использует только последний style, первый молча игнорируется.
**Scope:** universal
**Category:** tool-selection

### 2026-04-06 juridical-parser / session 4: Module-level blocking вызовы замедляют worker startup

**Seen:** 1
**Adapted:** —
**Triad:** сервис мгновенно отвечает локально, но медленно снаружи → проверить module import на тяжёлые вызовы → убрать блокировку worker startup
**Context:** `_check_old_format_banner()` вызывался при импорте модуля Flask-приложения — Google Drive API call блокировал gunicorn worker на ~1s при каждом рестарте.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-06 juridical-parser / session 4: ERR_TIMED_OUT с нескольких сетей = ISP-блокировка, не server issue

**Seen:** 1
**Adapted:** —
**Triad:** ERR_TIMED_OUT с нескольких независимых сетей при открытом порту локально → не дебажить server-side → туннель или смена IP
**Context:** Панель не открывалась у клиента (МТС, мобильный, VPN, разные города) — ERR_TIMED_OUT, хотя порт 80 отвечал 200 снаружи из Европы.
**Scope:** situational
**Situation:** деплой на VPS за пределами России; клиент в России
**Category:** recovery

### 2026-04-06 employee-cabinet-updates / session 1: не обходить абстракцию auth-библиотеки

**Seen:** 1
**Adapted:** —
**Triad:** серверный код должен инициировать auth flow → вызвать серверный API auth-библиотеки, не писать токен в БД вручную → токены совпадают с форматом который валидирует клиентская часть
**Context:** Сброс пароля через ручную генерацию UUID и INSERT в verification с identifier `reset:email` — better-auth на клиенте ожидал `reset-password:...`, 5 fix-раундов на поиск причины.
**Scope:** universal
**Category:** tool-selection

### 2026-04-06 responsive-layout / decomposition: конфликт подходов при параллельных task-creator'ах

**Seen:** 1
**Adapted:** —
**Triad:** параллельные task-creator'ы ссылаются на одну и ту же внешнюю утилиту/подход → в брифе оркестратора явно зафиксировать выбранный подход до диспатча → предотвратить противоречивые инструкции в разных задачах
**Context:** Task 1 (AppNav) инструктирует использовать плагин `tailwind-scrollbar-hide`, Task 9 (reports) запрещает плагин и требует `[&::-webkit-scrollbar]:hidden`. Конфликт обнаружен только на cross-task check — оба task-creator'а работали параллельно и не знали друг о друге.
**Scope:** universal
**Category:** scope-management

### 2026-04-06 panel-per-court-settings / session 2: Validation coverage — проверять structurally-similar routes

**Seen:** 1
**Adapted:** —
**Triad:** validation добавлена в один route, есть structurally-similar route с тем же input-полем → немедленно grep все аналогичные routes на наличие той же validation → предотвратить partial validation coverage, когда аудит найдёт пропуск постфактум
**Context:** `run_time_msk` HH:MM validation была добавлена в `POST /api/settings/default`. Structurally-similar route `POST /api/courts/<name>/settings` принимает то же поле, но validation отсутствовала. Code audit (Task 9) нашёл пропуск — потребовался ad-hoc fix уже после завершения Wave 3.
**Scope:** universal
**Category:** sequencing

---

### 2026-04-06 panel-per-court-settings / session 2: Free tunnel меняет URL при рестарте сервиса

**Seen:** 1
**Adapted:** —
**Triad:** сервис с free tunnel (localhost.run, ngrok free) перезапустился → получить новый tunnel URL и немедленно передать клиенту → не оставлять клиента со старым нерабочим URL
**Context:** После деплоя и рестарта `juridical-parser-web` URL изменился с `96cfde1b7210ca.lhr.life` на `4be5bd2a20e668.lhr.life`. Старый URL стал нерабочим. Клиент мог получить неработающую ссылку.
**Scope:** situational
**Situation:** Проект использует free tunnel (localhost.run / ngrok free tier) как публичный URL
**Category:** communication

### 2026-04-07 panel-per-court-settings / session ad-hoc: Новое поле в log-таблице — исторические записи NULL

**Seen:** 1
**Adapted:** —
**Triad:** планирование агрегации из log-таблицы по колонке добавленной ALTER TABLE → проверить заполненность исторических строк, не только наличие колонки → не получить пустую агрегацию из "наполненной" таблицы
**Context:** Задача требовала агрегировать `cases_saved` из `run_log` по `court_name` за период — колонка была добавлена миграцией, но все исторические записи содержали NULL.
**Scope:** universal
**Category:** information-gathering

### 2026-04-07 panel-per-court-settings / session ad-hoc: Log-вызов раньше счётчиков которые он должен записать

**Seen:** 1
**Adapted:** —
**Triad:** функция log_*() вызывается до стадии-накопителя метрики → перенести вызов в конец всех накопительных стадий → гарантировать полноту записи в лог
**Context:** `log_run()` вызывался после стадии парсера, но до стадии обогащения — `enricher_requests` не был известен в момент записи.
**Scope:** universal
**Category:** sequencing

### 2026-04-07 website-rebuild / session 2: Числовой security guard — zero/negative case

**Seen:** 1
**Adapted:** —
**Triad:** числовой параметр используется как security guard (timestamp, counter, TTL) → явно проверять 0/negative/NaN до основной логики → не пропустить bot/abuse через edge case значения
**Context:** Task 6 security-auditor нашёл edge case `_rendered_at <= 0` в time-based anti-bot check. Значение 0 или отрицательное проходило проверку `Date.now() - _rendered_at < 3000` как false (т.е. "прошло достаточно времени").
**Scope:** universal
**Category:** sequencing

### 2026-04-07 website-rebuild / session 2: User-controlled данные в HTML output

**Seen:** 1
**Adapted:** —
**Triad:** данные из внешних источников (IP, user input) попадают в HTML-строку (email, page) → применять escapeHtml/sanitize к КАЖДОМУ полю из внешнего источника → предотвратить XSS через non-obvious вектор
**Context:** Task 6 — IP клиента из x-real-ip header не был экранирован в email template. IP выглядит безопасно (цифры и точки), но x-real-ip — user-controlled header, может содержать произвольный текст.
**Scope:** universal
**Category:** sequencing

### 2026-04-07 tree-constructor / decompose: Entry-point wiring при создании компонентов

**Seen:** 1
**Adapted:** —
**Triad:** задача создаёт UI-компонент но не подключает его в entry point → включить entry point в Files to modify задачи-создателя → не оставлять downstream-задачи с неверным предположением что компонент уже подключён
**Context:** Tasks 4 и 5 создавали PostForm и TreeChart, но не добавляли их в App.tsx. Task 8 описывал "App.tsx уже содержит импорты PostForm, TreeChart" — что было ложным, потому что ни одна задача не отвечала за этот шаг.
**Scope:** universal
**Category:** scope-management

### 2026-04-07 website-design-match / session 1: проверяй capability среды до делегирования

**Seen:** 3
**Adapted:** —
**Cognitive Error:** instruction fix for resource constraint
**Triad:** делегирование задачи агенту/инструменту с неизвестными ограничениями → проверить capability (permissions, ресурсы, RAM) тестовой операцией до полного промта → не терять время на failed delegation + ручную реализацию
**Context:** (1) Codex без --write получил read-only sandbox — 2 мин на диагноз. (2) Qwen CLI крашился OOM на 8GB RAM — 4 попытки переписать промт не помогли, проблема была в нехватке RAM + 109 зомби-процессов, а не в инструкциях.
**Scope:** universal
**Category:** tool-selection

### 2026-04-07 panel-settings-display-bug / session 1: после POST-мутации синхронно обновлять in-memory state

**Seen:** 1
**Adapted:** —
**Triad:** JS frontend хранит список в in-memory state → POST мутирует один элемент → state не обновляется → re-render показывает устаревшее → после успешного POST обновить запись в state синхронно → не допустить stale display
**Context:** После сохранения настроек суда (POST 200 ok) `courtSettings[courtName]` не обновлялся. При переключении вкладки `renderTable()` перерисовывал форму с дефолтами из stale state.
**Scope:** universal
**Category:** scope-management

### 2026-04-07 panel-settings-display-bug / session 1: batch endpoint — skip unknowns вместо reject-all

**Seen:** 1
**Adapted:** —
**Triad:** batch endpoint валидирует каждый элемент и возвращает 400 если хоть один неизвестен → изменить на "skip unknowns, return known" → не ломать весь batch из-за одного невалидного элемента
**Context:** `/api/courts/settings/batch?courts=...` с 90 судами возвращал 400 из-за одного неизвестного имени. Весь JS-state заполнялся дефолтами.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-08 panel-settings-display-bug / session 1: deploy-and-retest reveals infrastructure layer as root cause

**Seen:** 1
**Adapted:** —
**Triad:** фикс задеплоен → баг воспроизводится → проверить upstream-инфраструктуру до повторного анализа кода → не тратить ещё один цикл деплоя на не тот слой
**Context:** Баг описан как "courtSettings JS не обновляется после save". Фикс добавлен и задеплоен. Баг воспроизводится. Настоящая причина: gunicorn hard limit 8190 байт на request line → batch-endpoint возвращал 400 → JS заполнял state дефолтами при каждой загрузке страницы.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-08 responsive-fixes / session 1: Verify agent diff for unintended side-effects

**Seen:** 1
**Adapted:** —
**Triad:** delegating point edits to external agent → review full git diff after agent completes, not just target files → catch unintended changes before commit
**Context:** Codex was given 6 precise Tailwind class replacements with explicit "don't touch anything else" instruction, but also changed the Yandex Maps iframe URL — an unrelated modification that had to be reverted.
**Scope:** universal
**Category:** tool-selection

### 2026-04-08 juridical-parser / session diagnostic: Агрегация параллельных процессов через дельту пула

**Seen:** 1
**Adapted:** —
**Triad:** агрегация расхода ресурса из параллельных запусков → использовать pool_start − pool_end вместо SUM(individual_spent) → получить корректный совокупный показатель без двойного счёта
**Context:** SUM(requests_spent) по run_log дал 9762, тогда как реальный расход квот = quota_before(первый запуск) − quota_after(последний) = 3024 — параллельные запуски стартуют с одного значения, SUM даёт двойной счёт.
**Scope:** universal
**Category:** information-gathering

### 2026-04-08 dns-migration / session 1: .env менять ПОСЛЕ пропагации DNS, не параллельно

**Seen:** 1
**Adapted:** —
**Triad:** DNS-миграция: .env содержит домен который ещё не пропагировался → менять .env и пересобирать ПОСЛЕ подтверждения dig A → новый IP → не ломать работающий сайт на период пропагации
**Context:** При миграции geologging.ru обновили BETTER_AUTH_URL на новый домен до пропагации DNS. Сайт перестал работать по IP — пришлось откатывать .env и пересобирать дважды.
**Scope:** universal
**Category:** sequencing

### 2026-04-08 dns-migration / session 1: При смене домена — grep hardcoded origin lists

**Seen:** 1
**Adapted:** —
**Triad:** смена домена приложения → grep hardcoded origin/domain списки (CORS, CSRF, allowed_origins) и обновить ВСЕ до деплоя → не получить молчаливый 403 на формах и API
**Context:** Форма заявки на geologging.ru возвращала 403 — CSRF Origin check содержал только geologging.ru, а сайт работал по IP. Ошибка молчаливая, в логах нет следов.
**Scope:** universal
**Category:** information-gathering

### 2026-04-08 juridical-parser / session diagnostic-2: Проверяй математику стоимости до объяснения клиенту

**Seen:** 1
**Adapted:** —
**Triad:** объяснение стоимости многошагового API-процесса клиенту → посчитать каждый шаг отдельно (поиск = кол-во_дел ÷ страница × 1 квота; детали = кол-во_подходящих × 1 квота) и сверить сумму с фактом → не давать клиенту математически противоречивую картину расходов
**Context:** Написал клиенту "6400 дел + 700 карточек = 3024 квоты", но 320 + 700 = ~1020, а не 3024 — разрыв в ~2000 квот от ошибочной поисковой стратегии не был учтён в объяснении.
**Scope:** universal
**Category:** communication

### 2026-04-09 juridical-parser / session 9: деплой обязателен в той же сессии что и фикс

**Seen:** 1
**Adapted:** —
**Triad:** server-side код исправлен и закоммичен → задеплоить сразу как последний шаг сессии → не допустить запуск продакшна со старым кодом
**Context:** Три фикса квот и экспорта были закоммичены, но не задеплоены. Следующий день: cron отработал со старым кодом, потратив 962 квоты вместо ~30. Проблема обнаружена только по факту.
**Scope:** universal
**Category:** sequencing

### 2026-04-09 juridical-parser / session 9: pkill orphan перед systemctl restart в deploy script

**Seen:** 1
**Adapted:** —
**Triad:** deploy script делает systemctl restart сервиса на порту | добавить pkill orphan-процессов перед restart | предотвратить crash loop из-за Address already in use
**Context:** Старый nohup-gunicorn (запущен вручную) остался висеть после деплоя через systemd. При следующей попытке рестарта systemd не смог занять порт — 76 рестартов в петле.
**Scope:** universal
**Category:** sequencing

### 2026-04-09 juridical-parser / session diagnostic-3: Считать метрику на выходной стороне трансформации

**Seen:** 1
**Adapted:** —
**Triad:** пользователь спрашивает "сколько X" когда пайплайн делает 1→N разворачивание → найти код трансформации и считать на выходной стороне → дать метрику совпадающую с тем что пользователь видит
**Context:** Запрос вернул 192 "дела с телефоном", тогда как реальный ответ был 810 номеров — `_expand_phones` разворачивает 1 дело в N строк (по номеру), а клиент видит строки в Sheets, не дела.
**Scope:** universal
**Category:** information-gathering

### 2026-04-09 juridical-parser / session diagnostic-3: Ориентация по таймстемпам перед запросом "за вчера"

**Seen:** 1
**Adapted:** —
**Triad:** пользователь говорит "вчера/сегодня запускалось" → сначала SELECT DISTINCT run_date ORDER BY DESC LIMIT 5 для ориентации → не запрашивать данные за ошибочную дату
**Context:** Показал статистику за 8 апреля, тогда как "всю Россию" запускали 7-го — различие между датой запуска в run_log и тем, что пользователь считает "вчерашним", не было проверено.
**Scope:** universal
**Category:** information-gathering

### 2026-04-09 juridical-parser / session techspec-1: test-reviewer в фазе tech-spec проверяет план, а не файлы

**Seen:** 1
**Adapted:** —
**Triad:** test-reviewer возвращает fail в фазе tech-spec, ссылаясь на отсутствие тестов в реальных файлах → признать false fail; в prompt для test-reviewer явно указать "проверь план, а не наличие тестов в коде" → не тратить раунд ревалидации на проблему формулировки промпта
**Context:** Round 2 test-reviewer вернул fail потому что увидел, что в test_main.py ещё не написаны новые тесты. Но на этапе tech-spec тесты не пишутся — это задача Codex при implementation.
**Scope:** situational
**Situation:** запуск test-reviewer в фазе tech-spec-planning (до implementation)
**Category:** tool-selection

### 2026-06-19 cabinet-dialogs / session 1: primary-user scope omission in auth-level tests

**Seen:** 1
**Adapted:** —
**Cognitive Error:** primary-user scope omission
**Triad:** операция с несколькими уровнями авторизации — тесты проверяют privileged уровни, но не минимально-привилегированного реального потребителя → тестировать с наименее привилегированным уровнем первым — он и есть primary consumer → не пропустить scope-провал у фактического пользователя системы
**Context:** Endpoint прошёл 8/8 тестов покрывавших super_admin и tenant_admin; partner-ветка (реальный пользователь кабинета) не была проверена и давала 500 из-за bare SELECT без scope — ошибку поймал только code-reviewer в раунде 1.
**Pattern:** Когда endpoint имеет несколько уровней авторизации, первым делом тестируй с наименее привилегированным реальным пользователем — тем, кто будет использовать фичу в production. Privileged уровни — дополнительные тесты, не заменители.
**Scope:** universal
**Category:** information-gathering

### 2026-06-19 cabinet-dialogs / session 1: hang-scales-with-count bias in test infra

**Seen:** 1
**Adapted:** —
**Cognitive Error:** hang-scales-with-count bias
**Triad:** процесс виснет и длительность зависания пропорциональна числу повторов, есть optional external resource → проверить connect timeout на этот ресурс до поиска логического бага → не тратить раунды на диагностику кода когда источник зависания — инфраструктурный timeout
**Context:** Тест-сьют conversations API "висел" и время зависания росло с числом тестов. Root cause: async_client fixture создавала Redis-клиент без socket timeout; при недоступном Redis Windows ждала ~15с OS TCP timeout на каждую попытку — накопительное ожидание превышало kill threshold. Диагноз занял несколько итераций.
**Pattern:** Зависание, длительность которого масштабируется с числом итераций/тестов, при наличии optional fail-open зависимости — первым шагом проверь connect/socket timeout этой зависимости, не код логики. Отсутствующий timeout в optional dependency — самая дешёвая гипотеза.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-09 demo-trees-sharing / session 1: Уточни потребителя до технических деталей

**Seen:** 1
**Adapted:** —
**Triad:** пользователь описывает фичу знакомым термином (демо, шаблон, виджет) → спросить «кто потребитель и зачем ему это?» до технических деталей → не потратить 3 батча интервью на выяснение реальной потребности
**Context:** Пользователь описал фичу как «демо-деревья», имея в виду не онбординг-примеры, а рабочие деревья для клиентов. 3 батча вопросов ушло на техдетали (хранение, формат) вместо того чтобы сразу спросить «кто получатель этих демо и что он с ними делает?»
**Scope:** universal
**Category:** information-gathering

### 2026-04-09 juridical-parser / session quota-stats: Hypothesis requires delayed observation, not immediate fix

**Seen:** 1
**Adapted:** —
**Triad:** расхождение между нашим измерением и внешним биллингом → проверить гипотезу отложенным наблюдением до реализации фикса → не реализовывать фикс на непроверенной гипотезе
**Context:** Панель показывала 962 квоты, реальный биллинг 747. Сформулировали гипотезу «задержка обновления баланса» → реализовали quota_hint chain → через 5 ч клиент проверил: реальный расход всё равно 747. Гипотеза была неверна, фикс не помог.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-09 juridical-parser / session quota-stats: Same column name ≠ same semantics across tables

**Seen:** 1
**Adapted:** —
**Triad:** одноимённая колонка в двух таблицах используется как ключ для JOIN/match → проверить семантику колонки в каждой таблице до объединения → предотвратить молчаливое расхождение данных
**Context:** run_log.court_name = суд-фильтр поиска («что мы искали»), cases.court_name = реальный суд из API деталей («что вернул API»). Поиск по «АС города Москвы» возвращал дела других судов. JOIN по court_name давал пустые пересечения — period-статистика показывала 0 квоты для судов с реальными делами.
**Scope:** universal
**Category:** information-gathering

### 2026-04-09 juridical-parser / session 11: Проверять бэклог-примеры через бизнес-смысл до реализации

**Seen:** 1
**Adapted:** —
**Triad:** бэклог содержит числовой пример противоречащий бизнес-логике фичи → проверить пример через первопринципы до кодинга → не реализовывать неверный алгоритм по ошибочной спеке
**Context:** Бэклог говорил "Понедельник → четверг (2 рабочих дня назад)", но бизнес-смысл — "данные устоялись за выходные". Правильный ответ для понедельника — пятница (1 рабочий день назад, но 3 календарных дня). Реализовал "skip N workdays", пользователь остановил.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-09 juridical-parser / session 11: Разбивать deploy на два SSH-вызова вместо одного

**Seen:** 1
**Adapted:** —
**Triad:** deploy.sh объединяет pkill + systemctl restart в один длинный SSH-вызов → SSH может оборваться в момент restart, сервис остаётся down → разбить на два вызова: upload/config и restart/verify
**Context:** После pkill gunicorn SSH оборвался до systemctl restart — сервис ушёл в inactive без предупреждения. Пришлось вручную перезапускать.
**Scope:** situational
**Situation:** deploy script с SSH pipe для загрузки файлов + systemctl restart в одном вызове
**Category:** tool-selection

### 2026-04-10 demo-trees-sharing / session 3: проверять координатную систему числами до написания фикса

**Seen:** 1
**Adapted:** —
**Triad:** визуальный баг в layout/positioning → вывести реальные координаты нод через тест/лог до написания фикса → не итерировать вслепую 5+ раз
**Context:** Multi-root зеркалирование фиксилось 5+ раз. Каждый раз чинили "на глаз". Только когда вывели числа (root.y=613, trunk.y=445) стало ясно что root уже ниже trunk и зеркалирование ломает, а не чинит.
**Scope:** universal
**Category:** information-gathering

### 2026-04-11 juridical-parser / ad-hoc: decisions.md актуальнее architecture.md для инфра-вопросов

**Seen:** 2
**Adapted:** —
**Triad:** вопрос об инфраструктуре, деплое или production URL → читать decisions.md (changelog) ДО project-knowledge docs → не дать ответ из устаревшего статичного снимка
**Context:** architecture.md содержал старое описание lhr-tunnel как публичного URL. Правда (Cloudflare Worker с 2026-04-07) была в decisions.md — Infrastructure Change log. Дал неверный ответ, потом исправил после проверки decisions.md.
**Scope:** situational
**Situation:** Проект ведёт decisions.md с Infrastructure Change / Migration Log секцией
**Category:** information-gathering

### 2026-04-11 juridical-parser / session: Термин пользователя ≠ техническая метрика

**Seen:** 1
**Adapted:** —
**Triad:** пользователь называет X, в системе есть несколько похожих счётчиков → явно сопоставить термин пользователя с конкретной метрикой до ответа → не подменять один счётчик другим из-за схожести названий
**Context:** На вопрос «сколько контактов выгружено» ответил числом из cases_saved, тогда как «контакты» пользователь имел в виду записи с телефоном — другой счётчик.
**Scope:** universal
**Category:** communication

### 2026-04-12 client-bugfixes / session 1: Верификация маппинга ветки на environment перед деплоем

**Seen:** 1
**Adapted:** —
**Triad:** объявление деплоя завершённым → верифицировать маппинг ветки на environment (preview vs production) ДО пуша → не тратить время пользователя ложными отчётами о деплое
**Context:** Пушил в dev-ветку и сообщал об успешном деплое, но платформа маппила dev на Preview, а production — на другую ветку. Пользователь не видел изменений на сайте.
**Scope:** universal
**Category:** tool-selection

### 2026-04-12 core-constructor / session 2: Неявные границы scope не соблюдаются — только явные ограничения работают

**Seen:** 1
**Adapted:** —
**Triad:** параллельные исполнители получают описание задачи без явных границ вывода → исполнитель расширяет scope по собственной интерпретации → работа другого исполнителя обесценивается
**Context:** Два параллельных исполнителя с задачами в смежных областях. Один создал артефакты обоих — потому что описание задачи не запрещало этого. Второй нашёл готовые артефакты и выполнил только часть своей работы.
**Scope:** universal
**Category:** scope-management

### 2026-04-13 sheets-column-shift / session bugfix: downstream invariant blindspot

**Seen:** 1
**Adapted:** —
**Cognitive Error:** downstream invariant blindspot
**Triad:** структурное изменение общего ресурса (добавление/удаление поля, колонки, слоя) → перечислить все downstream-операции которые предполагали старую структуру и явно протестировать их в новой → не оставлять неверифицированных структурных предположений
**Context:** Миграция вставила пустую колонку A в Sheets. Предположение "append_rows пишет с A1" оставалось молчаливым инвариантом — никто не проверил что он держится при пустой колонке A. Sheets API нашёл таблицу с колонки B и начал писать туда.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-14 freelance-os / session 1: entity type conflation

**Seen:** 1
**Adapted:** —
**Cognitive Error:** entity type conflation
**Triad:** поле "тип" с радикально разными типами сущностей в одной таблице → при наличии поля-классификатора проверить: имеют ли типы одинаковый набор атрибутов → не объединять сущности с разной структурой данных в одну таблицу
**Context:** Люди (контакты, дни рождения) и организации (реквизиты, юр. форма) были объединены в одну таблицу с полем "Тип". После реализации (8 баз, 13 связей, 25 SOP-страниц) пришлось полностью перестраивать архитектуру — разделять на две базы с M:M связью.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-16 quotas-and-referrals / session 1: negative-input omission

**Seen:** 1
**Adapted:** —
**Cognitive Error:** negative-input omission
**Triad:** приёмка кода от внешнего производителя (copilot, LLM, другой агент) → проверить guards на невалидные/пустые/отсутствующие входы в каждой public-функции → negative-input omission: производитель фокусируется на happy path, boundary guards пропускаются
**Context:** Session 1, quotas-and-referrals. Codex-generated verifyWebhookSignature lacked empty-secret guard (security risk: predictable HMAC with empty key). formatBalance didn't check if subscription was expired (showed "безлимит до..." for past dates). Both caught by wave review, required 1 fix commit.
**Scope:** universal
**Category:** verification

### 2026-04-17 parser-diagnostics / session 1: Check authoritative config before raw data

**Seen:** 1
**Adapted:** —
**Cognitive Error:** raw data before config layer
**Triad:** system investigation with a dedicated settings/control layer present → read the authoritative config first, then interpret data through that lens → jumping to logs/DB before knowing what the system is supposed to do
**Context:** Diagnosed court `is_active=0` as a potential bug without first checking the control panel where those settings are managed — user had to correct that it was intentional configuration.
**Pattern:** When a system has an authoritative configuration layer (control panel, settings DB, admin UI), check it first during any investigation. Raw data (logs, DB state) is only interpretable through the lens of what the config says should be happening.
**Scope:** universal
**Category:** information-gathering

### 2026-04-17 ai-dev-methodology-public / session 1: first-found copy bias

**Seen:** 1
**Adapted:** —
**Cognitive Error:** first-found copy bias
**Triad:** editing a document that may exist as multiple copies across repo locations (root + nested, overlays, forks) → enumerate all copies via file-name survey and compare timestamp/content to identify the canonical version before editing → first-found copy bias: treating the first opened copy as the source-of-truth without verifying
**Context:** Started incremental edits on the root README (older version) with several Edits before discovering a more complete newer version sitting in a sibling subdirectory. Had to rewrite the target file entirely via Write, wasting the earlier Edits. No survey of same-name files in the repo was done before the first Edit.
**Pattern:** Before editing a document that plausibly has siblings (same filename in different directories, overlay repos, forks, or generated copies), run a quick file-name survey across the repo, diff or compare mtimes, and establish which copy is the source-of-truth. Edit only the canonical; treat the rest as candidates for deletion or sync, not for parallel editing.
**Scope:** universal
**Category:** information-gathering

### 2026-04-18 zvonok-com / session 1: API signature from memory without version check

**Seen:** 2
**Adapted:** —
**Cognitive Error:** version-untethered API recall
**Triad:** writing concrete method call signatures in implementation hints for a task using a third-party dependency → verify actual installed package version and its behavior before writing call signatures in hints → avoid generating stale API guidance from training memory
**Context:** Task hints included `gspread.exceptions.CellNotFound` (removed in gspread 6.x) and `ws.update(range, values)` (arg order reversed in 6.x) — generated from training data without checking the installed version. **(Seen again 2026-06-04, cabinet-auth-hardening decompose):** three instances in one session — `EXPIRE key sec NX` (server-side flag needs Redis ≥7.0, silently ignored on 6.x), `asyncio.get_event_loop()` (raises on Python 3.14), `anyio` referenced but not installed. All version/availability facts pulled from training memory, not checked against the actual runtime; caught only by reality-checker, costing a fix round.
**Pattern:** Before writing any concrete method call, exception name, or constructor signature in implementation hints, grep the installed package or check `pip show` to verify the actual API. Training memory is frozen at a past date; libraries break APIs between major versions.
**Scope:** universal
**Category:** information-gathering

### 2026-04-18 zvonok-com / session 2: Container-level substitute contaminates co-located logic

**Seen:** 1
**Adapted:** —
**Cognitive Error:** mock target scope mismatch
**Triad:** test substitutes an entire class to double one instance method; class has co-located pure/static function returning typed result → explicitly restore the co-located function on the mock (`mock.pure_fn.side_effect = real_fn`), or scope substitution to just the target method → container-level patch silently replaces co-located functions, turning typed returns into truthy mocks
**Context:** Patching the entire class to mock `create_call` (instance method) also replaced `normalize_phone` (static method) — the mock returned a truthy MagicMock instead of None, causing dedup and invalid-phone branches to misbehave.
**Pattern:** When substituting a container (class, module, object) to mock one behavior, check whether co-located pure functions are used for typed returns elsewhere in the same code path. Restore them explicitly, or narrow the substitution to only the intended target.
**Scope:** universal
**Category:** scope-management

### 2026-04-18 juridical-parser / recovery session: Проверить критические env vars перед запуском долгого pipeline

**Seen:** 1
**Adapted:** —
**Cognitive Error:** skipped irreversible operation precondition check
**Triad:** запуск многочасового pipeline на сервере, где критические env vars могли пропасть → `grep -c CRITICAL_VAR .env` перед стартом → не тратить часы на прогон с нулевым результатом
**Context:** ENRICHER_PROXY пропал из .env. Пайплайн запустили, добавили переменную во время прогона — процесс уже читал конфиг без неё. 0 обогащений из 212 ИНН, пришлось убивать PID и перезапускать. Ошибка: запуск долгой необратимой операции без верификации preconditions.
**Pattern:** Перед запуском любой долгой batch-операции на сервере (pipeline, migration, import) проверить список критических env vars через `grep -c`. Python-процесс читает config при старте — добавление переменных в .env во время прогона не имеет эффекта.
**Scope:** situational
**Situation:** запуск долгих pipeline / batch-job / migration на удалённом сервере
**Category:** execution-safety

### 2026-04-18 zvonok-com / session: known constraint not propagated to new client

**Seen:** 1
**Adapted:** —
**Cognitive Error:** known constraint not propagated
**Triad:** новый внешний HTTP-клиент добавляется в систему → явно проверить все существующие сетевые обходные пути и применить к новому клиенту → не допустить прямое соединение в сети с уже известными ограничениями
**Context:** В системе уже был Tor-прокси для одного HTTP-клиента (ofdata.ru). Новый клиент (zvonok.com) добавлен без прокси — Beget так же блокирует TLS к zvonok.com. Потребовался fix-коммит.
**Pattern:** При добавлении нового внешнего HTTP-клиента в систему — сначала прочитать список существующих сетевых workarounds (proxy, tunnel, VPN). Если они существуют — применить к новому клиенту сразу, до тестирования.
**Scope:** universal
**Category:** information-gathering

### 2026-04-20 windows-codex-setup / session 1: user-subset completeness illusion

**Seen:** 1
**Adapted:** —
**Cognitive Error:** user-subset completeness illusion
**Triad:** user-spec опирается на внешний framework/chain (методология, stack, SDK) и пользователь называет подмножество компонентов для установки → открыть entry-point framework'а (его README, главный SKILL/manifest, install doc) и выписать ИМЕННО перечисленные им зависимости до записи компонентов в AC → принимать пользовательский список как финальный scope, игнорируя, что chain сам требует дополнительные элементы
**Context:** Пользователь сказал «тянем 3 скилла (methodology, quick-learning, skill-master) из ai-dev-methodology-codex». Записал в AC «3 скилла». Позже пришлось заново открывать `methodology/SKILL.md`, выяснять, что pipeline требует цепочку из 31 скилла + agents/ + shared/, перевёрстывать Technical Decisions и AC. Один лишний батч интервью и частичная переверстка спека.
**Pattern:** Когда спека импортирует внешний framework или dependency chain, и пользователь называет подмножество — открыть entry-point (README, install section, главный manifest) ДО фиксации AC. Пользовательский список = seed, framework-манифест = финальный scope. Правило «user knows best» не работает для внешних зависимостей, потому что пользователь часто знает только верхушку.
**Scope:** universal
**Category:** information-gathering

### 2026-04-20 notion-crm / session 1: API-created artifacts ≠ UI-created semantically

**Seen:** 1
**Adapted:** —
**Cognitive Error:** API-UI parity assumption
**Triad:** bulk-creating platform artifacts via API that have UI-specific dynamic behaviors → создать 1 artifact через API, прогнать полный end-to-end тест (включая runtime-поведение фичи), только потом масштабировать → API/UI semantic divergence: одинаковая структура артефакта в хранилище, разное поведение в runtime (dynamic filters, template-awareness, permissions)
**Context:** Созданы 12 artifacts через API batch-скрипт, структурно идентичных UI-созданным, но runtime-поведение отличалось (static vs dynamic filter). Пришлось удалять все 12 и пересоздавать вручную через UI.
**Pattern:** Перед bulk-creation через API artifacts, которые в UI имеют runtime-динамику (фильтры по контексту, auto-rewrite, template-binding), создать ОДИН тестовый экземпляр и прогнать полный пользовательский сценарий до конца. Structural equivalence в API-ответе ≠ behavioral equivalence в runtime. Платформа может хранить одинаковую структуру, но обрабатывать её по-разному в зависимости от происхождения.
**Scope:** universal
**Category:** information-gathering

### 2026-04-21 mvp-booking-flow / session 1: runaway parallel subagent fanout without economic gate

**Seen:** 1
**Adapted:** —
**Cognitive Error:** missing fanout-cost gate
**Triad:** about to spawn multiple parallel subagents (any purpose: research, validation, fix, review, generation) → before spawn, estimate fanout cost (agents × expected context per agent) vs remaining session budget; if cost would consume a large share of budget or a prior wave already did, halt auto-spawn and surface options (collapse to one agent / sequential batches / narrower scope / stop and ask) → silent-scaling bias: treat "parallelism available" or "spec allows N" as permission to use maximum fanout without checking whether budget remains for the rest of the session
**Context:** A validation-fix loop kept spawning dozens of parallel subagents per iteration; each wave took ~5 min and had to finish before user could practically redirect. Three rounds × ~20-30 agents burned a large share of context and token budget before the user intervened. Generalises beyond validation loops — any plan phase that says "spawn N research/review/fix agents in parallel" has the same failure mode.
**Pattern:** Any skill or plan step that spawns >3 parallel subagents is a cost checkpoint, not an automatic action. Before spawning: (1) estimate total cost = agents × expected output size × expected tool uses per agent; (2) compare to session-so-far burn (token/context/time); (3) if this wave + remaining pipeline likely exceeds a healthy budget, stop and present to user: expected cost, alternatives (one sequential agent, smaller batch, narrower scope, skip this step). Applies to research fanout, validator fanout, per-task fix fanout, per-file review fanout — any time "parallel subagents" is the chosen pattern. Treat the user's budget as a first-class constraint equal to correctness, not a background assumption.
**Scope:** universal
**Category:** sequencing

### 2026-04-21 content-card-series / session 1: category-typography reflex in editorial context

**Seen:** 1
**Adapted:** —
**Cognitive Error:** category-typography reflex
**Triad:** implementing a commercial-category format inside an editorial/personal-voice context → check whether the voice actually wants that category's typographic conventions before applying them → category-typography reflex
**Context:** Asked to render a pricing card for a personal-brand Telegram channel, I instinctively used marketplace typography — strikethrough old prices, "→" transition arrows, explicit "для подписчиков со спеццена автоматически" framing. User rejected: "суть содержания очень рыночно". The visual decisions bled commercial voice into an editorial brand.
**Pattern:** When implementing a conventional format for a commercial category (pricing, product spec, comparison, discount), do NOT auto-apply the category's typographic kit (strikethrough, discount arrows, % badges, CTA buttons, SKU tables). First check the surrounding voice: editorial/personal? Neutral typographic variants required — prices as simple typography with a middot separator, subscriber price as a color-differentiated inline phrase, no strike/arrow. Content category ≠ typographic category.
**Scope:** universal
**Category:** design-taste

### 2026-04-21 mvp-booking-flow / session 1: silent dependency assumption

**Seen:** 2
**Adapted:** —
**Cognitive Error:** silent dependency assumption
**Triad:** writing code or a task that calls a function/service/utility defined elsewhere in the codebase → grep the actual call-site signature and injected dependencies of that function before wiring it up → silent dependency assumption: assuming the target is self-contained or already injected based on its name alone, without verifying how the surrounding system provides its dependencies
**Context:** In wave-3 FSM storage tasks, a helper was referenced by name as if it accepted only domain-level arguments. The actual implementation required a `bot` instance injected through a `deps` container that the calling code never assembled. The omission was invisible until integration — the function silently failed to resolve its dependency at runtime. (Seen 2: session 3 — task 14 teammates assumed bookings.mark_draft_abandoned signature from spec; actual signature added session_factory param per established DI pattern.)
**Pattern:** Before writing any call to a function or service across a module boundary, grep its actual definition: what arguments does it take, what does it inject or import, what preconditions must be satisfied? Name-based inference ("this looks like a pure utility") is unreliable — the real signature may carry injected state (bot, db, config, context). Check the signature, not the name.
**Scope:** universal
**Category:** information-gathering

### 2026-04-21 КульмИИнатор / session 6: Middleware dispatch model assumption

**Seen:** 1
**Adapted:** —
**Cognitive Error:** unconditional middleware assumption
**Triad:** writing test that triggers middleware → verify whether framework fires middleware on all events or only on handler-matched dispatch → assume middleware runs unconditionally on every incoming event
**Context:** A test was written to trigger pre-handler logic by sending an event in a state that had no matching handler — the middleware never fired because the framework only runs "inner" middleware as part of handler dispatch, not on every event.
**Pattern:** Before writing tests for middleware behavior, check the framework's middleware dispatch model: "inner" (wrapped) middleware fires only when a handler is dispatched; "outer" (router-level) middleware fires on all events. If no handler matches the event, inner middleware is bypassed entirely. Design test input to match an existing handler.
**Scope:** universal
**Category:** information-gathering

### 2026-04-21 mvp-booking-flow / session 4: Spec-prescribed test tool incompatible with component

**Seen:** 1
**Adapted:** —
**Cognitive Error:** prescribed-mechanism trust
**Triad:** spec prescribes a specific test tool for an async/stateful component → verify tool-component compatibility before writing tests; fall back to asserting observable state if incompatible → prescribed-mechanism trust: using the spec's tool name without checking whether it works with the target component
**Context:** A task spec said "use freezegun to advance clock through scheduled jobs." The test tool (freezegun) and the async scheduler component are a brittle pairing — freezegun does not reliably intercept the scheduler's internal clock. The agent pivoted to asserting the `run_date` on scheduled triggers directly, which is the observable contract without needing to fire jobs.
**Pattern:** When a spec names a test tool for an async or stateful component, verify the combination is viable before writing tests. If incompatible, assert the observable contract (scheduled times, stored state, emitted events) rather than the execution mechanism. The contract is what matters; the prescribed mechanism is a suggestion.
**Scope:** universal
**Category:** tool-selection

### 2026-04-21 mvp-booking-flow / session 4: Integration test references future-wave function

**Seen:** 1
**Adapted:** —
**Cognitive Error:** cross-wave forward reference
**Triad:** integration test in wave N references a function not yet implemented in wave N+k → embed a minimal local stub preserving the observable contract; add an import-swap comment → cross-wave forward reference: attempting to import from a boundary that does not yet exist, treating "future work" as present
**Context:** Task 21 integration tests needed a job-coroutine from Task 23 (same or later wave, not yet committed). Rather than skipping or marking tests as blocked, the agent embedded a minimal stub matching the documented DB-gate behavior with a one-line comment indicating the real import path for when the function ships.
**Pattern:** When a task's tests depend on a function from a later wave, embed a minimal local stub that mirrors the documented contract. Add one comment: `# replace with: from module import fn when task N ships`. Do not skip the tests or block on the dependency — the stub preserves test intent without waiting.
**Scope:** universal
**Category:** sequencing

### 2026-04-21 mvp-booking-flow / session 6: extra action past protocol terminus

**Seen:** 1
**Adapted:** —
**Cognitive Error:** permissive gap assumption
**Triad:** autonomous worker receives a step-by-step completion protocol without explicit scope termination → explicitly bound the protocol with a "these N steps only, no additional steps" statement → permissive gap assumption: executor treats the gap between "not listed" and "not prohibited" as permission
**Context:** A worker was given a 3-step commit protocol (implement → review-reports → done). Without an explicit "no other commits" statement, the worker added a 4th "session complete" commit — a step belonging to the orchestrator's role, not the worker's.
**Pattern:** When specifying completion protocols for autonomous workers, close the protocol with an explicit termination statement: "Only these N steps. Do not add any further commits, messages, or actions." Without it, executors fill the undefined tail with what seems helpful, overstepping role boundaries.
**Scope:** universal
**Category:** communication

### 2026-04-21 mvp-booking-flow / session 6: defined artifact ≠ runtime invocation

**Seen:** 1
**Adapted:** —
**Cognitive Error:** definition-as-invocation assumption
**Triad:** implementing a module with exported constants/functions → trace the call path from every entry point to each defined artifact before marking done → treating "constant defined and exported" as equivalent to "constant used at runtime"
**Context:** A text constant was written, exported, referenced in docs, and confirmed present in the module — but the handler that was supposed to send it only sent a different message. The definition was never wired to the entry point. Discovered only during live testing.
**Pattern:** After implementing any output artifact (text, side-effect, message), trace backward from the user-visible entry point to verify the artifact is actually invoked. Presence in a module is not evidence of execution; only the call graph is.
**Scope:** universal
**Category:** information-gathering

### 2026-04-21 kulminiator / session calibration-1: narrow except hides side-effect swallowing

**Seen:** 1
**Adapted:** —
**Cognitive Error:** narrow except silently propagates
**Triad:** function wraps an external call in a named-exception tuple → catch all exceptions that represent "unavailable" semantics, then add `# noqa: BLE001` with rationale → assuming a named-exception list is exhaustive when the API surface is broad
**Context:** A helper caught three specific exception types for "API unavailable" and returned a fallback value. A fourth exception type with the same semantic was not listed, so it propagated upward and silently killed the caller's response path with no error message to the user.
**Pattern:** When the intent is "treat any failure from this external call as unavailable", use `except Exception` with a suppression annotation rather than enumerating exception types. Enumerate only when different exception types require different handling paths.
**Scope:** universal
**Category:** problem-decomposition


### 2026-05-09 rebuild-site-no-tilda-06-paykeeper / verification: cyrillic JSON in inline bash mangles payload

**Seen:** 1
**Adapted:** —
**Cognitive Error:** shell expansion through cyrillic-bearing string
**Triad:** sending structured payload with non-ASCII or quote-containing strings via CLI/script → use a serializer or file, never manual string interpolation → encoding-mangling assumption: trusting manual string building to produce valid structured data through variable expansion
**Context:** (1) curl AC smoke-check: inline `--data "$VAR"` mangled cyrillic — fix: heredoc file + `--data-binary @file`. (2) PowerShell Telegram test: manual `"{...\"$msg\"...}"` truncated message at embedded quote — fix: `@{text=$msg} | ConvertTo-Json` serializes safely.
**Pattern:** Never build JSON by hand when payload contains user-controlled or non-ASCII strings. Bash: heredoc file + `--data-binary @file`. PowerShell: `ConvertTo-Json`. Node/Python: `JSON.stringify`/`json.dumps`. Serializer is the only safe path — manual interpolation breaks on first embedded quote or non-ASCII byte.
**Seen:** 2
**Scope:** universal
**Category:** tool-selection

### 2026-05-09 rebuild-site-no-tilda-06-paykeeper / verification: read validators+registry before AC smoke sequence

**Seen:** 1
**Adapted:** —
**Cognitive Error:** payload guessing from spec wording
**Triad:** about to run a series of curl/HTTP smoke-checks against an API → read every zod/joi validator and every closed-set registry (enums, slug tables, code maps) the route depends on, then assemble the first valid payload from those sources → spec-as-payload-source: assuming user-spec wording reflects field types and exact enum values when validators are the actual contract
**Context:** First valid `/api/forms/order` smoke-call took 3 retries: `Checkbox:"on"` (validator wanted `z.literal(true)`), `child_class` wording mismatch (free-form OK), `serviceName:"ШКОЛА 1-11 — 1-4 классы"` (registry stored `"За пользование платформой"`). All three could have been read directly from `src/lib/validators/order.ts` and `src/content/orderCodes.ts` before the first request.
**Pattern:** Before running a smoke-check sequence against any API route, open the route's validator files and any closed-set registries it queries (enums, slug tables, code lookups). Assemble the first request from those exact values, not from user-spec/tech-spec narrative wording. Narrative is allowed to drift; validators are the contract.
**Scope:** universal
**Category:** information-gathering

### 2026-05-09 rebuild-site-no-tilda-06-paykeeper / verification: psql `\d "Table"` before ad-hoc SELECT

**Seen:** 2
**Adapted:** —
**Cognitive Error:** naming-parity assumption
**Triad:** about to write queries/extractors against an external system (DB, API) using field names from docs/models/specs → first run live introspection (`\d "Table"`, `databases.retrieve`, equivalent) and pick names from actual schema → naming-parity assumption: trusting that doc/model names match the live schema 1:1
**Context (Seen 1, 2026-05-09):** Tried `SELECT id, "paykeeperId", "serviceName", "priceRub" FROM "Order"` based on Prisma model intuition. The actual columns are `paykeeperRaw` (jsonb holding `{paymentId, paymentUrl}`) and `orderCode`/`items`/`total` — there is no `paykeeperId` or `priceRub` column. PSQL `ERROR: column "paykeeperId" does not exist` after the query already cost a roundtrip. `\d "Order"` would have surfaced the real schema in one command.
**Context (Seen 2, 2026-05-23 notion-data-import sketch):** Wrote a Notion-to-SQLite importer with property-name heuristics like `findByName(props, ['Организ', 'Org'])` based on the spec `freelance-os-spec.md`. After import all 22 movements had `org_id: null`. The actual Notion property in the Движения database is `Контрагент (орг)`, not `Организация` — the spec was outdated. A single `notion.databases.retrieve(movementsDbId)` printout at the start would have shown the real property names in seconds; instead the discovery came from inspecting `raw_props` of imported rows post-hoc, requiring a fix-import cycle.
**Pattern:** Before issuing any query/extractor against an external system (DB via ORM, third-party API, spreadsheet, file format) where field/property names are read from a secondary source (model, spec, docs), run a live introspection call once and confirm the names. Specs drift, ORMs rename, third-party schemas evolve — the live source is the only one that matches the data you'll receive.
**Scope:** universal
**Category:** information-gathering

### 2026-06-08 cabinet-sources-api / decompose: task-creator imports a conventionally-named code symbol into a generated smoke snippet without verifying the module's real exports

**Seen:** 1
**Adapted:** —
**Cognitive Error:** convention-variant symbol invention
**Triad:** a task-creator (or anyone) writes a verification/smoke/QA snippet that imports a code symbol from a project module → grep the module's actual exports and confirm the exact symbol name exists before emitting the snippet; never assume a conventionally-named sibling (e.g. a synchronous variant of an async-only export) exists → convention-variant invention: a runtime ImportError silently turns the smoke check into a no-op, so a broken or missing migration/route passes verification unnoticed
**Context:** Two generated tasks (pre-deploy QA + deploy runbook) both wrote `from app.db.session import engine_sync` for a table-presence migration smoke. The module exports only an async `engine` (AsyncEngine) — `engine_sync` never existed; it was invented because table inspection is *conventionally* done with a sync engine. On the VPS the snippet would have ImportErrored, making the migration-presence check a silent no-op. Reality-checker flagged it as critical in both tasks; fix was to use the real `engine` via `async with engine.begin()` or the Alembic CLI (`alembic current`).
**Pattern:** A smoke/QA snippet that ImportErrors does not fail loudly as "wrong check" — it fails as "check never ran", which reads as green if the surrounding step swallows the error or the snippet is the whole check. Before referencing any importable symbol in generated verification code, grep the source module for the exact name. Especially distrust "conventional sibling" symbols — a sync twin of an async export, a `*_sync`/`*_async` pair, a `get_X` next to an `X` — these feel obviously-present but are exactly where invention by convention happens. Sibling of [[verify file paths not guess]] and the QA-curl-endpoint pattern: same goal (no broken verification artifact pointing at a non-existent thing), different artifact (importable code symbol, not a path or URL).
**Scope:** universal
**Category:** information-gathering

### 2026-06-09 cabinet-sources-api / session 1: неожиданные off-task артефакты делегата приняты за мусор

**Seen:** 1
**Adapted:** —
**Cognitive Error:** unexpected-as-erroneous
**Triad:** делегированный исполнитель оставил неожиданные коммиты/изменения, не относящиеся к выданной задаче (а реальный результат — незакоммиченным) → осмотреть содержимое и ценность артефакта до отката/очистки; реальный результат верифицировать через состояние системы, не по отчёту → unexpected-as-erroneous: счесть удивившие off-task артефакты мусором и снести легитимную работу
**Context:** Делегированный агент ушёл с задачи: сделал два коммита на постороннюю тему и вернул бессвязный финальный отчёт, оставив свой настоящий результат незакоммиченным и непрогнанным. Инстинкт «откатить чужие неожиданные коммиты как мусор» уничтожил бы качественную, корректную работу; инстинкт «доверять отчёту» пропустил бы невыполненную задачу.
**Pattern:** Когда исполнитель (агент или человек) оставляет после себя удивляющие артефакты — коммиты/файлы/изменения вне согласованного скоупа — сначала исследуй их содержимое и ценность, и только потом решай про откат: неожиданное ≠ ошибочное. Параллельно не путай наличие отчёта с выполненной работой — верифицируй фактический результат через состояние системы (git log/diff, прогон тестов), а не по словам исполнителя. Две ловушки тянут в противоположные стороны (снести лишнее vs. поверить на слово), и обе закрываются одним движением: посмотреть на реальное состояние до любого необратимого действия. Sibling of [[Субагент сообщает о блокере — верифицировать самостоятельно]].
**Scope:** universal
**Category:** information-gathering


### 2026-06-14 fizika-generative-info / session 2: surrogate-target confusion in path-specific tests

**Seen:** 1
**Adapted:** —
**Cognitive Error:** surrogate-target confusion
**Triad:** writing a test for a specific execution path when a fallback/alternative path produces the same observable output → assert the path-activation observable (call count on the intended component, spy, state flag) in addition to the output → surrogate-target confusion: output present does not prove the intended path fired
**Context:** Across two tasks, tests repeatedly asserted on mock-stub content or fallback values that are equally produced by both the target path and the fallback path. A test that passes when the fallback fires is not a test for the target path. Fixes required adding explicit call-count assertions (mock_gen.call_count >= 1) and spies on the function that activates the target path, not just checking the returned string.
**Pattern:** When the tested path has a sibling fallback that produces the same or similar output, the output alone cannot distinguish which path fired. Assert the activation observable of the intended path — typically a mock call count, a spy invocation, or a state flag set only by that path — before asserting the output. Apply this check automatically whenever the function under test has more than one execution branch that returns the same type of result.
**Scope:** universal
**Category:** problem-decomposition

### 2026-06-14 fizika-generative-info / session 2: local-position phase inference

**Seen:** 1
**Adapted:** —
**Cognitive Error:** local-position phase inference
**Triad:** an executor writing a handoff or next-phase plan for the orchestrator infers the session/phase boundary from the position of their own task → consult the authoritative session plan to find the actual phase boundary before writing the handoff → local-position inference: "my task is done" does not mean "the phase is done"
**Context:** A subagent completing what it perceived as the last task overwrote the next-session prompt with a wrong framing ("Session 3 = only Task 6") when Task 6 was actually still in Session 2. The subagent inferred the session boundary from its own task number rather than from the session-plan document, requiring the orchestrator to detect and correct the misframing.
**Pattern:** Any executor that writes a phase-transition artifact (handoff, next-session prompt, summary, release note) must first verify the boundary in the authoritative plan rather than deriving it from task position. The local task index is not a reliable proxy for the broader plan structure — the plan may interleave waves, defer tasks, or group multiple tasks into one session.
**Scope:** universal
**Category:** scope-management

### 2026-06-16 bot-config-from-platform / session 1: delegated worker paused for review it could never receive

**Seen:** 1
**Adapted:** —
**Cognitive Error:** protocol-channel mismatch
**Triad:** a delegated worker (subagent) following a "stop and ask for review" protocol mid-task, but its role has no channel to receive the answer → run delegated work to completion with all decisions pre-baked into the brief and an explicit "do not pause for review"; route any genuine open question to a fresh respawn, never an in-place wait → protocol-channel mismatch: applying an interactive protocol whose response channel does not exist in this role turns a pause into an unrecoverable deadlock
**Context:** A coder subagent honored the global "one block at a time, stop for user review" rule and paused mid-task to ask a review question. But a subagent has no back-channel to receive a reply, so the pause was not a pause — it was a deadlock. The orchestrator had to abandon the stuck agent and respawn a fresh one with the decisions pre-baked and an explicit "do not stop for review" instruction. The interactive review protocol belongs to the top-level agent (which can talk to the user); a worker without that channel must never enter a wait state.
**Pattern:** Before a role adopts any protocol that suspends execution awaiting an external response (review approval, confirmation, clarification), verify the role actually owns a channel to receive that response. A worker that lacks the channel must not inherit the "stop and ask" behavior — it must run to completion on pre-baked decisions, and any real ambiguity must be resolved by the delegator up front (or by a fresh respawn), not by an in-place wait. Generalizes beyond agents: any actor handed a coordination protocol designed for a different communication topology will deadlock where the assumed channel is absent. Sibling of [[verify inter-agent tooling availability before planning review rounds]] (planner-side: confirm the channel exists; this entry is worker-side: don't enter a wait the channel can't service).
**Scope:** universal
**Category:** communication

### 2026-06-16 fizika-channel-abstraction / session 1: handoff looked complete to the author but had a contract hole

**Seen:** 1
**Adapted:** —
**Cognitive Error:** author-POV completeness blindness
**Triad:** finalizing an instruction/spec a context-less party must act on alone → before delivering, re-read it in that party's role and enumerate what they'd be missing (input/output contracts, signatures, required fields, unresolved forks), then resolve in-place → author-POV completeness blindness: judging "complete" against context the consumer does not share
**Context:** A handoff artifact read as complete from the author's side but omitted an interface detail (a callback's input contract and a required field) the executor needed; the gap stayed invisible until the artifact was re-read from the executor's perspective, which surfaced the exact point where they'd stall.
**Pattern:** Before delivering any artifact a context-less party must act on alone (handoff, spec, API doc, task brief), simulate their reading: step into their role and list what they'd be missing — contracts, signatures, fields, decisions left open — then close those in place rather than leaving them to discover mid-work. Author-side review measures completeness against context the consumer lacks, so it systematically misses interface holes that look obvious to the author. Distinct from consumer-capacity blindness (size/budget) and producer-side naming assumption (derive names from consumer code): the corrective here is a perspective-swap verification pass, not a specific contract source.
**Scope:** universal
**Category:** communication

### 2026-06-17 fizika-intent-interpreter / session 2: heaviest component on a budget-bounded subtask

**Seen:** 1
**Adapted:** —
**Cognitive Error:** capability-cost blindness
**Triad:** reusing the most-capable component (or its richest mode) for a sub-task that has a tight latency/resource budget → match the component's working mode to the budget — switch off its heavy/optional work, or pick a lighter variant, before enlarging the budget → capability-cost blindness: treating "more capable" as strictly better while its extra work silently and variably consumes the budget
**Context:** A powerful general component was reused for a small bounded sub-task on the "more capable is safer" default; its optional heavy work (variable, sometimes huge) intermittently consumed the whole budget, causing failures that looked like the budget being too small — so the first fix (enlarge the budget) only shifted the failure instead of removing it.
**Pattern:** When a sub-task has a hard latency/size/resource ceiling, do not assume the most-capable component is the right default — its extra capability does optional, often nondeterministic work that spends the same ceiling. Match the mode to the task: disable the heavy/optional behavior or pick a lighter variant, and only then size the budget. Growing the budget to absorb the overhead treats the symptom; removing the unneeded overhead removes the cause. Verify the lighter mode against the source's own docs and reproduce it before relying on it.
**Scope:** universal
**Category:** tool-selection

### 2026-06-18 fizika-widget-channel / planning: cross-cutting wrapper attached at a shared boundary leaked to sibling routes

**Seen:** 1
**Adapted:** —
**Cognitive Error:** shared-boundary scope blindness
**Triad:** attaching a cross-cutting behavior (filter/guard/header-adder/interceptor) at a shared boundary to serve one subset of consumers → verify the boundary's real coverage; if it spans the whole surface, attach the behavior at a narrower sub-boundary covering only the intended subset and add a check that the other consumers are unchanged → shared-boundary scope blindness: assuming a behavior added "for X" applies only to X when its attachment point covers all siblings
**Context:** A cross-cutting wrapper was added at a shared entry boundary to serve one group of endpoints, on the assumption it only affected that group; the framework applied it to the whole surface, silently altering/disarming sibling endpoints that carried their own protection.
**Pattern:** Before attaching cross-cutting behavior (auth, CORS, rate-limit, logging, headers) to serve a subset, confirm the attachment point's actual coverage. If it wraps the whole surface, move it to a scoped sub-boundary (sub-app / nested router / mount) covering only the intended subset, and add a regression check asserting the untouched siblings keep their prior behavior and protections. "I added it for X" is not "it applies only to X."
**Scope:** universal
**Category:** scope-management

### 2026-06-18 fizika-widget-channel / session 1: two layers enforced the same constraint with disagreeing outcomes

**Seen:** 1
**Adapted:** —
**Cognitive Error:** redundant-gate authority blur
**Triad:** two layers each independently enforce the same constraint but produce different observable outcomes (one rejects, the other clamps-and-continues) → name the contract the spec actually requires, make exactly one layer the sole authority for it, and remove enforcement from the other rather than keeping both → redundant-gate authority blur: stacking "defense-in-depth" validators that silently disagree on the observable result, with no layer designated as the canonical one
**Context:** The same constraint was guarded at two layers — an upstream validator that hard-rejects and a downstream gate that clamps-and-continues — added independently as "defense in depth"; they disagreed on the observable outcome (reject vs accept-with-refusal), and only a test asserting the required contract exposed which behavior was canonical.
**Pattern:** When two layers enforce one invariant, they are not automatically redundant-but-safe — if their failure modes differ (one rejects, one degrades), they encode two different contracts and will silently conflict. Decide which observable outcome the spec requires, make a single layer the authority for that constraint, and delete the other layer's enforcement of it rather than leaving both. Stacked validators are safe only when their outcomes are identical; when they differ, more layers means more ambiguity, not more safety.
**Scope:** universal
**Category:** problem-decomposition

### 2026-06-18 fizika-widget-channel / session 2: probe-method artifact ≠ system defect

**Seen:** 1
**Adapted:** —
**Cognitive Error:** probe-artifact-as-defect conflation
**Triad:** a post-deploy smoke probe returns a red result (error code / redirect / empty) → re-issue it with the method and flags the real consumer actually uses before concluding a defect → mistaking an artifact of the probe method for a fault in the system under test
**Context:** A post-deploy smoke run flagged two endpoints as broken (one returned 405, one 307), but the red results were artifacts of the probe method — a HEAD request against a GET-only route, and a probe that did not follow the mount redirect — not real failures; re-running with GET and follow-redirects showed both correct.
**Pattern:** When a smoke/health check comes back red, first check whether the probe itself was shaped like the real consumer: a HEAD where the client does GET, default flags that skip redirects/headers, a method the route never advertised. Re-issue the probe the way the actual caller hits it before logging a defect, opening a fix, or blocking a release. A red signal from a mismatched probe is noise; vary the probe before trusting the verdict.
**Scope:** universal
**Category:** tool-selection

### 2026-06-19 cabinet-dialogs / session 2: spec-count arithmetic drift

**Seen:** 1
**Adapted:** —
**Cognitive Error:** specification-over-measurement
**Triad:** spec утверждает точное количество элементов в тестовом наборе → пересчитать фактические данные и ассертировать реальный count, не число из документа → принять числовой AC в документе за истину без проверки реальных данных
**Context:** Task 6 spec написал "10 messages", но реальная fixture содержала 4 non-/new turns → 8 messages. Исполнитель правильно поймал расхождение, ассертировал 8 и зафиксировал deviation. Если бы ассертировал 10 из spec — тест был бы ложно красным или тихо зелёным с неправильной логикой.
**Pattern:** When an acceptance criterion states an exact count ("N messages", "K records", "M lines"), do not trust the number in the document — count the actual test data before writing any assertion. A spec's arithmetic can drift from reality during editing without invalidating the rest of the spec. Measure first, then assert; a deviation from spec is a flag for the author, not a reason to force-fit the fixture.
**Scope:** universal
**Category:** information-gathering

### 2026-06-20 widget-constructor / user-spec: constraint-preservation anchoring

**Seen:** 1
**Adapted:** —
**Cognitive Error:** constraint-preservation anchoring
**Triad:** an inherited or self-imposed scope constraint forces the feature to deliver only part of its stated intent → name the constraint↔intent conflict and the cost of relaxing it as an explicit decision, instead of recommending the constraint-respecting half-version as the default → optimizing to honor the boundary over delivering the feature's purpose, shipping a half-feature that technically respects the constraint
**Context:** user-spec said "don't touch the widget runtime". The "allowed domains" field could only half-work under that constraint — the server-side gate could read a managed list, but the browser CORS preflight stayed static, so a newly-added domain stayed blocked until an env change + restart. I recommended that half-version as an accepted MVP limitation; the owner had to push twice ("give both guards the live list") before I relaxed the constraint and delivered the field end-to-end via a small dynamic-CORS middleware — the genuinely simpler full solution.
**Pattern:** When a constraint you inherited or imposed forces a feature to deliver only part of its stated purpose, do not default to recommending the constraint-respecting degraded version. Name the conflict explicitly — "this boundary makes feature X only half-work; relaxing it costs Y" — and let the decision-owner weigh intent against constraint. The constraint is a means; the feature's purpose is the end. A half-feature that perfectly respects a self-imposed boundary is often worse than a whole feature that relaxes it cheaply.
**Scope:** universal
**Category:** problem-decomposition

### 2026-06-20 widget-constructor / session 1: self-guarding read-back blindness

**Seen:** 1
**Adapted:** —
**Cognitive Error:** self-guarding read-back blindness
**Triad:** writing a test/verification that reads back state through the same access layer that enforces a contextual access guard (row-level security, scope/ownership filter, tenant isolation) → make the read-back query itself satisfy the guard's required predicate (carry the scope/owner key); never assert via an unscoped lookup → treating verification queries as exempt from the guard under test, so the check fails on the guard you are validating, not the behavior
**Context:** In a tenant-guard test, the read-back `SELECT` had no `tenant_id` predicate. The guard (TenantScopeViolation) correctly fired on the verification query itself — the guard was alive and the production code was fine, but the test was written as if its own queries were exempt from the very isolation it was asserting. The failure pointed at the guard, not at the behavior under test.
**Pattern:** When a test reads state back through an access layer that enforces a contextual guard (row-level security, ownership/scope filter, tenant isolation), the verification query is subject to that same guard — it is not exempt. Write read-backs guard-compatibly: carry the scope/owner predicate the guard requires. Otherwise an unscoped lookup trips the guard you are validating, and you will misread "guard works" as "behavior broken" and chase a phantom bug in correct production code.
**Scope:** universal
**Category:** information-gathering


### 2026-06-21 widget-constructor / session 2: field-default camouflage in fallback tests

**Seen:** 1
**Adapted:** —
**Cognitive Error:** field-default camouflage
**Triad:** writing a test for fill/override logic where the model field has a static default value → verify the asserted value differs from the field's static default; if they are equal, force an input that makes the field unreachable without the logic under test → field-default camouflage: static default masks absent fill-logic, test passes green on broken code
**Context:** Tests for per-field fallback logic asserted values (e.g. accent_color="#7B61FF") that happened to match the field's Pydantic static default. The fallback code could be entirely absent and the test would still pass, because Pydantic supplies the default before any override logic runs. The test-reviewer flagged this as major; fixes required using a settings value that differs from the model default, then asserting the settings-derived value.
**Pattern:** Before finalizing a test for fill/override logic, ask: "Would this assertion still pass if the fill-logic were deleted?" If yes, the test is vacuous. Force the fixture so the expected value is only reachable via the logic under test — use a settings/config value that differs from the model field's static default, or patch the default itself. Apply this wherever the model has non-None static defaults and the logic supplies those same values.
**Scope:** universal
**Category:** problem-decomposition

### 2026-06-21 widget-constructor / session 2: handler-isolation blindness in layered processing

**Seen:** 1
**Adapted:** —
**Cognitive Error:** handler-isolation blindness
**Triad:** multiple independent processing layers (middleware, hook, filter, handler) handle the same unit-of-work and each independently reads a shared data source → enumerate all reads across layers and deduplicate at the unit boundary → handler-isolation blindness: each layer looks self-contained when read locally, so cross-layer fetch duplication is invisible
**Context:** A middleware and a route handler both called the same config-fetch function within the same request. When reading each component in isolation, both looked correct. The duplication only became visible during cross-component code review, flagged as a major finding. Fix: extract a shared helper and call it once per request, passing the result to downstream components.
**Pattern:** When writing a processing layer (middleware, decorator, filter, handler) that reads shared data, check whether any other layer in the same unit-of-work boundary already fetches or will fetch the same source. Treat the unit-of-work (request, event, job) as the deduplication scope. Extract a single fetch point and pass the result; do not rely on each layer being self-contained — that assumption fails as soon as two layers read the same source.
**Scope:** universal
**Category:** problem-decomposition

### 2026-06-22 widget-constructor / session 3: surface-local reimplementation drift

**Seen:** 1
**Adapted:** —
**Cognitive Error:** surface-local reimplementation drift
**Triad:** one capability is delivered through multiple surfaces/adapters, each with its own presentation layer → hold its behavior/output identical everywhere, pick one surface as the reference and validate every other surface's actual output against it live → surface-local reimplementation drift: each adapter looks self-contained, so a surface silently reimplements or trims the shared behavior and diverges
**Context:** A capability already working on a reference surface was exposed through a second surface that re-implemented its output rendering. The second surface silently diverged (it trimmed/omitted behavior the reference surface had), and the divergence was invisible to tests that ran only against the second surface in its own default condition — it surfaced only on live cross-condition verification. The reasoning error was treating each surface as independently "done" once its own checks passed, instead of holding all surfaces to one behavioral contract.
**Pattern:** When one capability ships through several surfaces/adapters, make behavioral parity an explicit contract: designate one surface as the reference, keep the shared logic in one place, and validate every other surface's *actual* output against the reference — a surface that renders or handles the same input differently is a defect, not an acceptable variation. Same-surface tests cannot see parity gaps, so verify each surface live on identical inputs.
**Scope:** universal
**Category:** problem-decomposition

### 2026-06-23 zina-draft-review / session 1: post-mutation guard placement

**Seen:** 1
**Adapted:** —
**Cognitive Error:** post-mutation guard placement
**Triad:** a transactional mutation is paired with an out-of-transaction state flip that signals "already done" → set the idempotency sentinel BEFORE issuing the mutation (optimistic lock), not after → post-mutation guard placement: the "done" signal sits after the commit, leaving a concurrency window where a concurrent caller passes the guard and duplicates the mutation
**Context:** A function committed a DB mutation inside a transaction, then set an external state flag (out-of-transaction) to mark the operation complete. A concurrent call arriving between commit and flag-set would pass the guard and execute the mutation a second time. Both the implementing agent and a security reviewer classified the state update as non-security; it was caught only by code-review. The reasoning error was treating the "done" flag as a logging step rather than as a concurrency control boundary.
**Pattern:** When a mutation guarded by an idempotency check also updates an out-of-transaction sentinel (cache key, file, in-memory flag), set the sentinel BEFORE issuing the mutation. If the mutation then fails, clear the sentinel (rollback the lock). Placing the sentinel after the commit creates a concurrency window proportional to commit latency — any concurrent caller that slips through will duplicate the mutation without any guard detecting it.
**Scope:** universal
**Category:** sequencing

### 2026-06-23 managed-widget-config / session 3: gated-source default

**Seen:** 1
**Adapted:** —
**Cognitive Error:** gated-source default
**Triad:** asked to retrieve reference facts that live behind an authenticated/interactive surface (control panel, login, owner, support ticket) → first check whether the same facts are observable from a public/zero-auth source (registry, public lookup, exposed metadata) and derive them there before requesting credentials or access → gated-source default: treating the authenticated surface as the required source for facts that are in fact publicly observable, so you ask for access/credentials before checking
**Context:** Asked "can't you just log into the hosting panel and grab the inputs?", the reflex options were (a) request credentials and drive the gated panel or (b) ask the owner to read it out. The actual unknowns — which TLD was registered, where the apex points, which nameservers — were all derivable from public DNS/whois with zero authentication. Checking the public source first closed every open fork (and revealed the apex already pointed at the target host) without touching the gated panel or spending an owner round-trip.
**Pattern:** When a fact is asked to be fetched from a credential-gated or interactive source, first ask "is this same fact publicly observable?" Many infra/config facts (DNS records, nameservers, registration, TLS chain, public endpoints, open APIs) are queryable with zero auth. Exhaust the zero-auth observable path before requesting credentials, panel access, or an owner round-trip — reserve the gated source for facts that genuinely live only behind it. This also avoids an outward/risky action when a read-only public probe suffices.
**Scope:** universal
**Category:** information-gathering

### 2026-06-23 managed-widget-config / session 3: proxy-signal success conflation

**Seen:** 1
**Adapted:** —
**Cognitive Error:** proxy-signal trust
**Triad:** confirming an action succeeded by reading a transformed/secondary signal (a piped or filtered output, a derived view, a downstream stage's status) → read the action's OWN outcome at its source, not the derived signal → proxy-signal trust: a downstream transform reports success while the underlying action failed, so the derived signal reads green over a real failure
**Context:** An operation's result was judged from a secondary signal instead of the action itself. A command's exit status was read after it was piped through a filter, so the pipeline's exit (the last stage's) replaced the command's real exit and a hard failure read as success — a service had been removed but not recreated, yet "deployed" came back green. The same error in a different guise: a test asserting a value was *substituted* stood in for the value actually *behaving*, so a broken render passed. Both checks were green over a red action.
**Pattern:** When confirming an action worked, read its outcome at the source, never through a transform that can mask failure. Don't judge a command by a piped/`tail`ed output — the pipeline's exit is the last stage's, not the command's (use pipefail or inspect the command's own status). Don't judge "it works" by "the value is present/substituted/exists" — assert the actual end behavior. A green derived signal sitting over a red action is worse than no check: it manufactures false confidence and you stop looking exactly when you should dig in.
**Scope:** universal
**Category:** information-gathering
