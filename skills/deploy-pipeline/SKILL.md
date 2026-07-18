---
name: deploy-pipeline
description: |
  Sets up CI/CD pipelines, deployment configuration, and automated deploy workflows.
  GitHub Actions, platform-specific deploy (Vercel, Railway, Fly.io, AWS, VPS),
  secrets management in CI.

  Use when: "подготовь деплой", "настрой автодеплой", "настрой CI/CD",
  "setup deploy", "configure deployment", "настрой пайплайн",
  "безопасный деплой", "деплой запинается", "preflight", "откат деплоя",
  "safe deploy", "deploy keeps breaking", "rollback"
---

# Deploy Pipeline

## Gathering Deployment Context

Read project-knowledge to understand the deployment target:
- `.claude/skills/project-knowledge/references/deployment.md`
- `.claude/skills/project-knowledge/references/architecture.md`
- `.claude/skills/project-knowledge/references/patterns.md`

If deployment target is not documented, ask the user:
- Target platform (Vercel, Railway, Fly.io, AWS ECS, VPS, NPM, Chrome Web Store)
- Environment details (URLs, project/service IDs, server access)
- Required secrets and where to obtain them

After gathering answers, immediately update `deployment.md` before proceeding with setup.

## CI/CD Convention

Create `.github/workflows/ci.yml` following this structure:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check-skip:
    runs-on: ubuntu-latest
    outputs:
      should_skip: ${{ steps.check.outputs.should_skip }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - id: check
        run: |
          FILES=$(git diff --name-only HEAD~1 HEAD 2>/dev/null || git diff --name-only HEAD)
          if echo "$FILES" | grep -vqE '\.(md|txt)$|^\.claude/|^\.spec/|^docs/'; then
            echo "should_skip=false" >> $GITHUB_OUTPUT
          else
            echo "should_skip=true" >> $GITHUB_OUTPUT
          fi

  test:
    needs: check-skip
    if: needs.check-skip.outputs.should_skip != 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # setup, install, lint, type-check, test, build

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # platform-specific deploy action
```

Adapt: add language setup, install steps, platform-specific deploy action.

## Platform Selection

| Platform | Choose when |
|----------|------------|
| Vercel | Next.js, React, static sites, serverless |
| Railway | Full-stack apps needing managed DB |
| Fly.io | Docker containers, global edge |
| AWS ECS | Enterprise, full infrastructure control |
| Custom VPS | Persistent sessions, multi-device |
| NPM | Node.js packages or CLI tools |
| Chrome Web Store | Browser extensions |

For VPS deployments: server-specific details (IPs, SSH keys, paths) go to `deployment.md`.

## Secrets Convention

Document all required secrets in `.claude/skills/project-knowledge/references/deployment.md`. For each secret:
- Name (GitHub Actions key)
- Where to obtain value (dashboard URL or CLI command)
- Which workflow uses it

Guide user to add secrets in GitHub repository settings. Create `.env.example` with application-level variable names.

## Documentation Updates

After configuring, update project-knowledge references. Append to existing content.

**deployment.md:** deploy target, pipeline overview, required secrets table, manual deploy command, rollback steps.

**patterns.md (Git Workflow section):** CI triggers, pipeline jobs, skip logic pattern, PR workflow.

## Decision Framework

- **Add deploy job:** yes when deployment target defined, user requests it, main is stable. No for early development, manual-deploy preference, or platforms requiring manual review (Chrome Web Store).
- **Matrix strategy:** yes for NPM packages and cross-platform libraries. No for single-environment apps and internal tools.
- **Staging environment:** yes when a dev branch exists or multi-developer team. No for solo + main-only (Vercel preview deploys are sufficient).

---

# Deploy Safety (universal mechanism)

Stops the recurring class of "a small thing breaks the deploy" (`&` in the wrong place, bad
YAML/nginx, malformed env value, wrong feed, a forgotten manual step) on **any** project, without
per-project hand-coding. It works by knowing artifact *classes* generically and auto-detecting a
repo's instances of them. Full model + rationale: [references/artifact-registry.md](references/artifact-registry.md).

## Parts

- **[references/artifact-registry.md](references/artifact-registry.md)** — the universal taxonomy (7 MVP classes: compose, env-schema, shell, static-config, migration, reverse-proxy, runtime-behavior), each with a detector, a generic validator, and lifecycle wiring. Logic written **once**.
- **[scripts/probe.py](scripts/probe.py)** — scans a repo, writes `deploy-manifest.yml` (which classes present, where, project params). One-time per project; re-run when the deploy surface changes.
- **[scripts/preflight.py](scripts/preflight.py)** — maps the release diff to classes and runs **only the touched** validators (`--all` in CI). Built-in checks first; a class whose external tool is absent is skipped with a notice (`optional`).
- **[scripts/deploy.sh](scripts/deploy.sh)** — the atomic, rollback-able spine: preflight → push → backup → tag `:prev` → build+recreate → health-gate → smoke → **auto-rollback on any failure**. Generalizes a hand-written deploy script; adds the `:prev` tag + health gate + rollback most scripts lack.
- **[scripts/smoke.py](scripts/smoke.py)** — deterministic post-deploy anchor check (asserts a substring only correct data produces). No LLM, so it can safely gate an automatic rollback.

## Onboarding a project (once)

1. `python probe.py --repo <repo>` → generates `deploy-manifest.yml`. Commit it.
2. Fill the three things the probe can't infer:
   - `spine.services` — the compose services to recreate atomically (manifest).
   - target host / dir / health URL — these are **`deploy.sh` args** (`--ssh`, `--dir`, `--health-url`), not manifest fields, since they belong to the deploy *target*, not the repo.
   - `classes.runtime-behavior.checks[]` — per externally-facing service: `url`, `request`, and
     `expect_substring` (auto-derive the token from seed data / project-knowledge first; interview
     only if underivable). `spine.backup_cmd` — backup command to run before mutation, if any.
3. Re-run `probe.py --force` whenever the deploy surface changes (new compose/nginx/seed/migration).

## CI wiring (the "tests exist before deploy" half)

Add a preflight step to the test workflow so every PR validates the full deploy surface:

```yaml
  - name: deploy preflight
    run: python .../preflight.py --repo . --all
```

This makes the safety checks exist and run **before** anything reaches the deploy branch — the
change-scoped subset then re-runs at deploy time via `deploy.sh` step 0.

## Plan-time gate ("tests in advance")

When decomposing a tech-spec (`decompose-tech-spec`): if a task edits a file of class X, note the
class-X validator as one of its acceptance checks. This is a lightweight convention — the CI
`preflight --all` is the actual enforcement, so do **not** rewire the task generator for it.

## Deploying

```bash
python .../preflight.py --repo . --diff-base <live-ref>     # local gate (or rely on deploy.sh step 0)
bash  .../deploy.sh --ssh HOST --dir /remote/repo --branch BR \
      --manifest deploy-manifest.yml --health-url URL [--diff-base REF] [--dry-run]
```

`--dry-run` prints the full plan (preflight, push, remote build/recreate/health/rollback, smoke)
without touching prod — use it to review a new project's wiring before the first real deploy.

## Growing it

Add a class to the registry only when a real incident exposes a deploy-breaking artifact it
doesn't cover (schema fields + a built-in-first validator; external tools always `optional`).
Record the motivating incident in the entry.
