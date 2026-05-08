# Test Quality — Mocking Strategy

For BAD/GOOD test examples and the "mock 3+ deps = wrong test type" rule, see [test-quality-review.md](test-quality-review.md).

## Mocking Strategy by Level

### Unit Tests
- **Mock:** Database, API calls, file system, time
- **Why:** Fast, isolated, deterministic
- **How:** Use framework mocking (jest.mock, unittest.mock)

### Integration Tests
- **Real:** Database (test DB), file system
- **Mock:** External services (payments, email)
- **Why:** Test real interactions, avoid external costs/delays

### E2E Tests
- **Real:** Everything (use test/sandbox mode for external services)
- **Why:** Test complete real-world scenario
