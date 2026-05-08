# Test Decision Framework

## Should I write unit tests?

See [unit-tests.md](unit-tests.md) "When to Write Unit Tests" for full YES/NO criteria.

## Should I write integration tests?

**YES if:**
- Tech Spec specifies integration tests
- Feature has API endpoints
- Feature interacts with database
- Feature calls external services

**NO if:**
- Tech Spec says "None"
- Feature is purely client-side
- Already covered by E2E tests

## Should I write E2E tests?

See [e2e-tests.md](e2e-tests.md) "When E2E Tests Are Written" for full criteria.

## When to Prioritize E2E Over Unit Tests

For some project types, E2E tests are MORE valuable than unit tests:

| Project Type | Primary Tests | Why |
|--------------|---------------|-----|
| API/Backend | Unit + Integration | Logic in functions |
| CLI Tools | Unit + Integration | Testable in isolation |
| **UI Apps** | **E2E + Integration** | Logic in UI interaction |
| **Browser Extensions** | **E2E (real browser)** | APIs can't be mocked reliably |
| **Mobile Apps** | **E2E** | Platform APIs need real env |

**Rule:** If mocking more than testing → wrong test type.

## Redundant Testing Anti-pattern

Tests that duplicate coverage waste time and create maintenance burden.

**Signs of redundant testing:**
- Same behavior verified by both unit test and integration test with no added value
- E2E test that only checks what unit tests already cover
- Multiple test files testing the same function with same scenarios
- "Tests for completeness" that exist without protecting against real regressions

**Rule:** Each test must justify its existence — it catches a specific failure that no other test catches.
