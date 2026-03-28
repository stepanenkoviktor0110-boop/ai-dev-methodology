---
description: |
  Remove all traces of AI-assisted development before delivering project to external client.
  Audits files, git history, code comments. Cleans with user confirmation at each step.

  Use when: "очистить следы", "clean delivery", "замаскировать AI",
  "подготовить к передаче заказчику", "prepare for client delivery"

  NEVER auto-trigger. Manual invocation only.
---

# Clean Delivery — Remove AI Pipeline Traces

## Prerequisites

- Project must be a git repository
- User must have confirmed this is for external client delivery
- All feature work should be completed and committed before running
- Check `git-filter-repo` availability: `git filter-repo --version 2>/dev/null`
  - If missing → install: `pip install git-filter-repo`
  - If pip unavailable → abort with message: "Install git-filter-repo: https://github.com/newren/git-filter-repo#how-do-i-install-it"

**CRITICAL — git-filter-repo removes remote origin.** Always save before running:
```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
```
Re-add after filter-repo completes:
```bash
git remote get-url origin 2>/dev/null || git remote add origin "$REMOTE_URL"
```
This applies to Steps 2.4 and 2.5. Warn user about this before starting cleanup.

## Step 1: Audit — Scan for AI Traces

Run a comprehensive scan and present findings to user. Do NOT modify anything yet.

### 1.1 File System Traces

Scan for these paths (relative to project root):
```
.claude/
CLAUDE.md
work/
.pytest_cache/README.md
```

Check existence with `ls` / `test -d` / `test -f`. Report which exist.

### 1.2 Git-Tracked Pipeline Artifacts

```bash
git ls-files | grep -iE '\.claude/|CLAUDE\.md|^work/'
```

Report any tracked files that should be removed from index.

### 1.3 Git History — Co-Authored-By

```bash
git log --all --format='%H %s' | head -200
git log --all --grep='Co-Authored-By' --format='%H %s'
git log --all --grep='[Cc]laude' --format='%H %s'
git log --all --grep='[Aa]nthropic' --format='%H %s'
```

Count commits with AI attribution. Report total.

### 1.4 Git History — Pipeline Commit Patterns

Search for these patterns in commit messages:
```
wave [0-9]
session.plan
draft(techspec)
draft(userspec)
chore(tasks)
chore(techspec)
validation round
user-spec interview
quick-learning
retrospective
feat(wave
docs: update project knowledge after
```

```bash
git log --all --format='%H %s' | grep -iE 'wave [0-9]|session.plan|draft\(techspec\)|draft\(userspec\)|chore\(tasks\)|chore\(techspec\)|validation.round|user-spec.interview|quick-learning|retrospective|feat\(wave|docs: update project knowledge after'
```

### 1.5 Code Comments — Dynamic Source Detection

Detect source directories dynamically:
```bash
# Find directories containing source code (exclude node_modules, .git, venv, etc.)
SOURCE_DIRS=$(find . -maxdepth 2 -type f \( -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.tsx' -o -name '*.jsx' -o -name '*.go' -o -name '*.rs' -o -name '*.java' \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/venv/*' -not -path '*/__pycache__/*' \
  | xargs -I{} dirname {} | sort -u)
```

Then scan detected directories:
```bash
grep -rn -iE 'claude|anthropic|AI.generated|LLM.generated' $SOURCE_DIRS \
  --include='*.py' --include='*.ts' --include='*.js' --include='*.tsx' --include='*.jsx' \
  --include='*.go' --include='*.rs' --include='*.java' 2>/dev/null
```

Exclude false positives (e.g., `claude` as a person name, `llm` as part of a variable in AI projects).

### 1.6 Present Audit Report

Format findings as a table:

```
## Audit Report

| Category              | Found | Details                          |
|-----------------------|-------|----------------------------------|
| Pipeline files        | 3     | .claude/, CLAUDE.md, work/       |
| Tracked artifacts     | 12    | .claude/skills/..., work/...     |
| Co-Authored-By        | 47    | commits with AI attribution      |
| Pipeline messages     | 8     | wave, draft(techspec), ...       |
| Code comments         | 0     | none found                       |
```

Ask user: **"Proceed with cleanup? This will rewrite git history (git filter-repo). Make sure you have a backup or the remote is the backup."**

Wait for confirmation before proceeding.

## Step 2: Cleanup — With User Confirmation Per Sub-Step

### 2.1 Update .gitignore

Ask user: "Add .claude/, CLAUDE.md, work/ to .gitignore?"

If confirmed:
- Read current `.gitignore` (or create if missing)
- Append these lines (if not already present):

