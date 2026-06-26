# Quick Reference — Tech Spec Planning

1. A reviewer confidently asserts a verifiable fact is wrong — run the cheapest direct check that settles it before acting; assertiveness is not evidence. (Seen: 5)
2. When moving tasks between waves, check "Files to modify" of all wave tasks pairwise for overlap to prevent merge conflict and duplication. (Seen: 5)
3. Verify file paths via ls/glob and grep call sites before writing — paths come from the filesystem, not memory or docs. (Seen: 4)
4. Launching task-creator agents — check the runner (jest/vitest/pytest) and test directories, pass them explicitly in every brief. (Seen: 3)
5. A Decision narrows/defers a user-spec requirement — first check the user-spec AC and update it in the same step; don't leave upstream doc contradicting. (Seen: 3)
6. Filter each tech-spec decision by "does product behavior change for the user?" — if not, decide it yourself instead of spending a communication round. (Seen: 3)
7. Moving a task/script/module/pipeline to another execution context — enumerate every implicit dependency (env, filesystem, network, runtime, auth); existence ≠ portability. (Seen: 3)
8. Before writing method-call signatures into implementation hints — verify the actually-installed package version, not stale API from training memory. (Seen: 2)
9. A quantitative gate is computed over a narrower input set than the unit being judged — align measurement scope before reading the number as a verdict. (Seen: 2)
10. A spec restates a contract that exists more authoritatively elsewhere (tests, real signature) — treat the machine-verifiable form as the contract; read it before coding. (Seen: 2)
