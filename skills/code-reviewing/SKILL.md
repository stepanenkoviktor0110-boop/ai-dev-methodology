---
name: code-reviewing
description: |
  Code review methodology and quality standards for comprehensive code analysis.
  Use to understand WHAT and HOW to review code: 11 review dimensions, process, quality standards.

  Use when: "проверь код", "code review", "ревью кода", "review this code", "check code quality"
---

# Code Review Methodology

Comprehensive code review methodology for ensuring production-ready quality and maintainable architecture.

## Review Dimensions

Perform systematic analysis across these 11 dimensions:

### 1. Architectural Patterns

- Evaluate adherence to established architectural patterns (MVC, MVVM, Clean Architecture, etc.)
- Assess design patterns usage (Factory, Strategy, Observer, etc.)
- Verify layer separation and dependency direction
- Check for architectural anti-patterns (circular dependencies, god objects, tight coupling)

### 2. Separation of Concerns

- Validate single responsibility principle compliance
- Examine module boundaries and cohesion
- Review business logic vs presentation logic separation
- Assess data layer abstraction and persistence logic isolation

**Good practices:**
- One file = one responsibility (UserService in one file, PaymentService in another)
- Functions < 50 lines; if larger, break into smaller functions
- Maximum 3 levels of nesting; use early returns to reduce nesting
- High-level modules should not depend on low-level details

### 3. Code Readability & Maintainability

- Evaluate naming conventions (variables, functions, classes)
- Assess code organization and file structure
- Check for appropriate use of comments and documentation
- Review complexity metrics (cyclomatic complexity, nesting depth)
- Verify consistent code style and formatting

**Good practices:**
- Meaningful comments focus on "why" rather than obvious "what"
- DRY principle: extract repeated code into functions/modules
- Readable > clever: clear code is better than short but cryptic code
- No magic numbers: extract to named constants (`MAX_UPLOAD_SIZE` not `5242880`)

### 4. Error Handling & Logging

- Examine error propagation strategy
- Verify appropriate use of try-catch blocks
- Check error messages clarity and actionability
- Assess graceful degradation and fallback mechanisms

**Good practices (error handling):**
- Always use try-catch for operations that can fail (API calls, DB operations, file I/O)
- Don't swallow errors: always re-throw after logging (unless explicitly handling)
- Fail fast: validate inputs early; throw errors immediately when invalid
- User-friendly errors: show generic message to users, log details internally

**Logging review checklist:**
- Key operations have logs (external calls, auth events, state transitions, business operations)
- Structured format used (JSON / logger library), not string concatenation or `console.log`
- Every log includes context: userId, action, resourceId (not just a bare message)
- Correlation/request ID propagated through call chain
- Log levels used correctly (info for success, warn for recoverable, error for failures)
- Error logs include stack traces
- No secrets or PII in logs (passwords, tokens, API keys, emails, phone numbers)
- No empty catch blocks (`catch (e) {}` — silent error swallowing)
- No logging inside tight loops (generates thousands of duplicate lines)

**Automatic severity mappings:**

| Pattern | Severity |
|---------|----------|
| Secrets or PII logged (tokens, passwords, emails in plaintext) | critical |
| Empty catch block — error swallowed without logging | major |
| External call (API, DB) without any logging | major |
| Missing correlation/request ID in service handling requests | minor |
| `console.log` / `print` used instead of structured logger | minor |

### 5. Type Safety (TypeScript/typed languages)

For TypeScript or other typed codebases:

- Validate type definitions completeness and accuracy
- Check for inappropriate use of `any` type (TypeScript) or equivalent loose typing
- Assess interface and type alias design
- Review generic type usage and constraints
- Verify null/undefined handling and optional chaining
- Check for type assertions and their justification

### 6. Testing Coverage

- Evaluate unit test presence and quality, coverage for critical paths
- Review test organization, naming, mocking strategies, isolation
- Check for integration/E2E test needs and edge case coverage

For full criteria (when to test, mocking strategy, quality review) see test-master skill.

### 7. Dependencies Management

- Review new dependencies necessity and appropriateness
- Check for dependency version conflicts
- Assess bundle size impact
- Verify security vulnerabilities (outdated packages)
- Evaluate licensing compatibility

**Good practices:**
- Verify imports exist before using: read source files to confirm exports match expected usage
- Check function signatures: ensure signatures match how you're calling them
- Prefer well-maintained packages: check npm/PyPI activity, security advisories
- Pin major versions: use `^` (caret) for npm to allow patch updates

### 8. Security Considerations

Surface-level pass: hardcoded secrets, missing input validation, obvious injection/XSS/CSRF, auth/authz logic, sensitive data exposure. Add `.env`, `*.key`, `credentials.json`, `secrets/` to .gitignore.

For deep audit (OWASP Top 10, attack vectors, dependency CVEs) invoke security-auditor skill.

### 9. Performance Implications

- Identify potential performance bottlenecks
- Review algorithmic complexity
- Check for unnecessary re-renders (React) or recomputations
- Assess memory leak risks
- Evaluate database query efficiency

**Good practices:**
- Avoid N+1 queries: use batch operations, eager loading, or caching
- Cache expensive computations: use memoization for functions
- Prevent memory leaks: clean up event listeners, timers, subscriptions in cleanup functions
- Use pagination for large datasets: don't load all records at once
- Profile before optimizing: measure actual bottlenecks before making changes

### 10. Cross-File Consistency

For the code under review, verify correctness of function/class usage:

**Process:**
1. When code CALLS a function from another file → Read that file, verify signature matches
2. When code USES a class/method → Read class definition, verify method exists and signature matches
3. When code IMPORTS something → Verify import path is correct

