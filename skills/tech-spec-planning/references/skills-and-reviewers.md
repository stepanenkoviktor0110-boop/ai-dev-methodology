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

## Skill → Reviewers Mapping

| Skill | Default reviewers |
|-------|------------------|
| `code-writing` | `code-reviewer`, `security-auditor`, `test-reviewer` |
| `infrastructure-setup` | `code-reviewer`, `security-auditor`, `infrastructure-reviewer` |
| `deploy-pipeline` | `code-reviewer`, `security-auditor`, `deploy-reviewer` |
| `documentation-writing` | `documentation-reviewer` |
| skill/agent authoring (no skill) | `skill-checker` |
| `pre-deploy-qa` | none — QA is its own verification |
| `post-deploy-qa` | none — verification result is the review |
| `prompt-master` | `prompt-reviewer` |
| `code-reviewing` | none — auditor IS the review (Audit Wave) |
| `security-auditor` | none — auditor IS the review (Audit Wave) |
| `test-master` | none — auditor IS the review (Audit Wave) |

When `reviewers` field is empty in a task — fall back to the default set for that skill.

## Examples

### Code task (most common)
```yaml
skills: [code-writing]
reviewers: [code-reviewer, security-auditor, test-reviewer]
```

### Infrastructure setup task
```yaml
skills: [infrastructure-setup]
reviewers: [code-reviewer, security-auditor, infrastructure-reviewer]
```

### Deploy pipeline task
```yaml
skills: [deploy-pipeline]
reviewers: [code-reviewer, security-auditor, deploy-reviewer]
```

### Task handling user input or auth
```yaml
skills: [code-writing]
reviewers: [code-reviewer, security-auditor, test-reviewer]
```
Security-auditor is already in the default set for code-writing. No extra action needed.

### Documentation task
```yaml
skills: [documentation-writing]
reviewers: [documentation-reviewer]
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
