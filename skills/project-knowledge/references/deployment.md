# Deployment & Operations

## Purpose
How the methodology is distributed, installed, and updated.

---

## Deployment Model

**Platform:** GitHub + local git clone

**Type:** Not a deployed application. The methodology is installed by cloning the repo into `~/.claude/skills/`. Updates arrive via `git pull`.

**Why:** Claude Code reads skill files from `~/.claude/skills/` at runtime. Cloning the repo directly into that location makes all skills immediately available with no additional setup.

---

## Distribution

**GitHub repo:** `https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology`

**Install:** clone `stepanenkoviktor0110-boop/ai-dev-methodology` into `~/.claude/skills`.

**Update:** run `git pull origin master` from `~/.claude/skills`. Auto-checked on first pipeline command per session (RULE #0 in CLAUDE.md).

---

## Codex Variant

**GitHub repo:** `https://github.com/stepanenkoviktor0110-boop/ai-dev-methodology-codex`

**Local clone:** `C:/tmp/ai-dev-methodology-codex/`

**Install (Codex):** clone `stepanenkoviktor0110-boop/ai-dev-methodology-codex` into `~/.agents/skills`.

---

## Update Workflow

1. Edit skill files directly in `~/.claude/skills/`
2. `git add -A && git commit -m "..."` from `~/.claude/skills/`
3. `git push origin master` → available to all installs on next `git pull`
4. Codex adaptation: manually diff changed skills, apply `.claude/` → `.agents/` substitution, push to Codex repo

---

## Environments

**Production:** `~/.claude/skills/` on developer's machine — this is what Claude uses daily.

---

## Monitoring

No automated monitoring. Verification is manual: invoke a skill after changes, observe behavior matches intent.