**What to check:**
- Function called with correct arguments
- Method exists on the class
- Import paths are valid
- Types match (if TypeScript)

**Report as issue if:**
- Function called with wrong arguments (runtime crash)
- Method doesn't exist (runtime crash)
- Import path broken (load failure)

Read the source files where functions/classes are defined to verify signatures match.

### 11. Resource Management

- Identify heavy resources: ML models, database connection pools, browser instances, API clients, large caches
- Check if heavy resources are created as singletons (one instance shared) or duplicated across files/components
- When code creates a heavy resource (`new Model()`, `ModelClass(...)`, `create_pool()`): search the project for other instantiations of the same class
- Verify resource lifecycle: who creates, who consumes, when disposed
- Check for resource leaks: opened connections/files/handles that are never closed

**Automatic severity mappings:**

| Pattern | Severity |
|---------|----------|
| Same heavy resource class instantiated in multiple files without shared instance | major |
| Heavy resource created inside a loop or per-request handler | critical |
| Resource opened but never closed (connection, file handle, cursor) | major |

## Dimension Prioritization

Focus on dimensions based on code context:

| Context | Prioritize | Reason |
|---------|------------|--------|
| Auth/login code | Security (8), Error Handling (4) | Auth vulnerabilities are critical |
| User input handling | Security (8), Type Safety (5) | Input validation prevents attacks |
| Database queries | Security (8), Performance (9) | SQL injection, N+1 queries |
| New feature | Architecture (1), Testing (6) | Foundation for future changes |
| Refactoring | Cross-File (10), Testing (6) | Avoid breaking existing code |
| Performance fix | Performance (9), Dependencies (7) | Target the actual bottleneck |
| Typed codebase | Type Safety (5), Cross-File (10) | Type errors cause runtime crashes |
| ML/AI pipeline | Resource Mgmt (11), Performance (9) | Heavy models duplicated waste memory |
| Microservice init | Resource Mgmt (11), Architecture (1) | Connection pools and clients should be shared |

## Review Process

Before starting, read [quick-ref-code-reviewing.md](../quick-learning/references/quick-ref-code-reviewing.md) — top reasoning patterns for this skill (if file exists and non-empty).

1. **Initial Scan**: Quick overview to understand scope and context
2. **Deep Analysis**: Systematic review of each dimension listed above
3. **Cross-Reference**: Compare implementation against userspec, techspec, and project standards
4. **Issue Categorization**: Classify findings by severity:
   - **critical** → blocking issues that must be fixed
   - **major** → significant concerns that should be addressed
   - **minor** → improvements that are valuable but optional
5. **Recommendation Formulation**: Provide specific, actionable suggestions

## Quality & Communication

- Focus on issues that materially impact quality, security, maintainability — not stylistic preferences
- Provide specific examples and code snippets; explain "why", not just "what"
- Consider project context from documentation when available
- Acknowledge good practices when present

## Checks against state

These read state off disk — they are not a re-check of the reasoning above. Run each line whose
precondition applies, read the output, act on what it says. Substitute `<diff paths>` with the files
under review.

```bash
# 1. a failing test cites a document — open the cited document before touching either side
rg -n -i "see |spec|doc/|docs/|§|раздел" <the failing test file>
<open each cited document at the cited place and read the passage>

# 2. secrets or PII inside logging calls (dimension 4 → critical)
rg -n -i "log|logger|print|console\.(log|error)" <diff paths> | rg -i "password|secret|token|api_key|email|phone|\.env"

# 3. empty catch blocks — errors swallowed silently (dimension 4 → major)
rg -n -U "catch\s*\([^)]*\)\s*\{\s*\}|except[^:]*:\s*pass" <diff paths>

# 4. unstructured logging where a logger exists (dimension 4 → minor)
rg -n "console\.log|^\s*print\(" <diff paths>

# 5. cross-file usage — the definition of every called function/class must be read, not assumed
rg -n "def <name>|function <name>|class <name>|export .*<name>" <repo>

# 6. heavy resource instantiated in more than one file (dimension 11 → major)
rg -n "new <ResourceClass>|<ResourceClass>\(" <repo> --glob '!**/test*'

# 7. secret-bearing paths are ignored (dimension 8)
rg -n "^\.env|\*\.key|credentials\.json|secrets/" .gitignore
```

Required results:

- **Check 1** must be run before the failing test is made to pass again, and its outcome written
  into the finding. The cited passage must actually state the asserted claim. If it does not, the
  test encodes the error being corrected — fix the test, not the code. A citation proves where a
  claim came from, never that it is right, so "the test cites a document" is not a reason to make
  the code match it. (triad #498)
- **Checks 2, 3, 4** must return nothing. Any hit is a finding at the severity given in the
  dimension-4 mapping table; report it, do not weigh it.
- **Check 5** must return a definition for every function, method and class the diff calls across a
  file boundary, and each signature must match the call site. No hit means a broken import or a
  renamed symbol — a runtime crash, reported as critical.
- **Check 6** must return hits in at most one non-test file per heavy resource class. Two or more
  files instantiating the same class means no shared instance; inside a loop or a per-request
  handler it is critical.
- **Check 7** must return a hit for every pattern whose file type exists in the repo. A missing
  pattern is a finding — add it to .gitignore before the review closes.

## Learned Patterns

Top reasoning patterns for this skill live in
[quick-ref-code-reviewing.md](../quick-learning/references/quick-ref-code-reviewing.md), loaded at
the start of the Review Process. Rules that a command can settle are in "Checks against state"
above rather than repeated here.
