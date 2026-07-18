# Artifact Registry — universal deploy-safety taxonomy

The cross-project knowledge that makes deploy-safety work on **any** repo without per-project
hand-coding. Logic lives here (once); project-specifics live in a generated `deploy-manifest.yml`
(see [probe](../scripts/probe.md)). The [runner](../scripts/runner.md) reads both.

## How the three pieces fit

- **Registry (this file)** — a fixed taxonomy of *artifact classes*. A class is anything a
  small mistake can break at deploy time and that recurs across projects (a compose file is a
  compose file in every dockerized project). Each class carries a **detector**, a **generic
  validator**, and the wiring for the two lifecycle hooks below.
- **Probe** — walks a repo, runs each class detector, writes `deploy-manifest.yml`: which
  classes are present, where, and the project-specific params (health URL, service list,
  anchor checks). One-time per project; re-run when the deploy surface changes.
- **Runner** — at **plan time** attaches a class's validator to a task as an acceptance gate
  when the task touches that class ("tests in advance"); at **deploy time** runs only the
  validators whose `scope-trigger` matches the release diff ("run only what changed"), then the
  always-on **atomic-switch spine**.

Universality comes from separation of levels: the **rows (classes) and lifecycle phases are
project-independent**; only the *instances* (paths, params) are project-derived by the probe.

## Class entry schema

Every class is described with the same fields — this uniformity is what lets the probe and
runner treat all classes generically:

| field | meaning |
|-------|---------|
| `class` | stable id, used as the manifest key |
| `detect` | globs / heuristics the probe uses to find instances (project-independent) |
| `validate` | the generic check command; must work on **any** instance of the class |
| `phase` | when it runs: `pre-deploy` \| `switch` \| `post-deploy` |
| `scope-trigger` | git-diff path globs that activate this validator at deploy (selectivity) |
| `plan-gate` | when `decompose-tech-spec` attaches it as a task acceptance gate (advance) |
| `prevents` | the failure class it kills |
| `manifest` | project-specific fields the probe writes for this class |

`validate` commands assume Docker is available (used as the universal, install-free runtime for
any external tool) and otherwise use only built-ins. A class whose external tool is absent and
has no built-in fallback is recorded by the probe as `optional: true` and skipped with a logged
notice rather than failing the run — the atomic-switch spine is the safety net for those.

## MVP classes (7)

### 1. `container-compose`
- **detect:** `docker-compose*.y{a,}ml`, `compose*.y{a,}ml` at repo root or `deploy/`
- **validate:** `docker compose -f <file> config -q` (parses YAML + resolves interpolation/env refs)
- **phase:** pre-deploy · **scope-trigger:** `docker-compose*.yml`, `compose*.yml`, `.env`
- **plan-gate:** task edits a compose file
- **prevents:** YAML/indent errors, misplaced `&`, unresolved `${VAR}`, bad service refs
- **manifest:** `files: []` (compose paths)

### 2. `env-schema`
- **detect:** a settings module (e.g. `**/config.py` defining pydantic `Settings`, or `env.ts`
  schema) **and** an `.env.example`
- **validate:** two checks — (a) *presence*: every required key (no-default setting) exists on
  the target env, by NAME only, never reading values; (b) *value-validity*: instantiate the
  settings object against the target env and catch the framework's validation error
- **phase:** pre-deploy · **scope-trigger:** `**/config.py`, `.env*`, settings-schema files
- **plan-gate:** task adds/changes a required setting
- **prevents:** missing env key (boot crash) **and** malformed value (e.g. secret too short)
- **manifest:** `settings_loader:` (command that imports settings), `required_extractor:`
  (how to list required keys — reuse the AST approach of `check-deploy-env.py`), `target_env:`
  (`local:<path>` or `ssh:<host>:<path>`)

### 3. `shell-script`
- **detect:** `deploy/*.sh`, `docker/*entrypoint*.sh`, `scripts/*.sh`, any file with a `#!.*sh` shebang
- **validate:** `bash -n <file>` (syntax parse — catches the real `&`/quote/`fi`/heredoc class for free); `shellcheck` additionally **iff** available (`optional`)
- **phase:** pre-deploy · **scope-trigger:** `**/*.sh`
- **plan-gate:** task edits a shell script
- **prevents:** misplaced `&`, unbalanced quotes/`fi`/`done`, broken heredoc
- **manifest:** `files: []` (discovered scripts)