```
# Pipeline artifacts
.claude/
CLAUDE.md
work/
```

### 2.2 Remove Pipeline Artifacts from Git Index

Ask user: "Remove tracked pipeline artifacts from git index? (files stay on disk, just untracked)"

If confirmed:
```bash
git rm -r --cached .claude/ 2>/dev/null
git rm --cached CLAUDE.md 2>/dev/null
git rm -r --cached work/ 2>/dev/null
git rm --cached .pytest_cache/README.md 2>/dev/null
```

Commit:
```bash
git commit -m "chore: update gitignore"
```

### 2.3 Clean Code Comments

If Step 1.5 found AI-related comments — show each one to user and ask whether to remove.
Apply edits only for confirmed removals.

If changes made, commit:
```bash
git commit -m "chore: clean up comments"
```

### 2.4 Rewrite Git History — Co-Authored-By

Ask user: **"Rewrite git history to remove Co-Authored-By lines? This uses git-filter-repo and is destructive. WARNING: filter-repo will remove remote origin — it will be restored automatically after. Confirm?"**

**Before running: save remote URL** (see Prerequisites CRITICAL note).

If confirmed, identify all branches to rewrite:
```bash
BRANCHES=$(git branch --format='%(refname:short)')
```

Ask user which branches to process (show full list). Then:

```bash
git filter-repo --message-callback '
  import re
  lines = message.decode("utf-8").split("\n")
  lines = [l for l in lines if not re.search(r"Co-Authored-By.*(?i)(claude|anthropic|noreply@anthropic)", l)]
  return "\n".join(lines).encode("utf-8")
' --refs refs/heads/branch1 refs/heads/branch2 --force
```

**Important:** `git filter-repo` removes the remote origin by default. After running, re-add it:
```bash
git remote add origin <REMOTE_URL>
```

Save the remote URL BEFORE running filter-repo:
```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
```

### 2.5 Rewrite Git History — Pipeline Commit Messages

Ask user: **"Rewrite suspicious commit messages to neutral ones? Confirm?"**

**Reminder: if Step 2.4 already ran filter-repo, remote origin was removed. It will be restored in Step 2.6.**

Apply message rewriting:

```bash
git filter-repo --message-callback '
  import re
  msg = message.decode("utf-8")
  replacements = [
    (r"(?i)wave ([0-9]+)", r"phase \1"),
    (r"(?i)session.plan", "schedule"),
    (r"(?i)draft\(techspec\)", "chore"),
    (r"(?i)draft\(userspec\)", "chore"),
    (r"(?i)chore\(tasks\)", "chore"),
    (r"(?i)chore\(techspec\)", "chore"),
    (r"(?i)validation.round", "review"),
    (r"(?i)user-spec.interview", "requirements gathering"),
    (r"(?i)user-spec", "requirements"),
    (r"(?i)tech-spec", "design"),
    (r"(?i)quick-learning", "notes"),
    (r"(?i)feat\(wave([0-9]+)\)", "feat"),
    (r"(?i)docs: update project knowledge after", "docs: update documentation for"),
    (r"(?i)retrospective", "review"),
  ]
  for pattern, repl in replacements:
    msg = re.sub(pattern, repl, msg)
  return msg.encode("utf-8")
' --refs refs/heads/branch1 refs/heads/branch2 --force
```

**Note:** If Step 2.4 already removed origin, skip re-adding. If both steps run, they share the same filter-repo session state.

### 2.6 Restore Remote & Cleanup Git Internals

**CRITICAL: filter-repo removes remote origin. Restore it now.**
```bash
# Verify remote was saved in Prerequisites step
echo "Restoring remote: $REMOTE_URL"
git remote get-url origin 2>/dev/null || git remote add origin "$REMOTE_URL"
# Verify restoration
git remote -v
```

If `$REMOTE_URL` is empty (was never saved), ask user for the remote URL manually.

```bash
# Cleanup git internals
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 2.7 Force Push

Ask user: **"Force push rewritten history to remote? List branches to push. THIS CANNOT BE UNDONE on remote."**

Show exact commands that will run:
```bash
git push --force origin branch1 branch2 ...
```

Only execute after explicit confirmation.

## Step 3: Verification

Run post-cleanup checks:

```bash
# Check git history
git log --all --format='%s' | grep -icE 'claude|anthropic|co-authored|wave [0-9]|session.plan|draft\(|chore\(tasks|chore\(techspec|quick-learning|retrospective|user-spec'

# Check tracked files
git ls-files | grep -iE '\.claude|CLAUDE|^work/'

