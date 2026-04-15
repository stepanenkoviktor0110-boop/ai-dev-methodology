# Test Quality Requirements

## What Makes a BAD Test

**Tests nothing:**
```typescript
expect(true).toBe(true)
```

**Tests only that mock was called:**
```typescript
expect(api.call).toHaveBeenCalled()  // Without checking result
```

**No assertions:**
```typescript
render(<Component />)  // Just renders, checks nothing
```

## What Makes a GOOD Test

**Tests actual result:**
```typescript
expect(calculateTotal(100, 0.2)).toBe(80)
```

**Tests real state change:**
```typescript
cart.add({ id: 1 })
expect(cart.items).toHaveLength(1)
```

## Rule: Excessive Mocking = Wrong Test Type

If mocking 3+ dependencies → use integration or E2E test instead.

## Mocking Strategy

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