### 4. `static-config`
- **detect:** deploy-data files — `**/seed/**/*.{json,yml,yaml}`, declared config data
  (`*.toml` config, `*.json` fixtures), excluding lockfiles, `node_modules`, build output
- **validate:** parse with the format's loader (`json.load` / `yaml.safe_load` / `tomllib.load`)
- **phase:** pre-deploy · **scope-trigger:** the detected data globs
- **plan-gate:** task edits a seed/fixture/config-data file
- **prevents:** broken JSON/YAML that only fails when the app or seeder reads it
- **manifest:** `globs: []` (which paths count as deploy-data for this project)

### 5. `db-migration`
- **detect:** `**/migrations/versions/*.py` (alembic), `prisma/migrations/`, `**/migrate/*.sql`
- **validate:** single-head check — the migration graph must have exactly one head
  (`alembic heads | wc -l == 1`, or the tool's equivalent). Application is **not** done here
  (entrypoint owns `upgrade head`); this only catches divergence.
- **phase:** pre-deploy · **scope-trigger:** migration dirs
- **plan-gate:** task adds a migration
- **prevents:** two-heads / divergent-migration collision (the exact class seen when two
  branches both branch off the same revision)
- **manifest:** `tool:` (alembic/prisma/…), `head_check:` (command)

### 6. `reverse-proxy-config`
- **detect:** `deploy/nginx/*.conf`, `nginx.conf`, `Caddyfile`, `traefik*.y{a,}ml`
- **validate:** proxy's own syntax check in a throwaway container
  (`docker run --rm -v <cfg>:/etc/nginx/nginx.conf:ro nginx:alpine nginx -t`); `optional` — if
  skipped, the switch-phase health gate is the net (a broken proxy fails health → rollback)
- **phase:** pre-deploy (optional) + switch (health) · **scope-trigger:** proxy config globs
- **plan-gate:** task edits a proxy config
- **prevents:** proxy syntax errors that 502 the site after reload
- **manifest:** `type:` (nginx/caddy/…), `files: []`

### 7. `runtime-behavior`  *(the anchor smoke — deterministic, no LLM)*
- **detect:** cannot be auto-detected from files — the probe **interviews once** (or reads
  project-knowledge) for each externally-facing service: its health URL, one anchor request,
  and an expected substring that only correct data/config produces (e.g. a price/SKU that only
  the right feed yields)
- **validate:** call the endpoint, assert HTTP 200 + non-empty + expected substring present.
  Deterministic on purpose: it gates an **automatic rollback**, so it must not depend on LLM
  judgment or flaky external egress
- **phase:** post-deploy (drives rollback) · **scope-trigger:** always runs post-switch (cheap)
- **plan-gate:** task changes a service's bound data/feed or answer contract
- **prevents:** "booted healthy but behaves wrong" — silent bot, wrong feed/data bound
- **manifest:** `checks: [{service, url, request, expect_substring}]`

## Always-on spine (runner logic, not a class)

Independent of which classes fire, every deploy runs the atomic-switch spine — this is what
makes any slip non-fatal:

1. build image, tag current running image `:prev`
2. bring the new version up **alongside** (entrypoint applies migrations)
3. **health gate:** poll each service `/health` every 3 s up to 120 s, require 2 consecutive 200s
4. switch traffic to new; keep `:prev` warm
5. post-deploy `runtime-behavior` smoke
6. **any gate fails → restore `:prev`** (prod stays up); **all green → promote, retire old**

Backup-before-mutate is assumed present (a project-level concern) and invoked before step 1
when the manifest declares a `backup_cmd`.

## Growing the registry

MVP is 7 classes. Add a class only when a real incident exposes a deploy-breaking artifact not
covered here. A new class must supply every schema field above and a **built-in-first** validator
(external tools always `optional`). Record the incident that motivated it in the entry.
