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

## Available Resources

Inventory of what's installed and ready on this machine. **Not a prescribed stack** — when starting a project, ask the user which tools to use. This list exists so that I don't suggest installing something that is already there, and don't suggest tools that are explicitly not available.

**GitHub account:** stepanenkoviktor0110-boop (via gh CLI, auth stored).

### Runtimes (verified April 2026)

- **Node.js 24.11.1** + npm 11.6.2
- **Python 3.14.3** + pip 25.3 + **uv 0.10.9** (modern Python package manager)
- **Rust 1.93.1** (rustc + cargo)
- **Docker 29.2.1**
- **Git 2.53** + **gh 2.88** (GitHub CLI)

### Utilities

- ripgrep 15.1, gitleaks 8.30, tesseract 5.4 (OCR)

### Global npm CLIs

- @anthropic-ai/claude-code, @openai/codex, @qwen-code/qwen-code, @upstash/context7-mcp, vercel

### CIP / UI Design CLI

UI design intelligence от плагина `ui-ux-pro-max` — детерминированный data-source: palette, typography, style, anti-patterns под индустрию. Шелл — PowerShell (`& "<python>" "<script>" "<query>" <flags>`).

- **Python:** `C:\Users\natel\AppData\Local\Python\bin\python.exe` (not via `uv`, not system `python` alias).
- **Script:** `C:\Users\natel\.claude\plugins\cache\ui-ux-pro-max-skill\ui-ux-pro-max\2.5.0\.claude\skills\design\scripts\cip\search.py`

Режимы: `--cip-brief -b "<Brand>"` (основной), `--domain {deliverable,style,industry,mockup} "<query>"` (точечный поиск), `--json` (машинно-парсимо).

Скиллы-потребители: code-writing, sketch, content-card, design-spec, design-plan.

### Not installed on this machine

- Bun, pnpm, yarn — alternative Node package managers
- poetry — Python package manager (uv is used instead)
- Go, .NET SDK
- Database clients (psql, mysql, sqlite3 CLI) — if a DB is needed, run it in Docker

**Behaviour:** don't suggest tools from this list without first asking the user whether to install them.

### Experienced across projects

The user has projects in: Next.js + Prisma + PostgreSQL, Vite + React, Fastify + grammy (Telegram bots) + better-sqlite3, Python via uv with Flask/requests/gspread, plain Node scripts. Assume familiarity with any of these without extra explanation.
