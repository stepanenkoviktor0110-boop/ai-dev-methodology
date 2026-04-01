---
name: progress
description: |
  Generates an AI summary of project progress from local files and posts it
  to the dashboard backend API. Reads git log, checkpoint.yml, task files,
  and decisions.md to build a 2–3 sentence Russian summary, then POSTs the
  full progress record to /api/progress.

  Use when: "/progress", "отправь прогресс", "обнови прогресс", "синхронизируй прогресс", "progress update", "запиши прогресс"
---

# Progress Reporter

Reports project progress to the freelance dashboard. Reads local project state, generates a short Russian summary, and sends it to the backend API.

## Phase 1: Read Local Context

1. Run `git log --oneline -30` to get recent commit titles.
2. Run `git log --format="%ci" -1` to get the most recent commit date (needed for `last_commit_days`).
3. Glob `work/*/logs/checkpoint.yml` — pick the most recently modified file. Read it to extract `last_completed_wave` and `total_waves`.
4. Glob `work/*/tasks/*.md` — from the most recently modified feature directory, read task files to understand what is done and in progress (check `status:` in frontmatter).
5. Glob `work/*/decisions.md` — from the most recently modified feature directory, read key decisions.

If the `work/` directory is absent or contains no matching files — note this and continue. The skill still works without work/ data (progress_percent will be null).

**Checkpoint:** Git log retrieved. Checkpoint file read (or noted as absent). Task statuses and decisions collected (or noted as absent).

## Phase 2: Generate Summary

Based on the collected context (git log, checkpoint, tasks, decisions), write a 2–3 sentence summary in Russian:
- First sentence: what was completed recently (reference specific tasks or features).
- Second sentence: what is currently in progress or planned next.
- Keep it factual and concise — no filler phrases.

Example tone: "Реализован бэкенд API с тремя эндпоинтами и 28 тестами. Сейчас в работе фронтенд-колонка прогресса и скрипт синхронизации."

**Checkpoint:** Summary is 2–3 sentences, in Russian, references concrete work items.

## Phase 3: Build Payload

1. Read `~/.claude/dashboard.json`. If the file is missing, show this message and stop:
   ```
   Создайте ~/.claude/dashboard.json с полями api_url, api_key
   ```
   Extract `api_url` and `api_key` from the file.

2. Run `git remote get-url origin` to get `repo_url`. If git remote is not configured, show this message and stop:
   ```
   Репозиторий не привязан к GitHub. Настройте git remote origin.
   ```

3. Compute `last_commit_days`:
   - Parse the date from `git log --format="%ci" -1` (ISO format).
   - Calculate: `Math.floor((Date.now() - commitDate) / 86400000)`.
   - If git log returned no commits — set to `null`.

4. Compute `progress_percent`:
   - From checkpoint.yml: `Math.round(last_completed_wave / total_waves * 100)`.
   - If checkpoint.yml is absent, or `total_waves` is 0 or missing — set to `null`.

5. Set `updated_at` to the current ISO timestamp: `new Date().toISOString()`.

6. Assemble the payload:
   ```json
   {
     "repo_url": "<from git remote>",
     "last_commit_days": "<computed>",
     "progress_percent": "<computed or null>",
     "updated_at": "<ISO timestamp>",
     "summary": "<generated summary>"
   }
   ```

**Checkpoint:** Payload assembled with all 5 fields. `api_url` and `api_key` extracted.

## Phase 4: POST to API

1. Run this curl command (substitute values):
   ```bash
   curl -s -w "\n%{http_code}" -X POST "{api_url}/api/progress" \
     -H "Content-Type: application/json" \
     -H "X-Api-Key: {api_key}" \
     -d '{payload_json}'
   ```

2. Check the HTTP status code in the response:
   - **2xx** — report success. Show the summary that was sent.
   - **Non-2xx** — show the HTTP status code and response body. Do not silently ignore errors.

**Checkpoint:** POST sent. Response status shown to user (success or error with details).

## Final Check

Before finishing, verify:
- [ ] Summary is 2–3 sentences in Russian, references concrete work
- [ ] Payload contains all 5 fields (repo_url, last_commit_days, progress_percent, updated_at, summary)
- [ ] POST response status was shown to the user
- [ ] Errors (missing config, missing remote, failed POST) were reported clearly