# Check file system
ls -la .claude/ CLAUDE.md work/ 2>/dev/null

# Check code comments (use same dynamic source detection as Step 1.5)
grep -rn -iE 'claude|anthropic' $SOURCE_DIRS \
  --include='*.py' --include='*.ts' --include='*.js' --include='*.tsx' --include='*.jsx' \
  --include='*.go' --include='*.rs' --include='*.java' 2>/dev/null
```

### Verification Report

```
## Verification Report

| Check                    | Status | Details                   |
|--------------------------|--------|---------------------------|
| Git history clean        | pass/fail | N suspicious commits left |
| No tracked artifacts     | pass/fail | files still in index      |
| Code comments clean      | pass/fail | N comments remaining      |
| .gitignore updated       | pass/fail | patterns added            |
```

If anything remains — ask user if they want to address it manually or accept.

## Step 4: Deploy Check (Optional)

If `deploy.sh`, `.github/workflows/`, `Dockerfile`, or similar CI/CD config exists:

1. Ask user: "Redeploy with cleaned history? This ensures the server has no AI traces."
2. If deploy is SCP-based (no .git on server) — confirm it's already clean.
3. If deploy is git-based — remind user that force-push was needed (Step 2.7).

## Step 5: Pre-Commit Hook (Optional)

Ask user: "Install a pre-commit hook to prevent future AI traces from being committed?"

### Option A: .pre-commit-config.yaml (if pre-commit framework detected)

If `.pre-commit-config.yaml` exists, add a local hook:

```yaml
  - repo: local
    hooks:
      - id: block-ai-artifacts
        name: Block AI pipeline artifacts
        entry: bash -c 'if git diff --cached --name-only | grep -qE "^\.claude/|^CLAUDE\.md"; then echo "ERROR: pipeline artifact staged"; exit 1; fi'
        language: system
        always_run: true
      - id: block-ai-commit-msg
        name: Block AI patterns in commit messages
        entry: bash -c 'if grep -qiE "Co-Authored-By.*(claude|anthropic)|wave [0-9]|draft\(techspec\)|session.plan|quick-learning" "$1"; then echo "ERROR: AI pattern in commit message"; exit 1; fi'
        language: system
        stages: [commit-msg]
```

### Option B: Raw git hooks (no pre-commit framework)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Block AI pipeline traces from being committed

STAGED=$(git diff --cached --name-only)

if echo "$STAGED" | grep -qE '^\.claude/|^CLAUDE\.md'; then
  echo "ERROR: Attempting to commit pipeline artifact (.claude/ or CLAUDE.md)"
  echo "These files should stay in .gitignore"
  exit 1
fi

exit 0
```

Create `.git/hooks/commit-msg`:

```bash
#!/bin/bash
# Block AI attribution and pipeline patterns in commit messages

MSG=$(cat "$1")

if echo "$MSG" | grep -qiE 'Co-Authored-By.*(claude|anthropic)'; then
  echo "ERROR: Commit message contains AI attribution (Co-Authored-By)"
  exit 1
fi

if echo "$MSG" | grep -qiE 'wave [0-9]|draft\(techspec\)|draft\(userspec\)|chore\(tasks\)|chore\(techspec\)|session.plan|quick-learning'; then
  echo "ERROR: Commit message contains pipeline patterns"
  echo "Rewrite the message to use neutral terms"
  exit 1
fi

exit 0
```

Make hooks executable:
```bash
chmod +x .git/hooks/pre-commit .git/hooks/commit-msg
```

## Idempotency

This skill is safe to run multiple times:
- .gitignore additions check for duplicates before appending
- `git rm --cached` on untracked files is a no-op (exits with warning, not error)
- filter-repo on already-clean history produces no changes
- Verification step confirms current state regardless of prior runs
- Pre-commit hooks overwrite cleanly

## Self-Verification

- [ ] git-filter-repo installed and available
- [ ] Audit completed — all trace categories scanned
- [ ] User confirmed before each destructive step
- [ ] .gitignore updated with pipeline patterns
- [ ] Pipeline artifacts removed from git index
- [ ] Code comments cleaned (if any found)
- [ ] Git history rewritten — no Co-Authored-By with Claude/Anthropic
- [ ] Git history rewritten — no pipeline commit message patterns
- [ ] Remote origin restored after filter-repo
- [ ] Git internals cleaned (reflog, gc)
- [ ] Force push completed (if user confirmed)
- [ ] Verification report shows all clean
- [ ] Deploy check offered (if CI/CD exists)
- [ ] Pre-commit hook offered (both framework and raw variants)
