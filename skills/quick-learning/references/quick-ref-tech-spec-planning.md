# Quick Reference — Tech Spec Planning

1. Grep exact symbol/path/function name before recording in spec — never trust naming-convention assumptions (name-mirage, triad #307).
2. Verify file paths via ls/glob before writing them in tech-spec; docs describe intent, not reality (Seen: 2).
3. Verify API response shapes with a live call before including them in spec — one call is cheaper than mirage propagation (Seen: 2).
4. Verify ALL file targets (add vs replace vs delete) via grep before describing the operation; wrong op type surfaces only at execution (Seen: 2).
5. When spec narrows a user-spec requirement → check that requirement in user-spec AC first to avoid hidden scope reduction without user agreement.
6. When writing a derivative artifact (tech-spec from user-spec) → grep upstream source for each policy to prevent silent default erosion (triad #311).
7. Derive output field names from the consumer's parsing code, not from spec prose or convention — producer naming ≠ consumer naming (triad #300).
8. When a stakeholder names a technical component as a requirement → verify it against current project docs before fixing in spec (triad #267).
9. Filter decisions for user discussion: "does this change product behavior for the user?" — if no, decide silently and move on.
10. When spec defines narrower access on an endpoint where existing guard allows broader roles → explicitly describe new guard creation in the task to prevent auth gaps discovered only at security audit.
