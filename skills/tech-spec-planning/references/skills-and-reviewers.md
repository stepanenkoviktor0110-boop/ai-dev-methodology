# Skills and Reviewers Catalog

Single source of truth for selecting skills and reviewers in Implementation Tasks.
Used by: tech-spec-planning (Phase 4), task-decomposition (Phase 1).

## Execution Skills

| Skill | What it's for | Typical tasks |
|-------|--------------|---------------|
| `code-writing` | Writing/modifying code, TDD cycle | API endpoints, models, services, components, migrations, tests |
| `infrastructure-setup` | Framework init, folder structure, Docker, pre-commit hooks, testing setup | Dockerfile, pre-commit hooks, folder structure, .gitignore, smoke tests |
| `deploy-pipeline` | CI/CD pipelines, deployment config, automated deploy | GitHub Actions, deploy scripts, platform config, secrets management |
| `documentation-writing` | Documentation, Project Knowledge updates | Architecture docs, API docs, conventions, patterns |
| _(no skill)_ | Creating/updating skills and agents — follow the skill-authoring conventions directly | New skills, skill modifications |
| `pre-deploy-qa` | Acceptance testing before deploy (tests + acceptance criteria) | QA task in Final Wave |
| `post-deploy-qa` | Live environment verification after deploy via MCP tools | Post-deploy task in Final Wave |
| `prompt-master` | Writing/improving LLM prompts, prompt engineering | System prompts, user prompt templates, few-shot examples, prompt optimization |

| `code-reviewing` | Full-feature code quality audit | Code Audit in Audit Wave |
| `security-auditor` | Full-feature security audit | Security Audit in Audit Wave |
| `test-master` | Full-feature test quality audit | Test Audit in Audit Wave |

Tasks without skill (user instructions) — skill not specified, description is in the task itself. Example: "ask user to register a bot in BotFather".

Prompt tasks (LLM system prompts, user templates) use `prompt-master` skill — they are NOT code-writing tasks. TDD Anchor is replaced by manual verification on sample data.

## Reviewer Agents

This table says which agent checks what. It does not say which model runs it or how hard it
should think — that is configuration, and it lives in each agent's own frontmatter and in the
harness settings. A skill that pins either one overrides a setting the owner made deliberately,
and goes stale the moment that setting changes.

| Agent | What it checks |
|-------|---------------|
| `code-reviewer` | Code quality: structure, patterns, naming, complexity, error handling |
| `security-auditor` | OWASP Top 10, injection, XSS, auth, input validation, secrets |
| `test-reviewer` | Test quality: coverage, meaningful assertions, test pyramid balance |
| `skill-checker` | Skill compliance: frontmatter, structure, authoring guidelines |
| `prompt-reviewer` | Prompt quality: clarity, positive framing, examples over rules, compression, XML structure, success criteria |
| `infrastructure-reviewer` | Infrastructure setup quality: folder structure, pre-commit, Docker, .gitignore, testing |
| `deploy-reviewer` | CI/CD pipeline and deployment config quality: workflows, secrets, platform config |

## Reviewer Routing

Route by what the task's files actually contain, not by which skill produced them. Read the task's
`Files to modify` and `Files to read`, match every row whose trigger fires, and take the union of
the reviewers. A task that matches no row gets no reviewer.

| Trigger — what the task's files contain | Reviewer |
|---|---|
| Non-trivial application code: modules, endpoints, services, components, scripts | `code-reviewer` |
| Authentication or authorization, user-supplied input, secrets and credentials, database queries built from input, external API calls, file uploads, publicly reachable endpoints, database schema migrations | `security-auditor` |
| Test files added or changed, or a task whose contract is defined by tests (TDD anchor) | `test-reviewer` |
| Dockerfile, compose file, pre-commit hooks, project scaffolding, `.gitignore`, test-harness config | `infrastructure-reviewer` |
| CI/CD workflows, deploy scripts, platform config, secrets handling in CI | `deploy-reviewer` |
| Files under `.claude/skills/` or `.claude/agents/` | `skill-checker` |
| LLM prompts: system prompts, prompt templates, few-shot examples | `prompt-reviewer` |
| Project-knowledge files or other project documentation | `documentation-reviewer` |
| Trivial change only: typo, comment, renamed local, version bump, formatting | none |
| Audit Wave or Final Wave task — the audit or QA run is itself the review | none |

When the `reviewers` field is empty in a task — apply this table to the task's files.

## Examples

### Code task touching no auth and no user input
```yaml
skills: [code-writing]
reviewers: [code-reviewer, test-reviewer]
```
Internal logic with its unit tests. No security-relevant surface → no security pass.

### Code task handling user input or auth
```yaml
skills: [code-writing]
reviewers: [code-reviewer, security-auditor, test-reviewer]
```

### Code task shipping a schema migration
```yaml
skills: [code-writing]
reviewers: [code-reviewer, security-auditor, test-reviewer]
```
The migration fires the security row even when the task touches no auth.

### Infrastructure setup task
```yaml
skills: [infrastructure-setup]
reviewers: [infrastructure-reviewer, security-auditor]
```
Security fires on the `.gitignore` / secrets side; add `code-reviewer` when the task also writes
application code.

### Deploy pipeline task
```yaml
skills: [deploy-pipeline]
reviewers: [deploy-reviewer, security-auditor]
```
Security fires on secrets handling in CI.

### Documentation task
```yaml
skills: [documentation-writing]
reviewers: [documentation-reviewer]
```

### Trivial change (version bump, typo)
```yaml
skills: [code-writing]
reviewers: []
```

### Audit task (Audit Wave)
```yaml
skills: [code-reviewing]  # or security-auditor, test-master
reviewers: []
```

### QA task (Final Wave)
```yaml
skills: [pre-deploy-qa]
reviewers: []
```

### Post-deploy verification (Final Wave)
```yaml
skills: [post-deploy-qa]
reviewers: []
```

### Prompt task
```yaml
skills: [prompt-master]
reviewers: [prompt-reviewer]
```
