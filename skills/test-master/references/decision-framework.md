# Test Decision Framework

## Should I write unit tests?

**YES if:**
- Function has business logic
- Function makes decisions
- Function transforms data
- Function handles errors
- Task specifies testing

**NO if:**
- Simple getter/setter
- One-line text change
- Trivial config update
- No code written (research/docs)

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

**YES if:**
- Feature has >5 tasks
- Feature touches critical flows
- Feature has breaking changes
- User explicitly requests
- Tech Spec specifies E2E tests

**NO if:**
- Small feature (<3 tasks)
- Non-critical functionality
- Well covered by unit + integration tests
- Time/cost constraints

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
