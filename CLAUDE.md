# Global Preferences

## ⛔ CRITICAL — NEVER skip this rule

**NEVER generate multiple artifacts without stopping for user review.** For EVERY artifact (code, config, spec, agent, skill, template): generate ONE block → list controversial points → explain each in simple terms → STOP and WAIT for user decision → apply fixes → ONLY THEN proceed to next block. This applies to ALL workflows without exception. Violation of this rule means the output is rejected.

## ⛔ RULE #0: Methodology Update — Manual Only
Only check for methodology updates when the user explicitly runs `/update-methodology`.
DO NOT run automatically at session start.

## ⛔ RULE #1: Single Source of Truth

**`~/.claude/skills/` — единственный source of truth для всех знаний методологии.**

All writes — lessons-learned (retrospective), reasoning-patterns (quick-learning), triad-index, quick-ref — go to `~/.claude/skills/` and nowhere else. After writing, commit and push to origin.

- `$AGENTS_HOME = ~/.claude/skills` — every skill that references `$AGENTS_HOME` writes HERE.
- No copies in `c:/tmp/` or other locations. If a separate platform (Codex) uses its own repo — it has its own knowledge base. Cross-sync is manual and explicit.
- After `/retrospective` or `/quick-learning` writes files → `cd ~/.claude/skills && git add -A && git commit && git push origin master`.

## ⛔ RULE #2: NEVER Leak Secrets

**NEVER output contents of .env, credentials, tokens, passwords, API keys, or any secrets.** This applies to ALL contexts — diagnostics, debugging, deployment, any SSH commands.

- **NEVER** run `cat .env`, `grep PASSWORD`, `echo $DATABASE_URL` or any command that could print secrets
- To check a variable exists: `grep -c VARIABLE_NAME .env` (returns count, not value)
- To show masked value: `sed 's/:[^@]*@/:***@/g'` or similar masking
- If you accidentally output a secret: **immediately** rotate it, don't just apologize

Violation = credentials compromised, requires emergency rotation.

## Communication
- Общаться с пользователем только по-русски. Код, команды и технические термины — на английском, сопроводительный текст — по-русски.

## Quick Learning
- Запускать только по явному запросу: `/quick-learning` или "быстрый анализ".
- Можно вызвать вручную в любой момент: `/quick-learning` или "быстрый анализ", "что улучшить в процессе".

## Work Style
- Границы сессий определяются автоматически из `session-plan.md` (генерируется при `/decompose-tech-spec`). После завершения сессии feature-execution генерирует промт для следующей сессии. Не запускать следующую сессию автоматически.
- После завершения каждого этапа: проверить документацию, зафиксировать шаги, дать рекомендацию начать новую сессию с конкретным промтом для копирования.
- Сначала искать ответы в документации проекта (project knowledge, backlog, code-research, skills), не спрашивать пользователя то, что можно найти самостоятельно.
