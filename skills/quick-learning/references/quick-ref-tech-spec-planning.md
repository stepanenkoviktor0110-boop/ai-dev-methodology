# Quick Reference — Tech Spec Planning

1. Verify target files before describing an operation — grep each file; a file without X needs add, not replace. (Seen: 2)
2. Verify API response shapes with a live call before copying them from code-research into the spec — one call is cheaper than a mirage. (Seen: 2)
3. Verify file paths and call sites via ls/grep, not from memory or docs. (Seen: 2)
4. When an external naming claim (component, attribute, code symbol) is about to enter the spec — verify it against ground truth before recording. (Seen: 1)
5. When a Decision narrows/defers a user-spec requirement — check if it appears in user-spec AC before writing the Decision. (Seen: 1)
6. When completing Implementation Tasks — check Files-to-modify overlap within each wave to prevent merge conflicts. (Seen: 1)
7. When a task references a backlog item/prior spec/decision by id — open and read it in full before drafting the plan. (Seen: 1)
8. When a spec instruction contradicts an established project reference — treat the reference as authoritative and flag the instruction as a hypothesis, not a newer override. (Seen: 1)
9. When writing curl in AVP for authenticated endpoints — include auth header AND a without-key -> 401 case to avoid false QA pass. (Seen: 1)
10. When a quantitative threshold is borrowed from a closed/archived session's report — re-measure on the working branch or rewrite it as relative (baseline + delta). (Seen: 1)
