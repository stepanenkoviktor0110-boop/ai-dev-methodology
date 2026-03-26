# Global Preferences

## ⛔ RULE #0: Auto-Update Before Any Pipeline Step

**Before running ANY skill command** (`/new-user-spec`, `/new-tech-spec`, `/decompose-tech-spec`, `/do-feature`, `/do-task`, `/retrospective`, `/done`, `/design-system-init`, `/design-generate`, `/design-review`, `/design-retrospective`, `/init-project`, `/init-project-knowledge`, `/write-code`, `/pre-deploy-qa`, `/post-deploy-qa`), the agent MUST check for methodology updates.

**This check is MANDATORY and runs ONCE per session** (not before every command — just the first pipeline command in the session). After the first check, set a mental flag "methodology_checked = true" and skip on subsequent commands within the same session.

```bash
cd ~/.claude/skills && git fetch origin master --quiet && git diff HEAD origin/master --stat
```

- If diff is non-empty → run `git pull origin master` and report: "Методология обновлена: {N} файлов изменено." New skills become available on the next user message.
- If diff is empty → proceed silently (no message needed).
- If fetch fails (no internet, auth error) → warn user: "Не удалось проверить обновления методологии. Продолжаю с текущей версией." and proceed.

**Important:** `~/.claude/skills/` IS the methodology repo clone. `git pull` there updates everything — skills, agents, templates. No manual copying needed.

## Communication
- Общаться с пользователем только по-русски. Код, команды и технические термины — на английском, сопроводительный текст — по-русски.

## Quick Learning
- Скилл `quick-learning` запускается автоматически (как фоновый субагент) перед каждым session break в `/do-feature` и `/do-task`.
- Можно вызвать вручную в любой момент: `/quick-learning` или "быстрый анализ", "что улучшить в процессе".

## Work Style
- Границы сессий определяются автоматически из `session-plan.md` (генерируется при `/decompose-tech-spec`). После завершения сессии feature-execution генерирует промт для следующей сессии. Не запускать следующую сессию автоматически.
- После завершения каждого этапа: проверить документацию, зафиксировать шаги, дать рекомендацию начать новую сессию с конкретным промтом для копирования.
- Сначала искать ответы в документации проекта (project knowledge, backlog, code-research, skills), не спрашивать пользователя то, что можно найти самостоятельно.
