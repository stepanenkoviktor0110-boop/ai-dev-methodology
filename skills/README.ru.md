# AI-First Development Methodology v1.5 — Claude Code

[English version](README.md)

Структурированная AI-First методология разработки для [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Каждая фича проходит через спек-пайплайн с автоматическими валидаторами и quality gates на каждом этапе.

## Что это делает

Полный фреймворк разработки, где AI-агенты ведут весь цикл: требования → архитектура → задачи → код → ревью → документация. Ты направляешь процесс, агенты делают работу.

**Какие проблемы решает:**
- **Потеря контекста между сессиями** — распределённая база знаний сохраняется между сессиями
- **Качество без ручного ревью** — автоматические валидаторы на каждом этапе
- **Расползание скоупа** — спеки утверждаются до начала кодирования
- **Устаревшие знания о библиотеках** — Context7 MCP подтягивает актуальную документацию

## Установка

### Требования

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) установлен и настроен
- [GitHub CLI](https://cli.github.com/) (`gh`) для инициализации проектов
- Git

### Шаг 1: Клонировать фреймворк

```bash
git clone https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology.git ~/.claude/skills
```

Это размещает все скиллы и шаблоны там, где Claude Code их ожидает (`~/.claude/skills/`).

### Шаг 2: Настроить Claude Code

Добавить в `~/.claude/CLAUDE.md`:

```markdown
# Global Preferences

## Communication
- Общаться с пользователем по-русски. Код и команды — на английском.
```

### Шаг 3: Настроить MCP (опционально, но рекомендуется)

Добавить [Context7](https://github.com/upstash/context7) MCP-сервер для актуальной документации библиотек.

### Шаг 4: Проверить установку

```bash
ls ~/.claude/skills/methodology/SKILL.md
```

## Использование

### Новый проект (с нуля)

```
/init-project                  # Шаблон + git + GitHub репо
/init-project-knowledge        # Интервью → заполнить всю документацию проекта
```

### Новая фича (полный пайплайн)

```
/new-user-spec                 # Шаг 1: Интервью → user-spec.md (требования)
                               #   ⛔ пользователь утверждает спек
/new-tech-spec                 # Шаг 2: Исследование → tech-spec.md (архитектура)
                               #   ⛔ пользователь утверждает спек
/decompose-tech-spec           # Шаг 3: Разбивка на задачи → tasks/*.md
                               #   ⛔ GATE 1: пользователь утверждает декомпозицию
                               #   ⛔ GATE 2: пользователь утверждает план сессий (LOC бюджет)
                               #   ⛔ HARD STOP — нет авто-перехода к коду
/do-feature                    # Шаг 4: Выполнение задач по волнам
                               #   ⛔ GATE 3: пользователь подтверждает скоуп сессии + LOC
                               #   ⛔ GATE 4: конец сессии → отчёт + промт + СТОП
/retrospective                 # Шаг 5: Извлечь уроки → обновить скиллы
/done                          # Шаг 6: Обновить документацию проекта → архивировать фичу
```

Каждый шаг имеет валидаторы и **блокирующие гейты** — ни один шаг не продолжается без явного одобрения пользователя:

| Шаг | Команда | Валидаторы | Гейты | Результат |
|-----|---------|-----------|-------|-----------|
| Требования | `/new-user-spec` | quality + adequacy (2) | пользователь утверждает спек | `user-spec.md` |
| Архитектура | `/new-tech-spec` | skeptic + completeness + security + test + template (5) | пользователь утверждает спек | `tech-spec.md` |
| Задачи | `/decompose-tech-spec` | template + reality (2) | утверждение задач, затем план сессий | `tasks/*.md` + `session-plan.md` |
| Код | `/do-feature` | code + security + test ревьюеры (3) | подтверждение скоупа, СТОП в конце сессии | коммиты |
| Аудит | (авто, последние волны) | holistic code + security + test аудит (3) | — | отчёты аудита |
| QA | (авто, финальная волна) | pre-deploy + deploy + post-deploy | — | проверенная фича |

### Одна задача (ручной контроль)

```
/do-task                       # Выполнить одну задачу с quality gates
```

### Ad-hoc кодирование (без спека)

```
/write-code                    # TDD-цикл: план → тесты → код → ревью
```

### Дизайн-пайплайн

```
/design-system-init            # Создать дизайн-систему: tokens.json + компоненты
/design-spec                   # Дизайн-спецификация через адаптивное интервью
/design-plan                   # Дизайн-план с решениями по лейаутам
/design-generate               # Генерация HTML/CSS страниц из текстовых описаний
/photo-crop                    # Расчёт object-position для фото в лейаутах
/design-review                 # Ревью UI-кода против дизайн-токенов
/design-retrospective          # Извлечь эстетические уроки, построить профиль вкуса
```

### Другие команды

| Команда | Назначение |
|---------|-----------|
| `/init-project-knowledge` | Заполнить документацию проекта через интервью |
| `/retrospective` | Извлечь уроки, обновить скиллы |
| `/done` | Финализировать фичу, обновить документацию, архивировать |

## Как это работает

### Структура проекта

```
your-project/
├── .claude/
│   └── skills/
│       └── project-knowledge/      # База знаний проекта
│           ├── SKILL.md
│           └── references/
│               ├── project.md      # Цель, аудитория, скоуп
│               ├── architecture.md # Стек, структура, модель данных
│               ├── patterns.md     # Конвенции кода, тестирование, бизнес-правила
│               └── deployment.md   # Платформа, CI/CD, мониторинг
├── work/                           # Рабочие элементы фич
│   ├── my-feature/
│   │   ├── user-spec.md           # Требования (для человека)
│   │   ├── tech-spec.md           # Архитектура (для агентов)
│   │   ├── decisions.md           # Решения, принятые при реализации
│   │   ├── tasks/                 # Атомарные файлы задач
│   │   └── logs/                  # Планы сессий, чекпоинты, отчёты ревью
│   └── completed/                 # Архив завершённых фич
├── CLAUDE.md                      # Инструкции проекта
└── README.md
```

### Глобальный фреймворк (`~/.claude/skills/`)

```
~/.claude/skills/                   # Этот репозиторий
├── skills/                        # 25+ скиллов (методология, выполнение, качество, дизайн)
├── shared/
│   ├── work-templates/            # Шаблоны для спеков, задач, сессий
│   └── design-references/         # Кросс-проектный дизайн-опыт
└── README.md
```

### Ключевые принципы

- **Spec-Driven** — пиши спеки до кода. Иерархия: User Spec → Tech Spec → Tasks → Code
- **Blocking Gates** — 6 обязательных HARD STOP в пайплайне. Ни один шаг не продолжается без явного одобрения
- **Многоуровневая валидация** — автоматические валидаторы на каждом этапе (2 → 5 → 2 → 3)
- **Планирование сессий** — волны сгруппированы по ~1200 LOC бюджету на сессию
- **Handoff сессий** — структурированный отчёт + промт для следующей сессии на каждом стопе
- **Just-In-Time Context** — агенты читают только то, что нужно для текущей задачи
- **Единая система знаний** — triad-based буфер reasoning-patterns.md, pruning, промоушен паттернов в скиллы
- **Ретроспектива** — уроки встраиваются обратно в скиллы после каждой фичи

### Архитектура агентов

Claude Code использует встроенный Agent tool со специализированными типами субагентов для параллельной работы:

**Как `/do-feature` оркестрирует:**
- Запускает агентов-воркеров на задачу (параллельно в волне)
- Запускает агентов-ревьюеров для code review (параллельно)
- Макс 3 раунда ревью на задачу
- Audit wave: 3 параллельных аудитора (code, security, test)
- Final wave: QA + deploy + post-deploy верификация

**Паттерны субагентов:**
- `/decompose-tech-spec`: `task-creator` на задачу + `task-validator` + `reality-checker`
- `/new-tech-spec`: 5 валидаторов параллельно
- `/new-user-spec`: 2 валидатора параллельно

### Скиллы

| Категория | Скиллы |
|-----------|--------|
| Планирование | user-spec-planning, tech-spec-planning, task-decomposition, project-planning |
| Выполнение | code-writing, feature-execution, pre-deploy-qa, post-deploy-qa |
| Качество | code-reviewing, security-auditor, test-master |
| Дизайн | design-system-init, design-spec, design-plan, design-generate, design-review, design-retrospective, photo-crop |
| Мета | methodology, retrospective, quick-learning, documentation-writing, skill-master, prompt-master |

Полные детали любого скилла:
```
~/.claude/skills/{skill-name}/SKILL.md
```

## Отличия от Codex-версии

Этот репо и [ai-dev-methodology-codex](https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology-codex) используют одну методологию, но отличаются интеграцией с платформой:

| Аспект | Claude Code (этот репо) | Codex |
|--------|------------------------|-------|
| Система агентов | Claude Code Agent tool | `spawn_agent`/`wait_agent`/`close_agent` |
| Конфиг | `~/.claude/settings.json` | `~/.codex/config.toml` |
| Расположение скиллов | `~/.claude/skills/` | `~/.agents/` |
| Модели | Claude (Opus/Sonnet/Haiku) | GPT-5.x тиры |
| Дизайн-пайплайн | Полный (4 скилла) | Полный (4 скилла) |
| Директория agents/ | Нет (валидаторы через Agent tool) | Да (`agents/`) |

## Основано на

Эволюционный форк [molyanov-ai-dev](https://github.com/pavel-molyanov/molyanov-ai-dev) Павла Молянова (MIT License).

## Changelog

### v1.5 — Skill Trainer: встраивание триад в скиллы (2026-04-01)

- **skill-trainer** — новый скилл для пакетного встраивания накопленных триад в целевые скиллы. Читает все триады с `Adapted: —` из triad-index.md, анализирует каждый скилл, авто-применяет правила без спорных случаев, при конфликте предлагает формулировку и ждёт решения. Команда `force-embed pattern N` — принудительное встраивание конкретной триады.
- **quick-learning** — рефакторинг ответственности: скилл больше не встраивает паттерны в скиллы при Seen ≥ 2. Только собирает триады и уведомляет при накоплении необработанных.
- **Поле Adapted** — новое поле отслеживания в triad-index.md и reasoning-patterns.md. Значения: `—` (ещё не встроена), `{skill-name}` (встроена), `n/a` (нет подходящего скилла).

### v1.4 — Единая система знаний + дизайн-пайплайн (2026-03-27)

- **Unified knowledge system** — единый буфер reasoning-patterns.md с triad-based dedup вместо разрозненных lessons-learned.md
- **Pruning trigger** — автоматическая очистка при >25 записей
- **Mechanical pre-filter** — 3+ content words в Goal = Near match candidate
- **Design categories** — design-taste, design-process, design-iteration
- **Design pipeline** — 4 скилла для UI/UX: design-system-init, design-generate, design-review, design-retrospective
