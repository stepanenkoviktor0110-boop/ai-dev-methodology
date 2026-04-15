---
name: test-master
description: |
  Testing methodology: when to write which tests, how to ensure test quality, test pyramid strategy.

  Use when: "напиши тесты", "как тестировать", "проанализируй тесты", "проверь качество тестов", "ревью тестов", "тестовая стратегия"
---

# Test Master

```
        /\
       /E2E\        <- Few (3-5 critical flows)
      /------\
     /Integr.\      <- Some (all endpoints + DB)
    /----------\
   /   Unit     \   <- Many (all business logic)
  /--------------\
 /    Smoke      \  <- Minimal (1-2 basic tests)
/------------------\
```

## Test Types — When to Use

| Type | Use for | Written when | Details |
|------|---------|-------------|---------|
| **Smoke** | Framework configured, env vars, imports | Infrastructure setup (once) | [smoke-tests.md](references/smoke-tests.md) |
| **Unit** | Business logic, decisions, transforms, error handling | Each task, immediately after code | [unit-tests.md](references/unit-tests.md) |
| **Integration** | All API endpoints, DB ops, external services | End of feature (per Tech Spec) | [integration-tests.md](references/integration-tests.md) |
| **E2E** | Top 3-5 critical flows, large features (>5 tasks) | After deploy to dev | [e2e-tests.md](references/e2e-tests.md) |

Skip unit tests for: simple getters, one-line changes, trivial config.
Every API endpoint and DB write must have an integration test.

## Decision & Quality

**Deciding what to test?** Read [decision-framework.md](references/decision-framework.md) — YES/NO criteria per type, E2E prioritization by project type, redundant testing anti-pattern.

**Writing or reviewing tests?** Read [test-quality.md](references/test-quality.md) — good/bad test examples, mocking strategy per level.

**Reviewing existing tests?** Read [test-quality-review.md](references/test-quality-review.md) — categories of bad tests, severity levels.

## Key Principles

1. Write tests immediately — same session as code
2. Test behavior, not implementation
3. Keep tests fast — unit: ms, integration: s, E2E: min
4. Isolate tests — mock external deps in unit tests
5. One concern per test
6. Clear test names — describe what's tested and expected outcome
7. Independent tests — own setup, no shared state
8. Clean state — always start with known DB state
9. Assert on actual results, not mock calls
10. Each test earns its place — catches a failure no other test catches
