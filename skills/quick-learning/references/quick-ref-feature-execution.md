# Quick Reference — Feature Execution

1. Implementing a task that depends on a prior-wave component — read the actual source interface before using the spec description; spec text is not ground truth. (Seen: 6)
2. Verify the result in the real environment before declaring "done" (curl/log/grep a unique marker from the new commit). (Seen: 5)
3. Subagent doesn't finish the task → lead executes directly instead of retrying. (Seen: 5)
4. Symptom has several plausible causes — read the observable evidence before naming a diagnosis and calibrate the claimed cause to the strength of proof. (Seen: 5)
5. Changing/fixing one element of a sibling group (UI, DB query, route guard) — explicitly apply the change to every sibling. (Seen: 4)
6. Automated tool makes repeated connections to a rate-limited server — do a manual connection check first; on block, switch to an alternative IP. (Seen: 4)
7. Worker reports "checks pass" after editing syntax-sensitive constructs — run the check yourself; don't trust the self-report. (Seen: 4)
8. Batch of fork-decisions headed to a stakeholder vote — filter each through your standing decision-authority rule; decide yours, escalate only what's reserved. (Seen: 4)
9. Identical failure recurs across ≥2 attempts — stop retrying; diagnose and fix the behaviour/config that generates it, not the instance. (Seen: 3)
10. A visual/UI decision from the spec not yet seen by the stakeholder — show it before finalizing (one screen at a time); spec described ≠ stakeholder approved. (Seen: 3)
