---
name: safe-delete
description: |
  Pre-delete project audit: verify git sync, docs, VPS state, kill local processes.
  On-demand only — invoke manually before deleting a project from local machine.

  Use when: "safe-delete", "можно удалять?", "проверь перед удалением",
  "подготовь к удалению", "удалить проект", "prepare for deletion"
---

# Safe Delete — Pre-Deletion Project Audit

Verdict: **READY** (can delete) or **BLOCKED** (fix first). Only kills processes on LOCAL machine.

## Step 1: Git Sync

Run `git status`, `git log origin/<branch>..HEAD`, `git remote -v` in parallel.

| Check | BLOCKED if | WARNING if |
|-------|-----------|------------|
| Uncommitted changes | any exist | — |
| Unpushed commits | any exist | — |
| Remote reachable | fetch fails | — |
| Untracked files | — | any exist (will be LOST) |

If untracked files found — list each one, warn about permanent loss, **wait for user confirmation** before continuing.

## Step 2: Documentation

Read CLAUDE.md → find `project-knowledge/references/` path. Check each `.md` file: exists, not empty, no TODO/TBD/FIXME placeholders. Report: `N docs checked, all complete` or list gaps.

## Step 3: Remote/VPS (if applicable)

Read CLAUDE.md for SSH host, app path, domain. If none found → skip, note "No remote configured."

| Check | How | BLOCKED if |
|-------|-----|-----------|
| App online | `pm2 list` via SSH | process not online or uptime=0 |
| Code sync | compare `git log -1` on VPS vs origin HEAD | VPS behind origin |
| SSL | `certbot certificates` via SSH | invalid or expiry < 14 days |
| HTTP | `curl -s -o /dev/null -w '%{http_code}'` the domain | not 200 |
| DB | `psql -c 'SELECT 1'` via SSH | connection fails |

**CRITICAL:** Never output .env values, DB contents, or PII. Only check connectivity.

## Step 4: Kill Local Processes

Find processes whose command line contains the project directory path. Kill dev servers, node, file watchers, test runners. Platform-aware: `wmic`/`taskkill` on Windows, `ps`/`kill` on Unix. Report: `Killed N processes` or `No running processes found`.

## Step 5: Verdict

```
=== SAFE DELETE AUDIT ===
Git:        OK | BLOCKED (reason)
Docs:       OK (N files) | WARNING (gaps)
VPS:        OK | BLOCKED (reason) | SKIPPED
Untracked:  CLEAN | WARNING (N files lost)
Processes:  KILLED (N) | CLEAN
VERDICT:    READY | BLOCKED
```

If READY → `git clone <remote-url>` to restore later.
If BLOCKED → list each blocker with fix command.
