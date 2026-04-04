# Learned Patterns — Code Writing

> Loaded by audit agents and retrospective only. Orchestrator loads only Promoted Patterns (in SKILL.md).

- When wrapping API calls with a generic retry decorator -> explicitly exclude non-retryable exceptions (auth errors, validation failures) to avoid retrying errors that will always recur
- When unit tests use mocks for external processes/APIs -> run at minimum 1 live smoke run before declaring QA passed, to prevent false all-tests-pass when mock diverges from reality
- When using a retry decorator with a rate-limited API -> verify whether failed requests count toward the quota before enabling retry, to avoid burning quota on pointless retries
- When generating config files with enum fields or nested configs -> verify all allowed values from the official schema/docs including nested objects to avoid invalid-but-plausible values
- When writing deploy scripts that create named resources -> clean up by identity (name/ID), not through management tool, to prevent failure from orphaned resources
- When TDD Anchor describes a test for a private class method -> invoke through an object instance, not through direct import, so tests do not fail with ImportError before running real logic
- When calling clear/reset on an external service before writing new data -> explicitly reset ALL state layers (content + formatting + cache) to prevent previous state from surfacing after cleanup
- When CSS position:fixed fails on a React component with inline style display:none -> use JS isMobile state + resize listener mirroring existing components, not CSS overrides
- When connecting an external library adapter to a DB -> verify the expected object type (raw driver vs query builder) in docs BEFORE writing init code, to avoid runtime adapter incompatibility on first query
- When writing a GitHub Actions SSH deploy step that reloads a service -> remove sudo from the reload command and add StrictHostKeyChecking=no in the SSH command, to prevent permission denied on first CI deploy
- When parallel tests write to a shared test DB through a single seed user -> use different email constants per test task to avoid teardown race conditions during parallel execution
- When JS state exists only to toggle CSS values by viewport -> replace state+listener with CSS media queries + className to eliminate re-renders and make layout CSS-controlled
- When writing integration tests with a shared pg connection pool singleton -> declare globalTeardown in vitest.config calling pool.end() once, to prevent hanging test process or pool-ended errors across suites
- When writing E2E tests for async UI operations (upload, submit, save) -> replace waitForTimeout(N) with assertion on a specific data-testid element to avoid flaky tests
- When implementing an HTTP server with API key auth -> include timing-safe comparison and explicit body size limit in the initial implementation, to avoid a predictable security review round
- When a helper function accepts a value from an external source (API response, env var, user input) -> manually check edge cases (null, undefined, empty string, 0) before first review
- When task has numeric thresholds in code -> extract magic numbers to named constants before first review, to avoid a predictable hardcoded-value review finding
- When a library config option is silently ignored in a new major version -> check option behavior in config-file vs CLI through changelog/issues for the current version BEFORE writing config
- When an integration test checks duplicate/error flow in an auth library -> verify through DB side effect, not HTTP status, to avoid false-negative when library returns 200 with a resend flow
- When E2E global-setup requires a seeded verified user -> use direct INSERT with hashPassword instead of sign-up API + SQL UPDATE, to remove seed phase dependency on a running server
- When adding a new parameter to an existing API request -> check nullable response fields with the new parameter on real data, to prevent TypeError in production
- When uploading files to a remote server via SSH: if SCP or heredoc inside SSH gives Connection closed but plain SSH commands work → use `cat file | ssh host "cat > /remote/path"` (pipe upload); for Python scripts specifically → write to local file, upload via SFTP, execute with python3 -u, to load files without changing port or auth and avoid escaping/buffering issues
- When a bash command passes $(find ... | cut ...) as a path to a flag accepting a file path -> extract the substitution to a named variable in a separate quoted command, to avoid silent false results when paths contain spaces
- When a better-auth handler returns 404 for a correct path -> check BETTER_AUTH_URL for an extra path prefix, to avoid hours debugging webpack and routing
- When a Next.js API route returns 404 with RSC headers and console.error does not fire -> check compiled route.js for import("dependency") and async factory pattern, to diagnose silent module initialization failure
- When Next.js dev server returns 500 Cannot-find-module vendor-chunks/X -> delete .next and restart the server before diagnosing dependency issues, to avoid time spent on a non-existent problem
- When a backlog task describes adding a guard/validation to a file modified in earlier waves -> read the actual file before coding to check whether the guard already exists, to avoid duplicating implementation added as a byproduct of another task
