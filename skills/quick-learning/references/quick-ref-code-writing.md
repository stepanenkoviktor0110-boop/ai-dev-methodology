# Quick Reference — Code Writing

1. Exclude non-retryable exceptions (auth, validation) from retry decorators — retrying them burns quota and never recovers. (Seen: 2)
2. Run ≥1 live smoke run before declaring QA done — mocks can diverge from reality and give false all-pass. (Seen: 2)
3. Assertions on output format, not input attributes: for format-conversion functions assert the output form, else test never catches conversion bugs. (Seen: 2)
4. Path from any external value (API, disk, user input) → validate each segment against allowlist before building path. (Seen: 2)
5. Extract magic numbers to named constants and check edge cases (null/undefined/0) before first review — predictable review findings. (Seen: 2)
6. After fixing first violation of a structural rule → scan the ENTIRE artifact for remaining occurrences (first-fix completion bias). (Seen: 1)
7. Before committing: verify `git diff --name-only` is empty; re-stage auto-fixed files to avoid hooks silently rolling back fixes. (Seen: 1)
8. When task adds guard/validation to a previously modified file → read the file first; guard may already exist from another wave. (Seen: 1)
9. Distinguish transient vs permanent errors in error handlers — don't swallow both under generic Exception; transient → propagate, permanent → mark failed. (Seen: 1)
10. When task requires writing code, write sketch.md (root cause + what must work) and delegate to Codex BEFORE writing directly. (Seen: 1)
