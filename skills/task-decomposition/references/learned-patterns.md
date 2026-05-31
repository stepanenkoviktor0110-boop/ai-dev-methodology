# Learned Patterns — Task Decomposition

> Loaded by audit agents and retrospective only. Orchestrator loads only Promoted Patterns (in SKILL.md).

- When writing AC for CI/CD pipeline tasks -> explicitly include concurrency/idempotency guards (cancel-in-progress, prevent duplicate runs) in AC, to avoid predictable best-practice additions as deviation findings
- When writing AC for markdown-only features -> formulate criteria through presence of specific structural artifacts (sections, links, guard blocks), not keywords, to make AC automatically checkable
- When a task in a wave references another task result -> replace the inter-task dependency with reading from a shared source of truth, to preserve wave parallelism without read-after-write risks
- When creating a deletion task (remove feature/constant/field) -> add explicit AC to check dead variables, stale comments, and duplicate tests before review
- When designing algorithms that distribute records into capacity-capped buckets -> define the overflow policy before implementing, to avoid silently losing records when a bucket fills
- When adapting a task template to a new domain -> generate 1 pilot task and verify each frontmatter field for compatibility before scaling, to avoid accumulating 30+ fixes on first run
- When AC contains a numeric boundary (max N iterations/attempts) -> include the boundary value N in smoke or AC check to catch off-by-one before code audit
- When describing an agent skip behavior on empty input -> explicitly describe the processing logic that runs after the skip, not only the output marker, to prevent label-swap without logic change
- When a task contains a test using an exact marker string defined in another task -> declare depends_on on the source task even if the string is a literal, to avoid missing implicit dependencies
- When task N creates no-op stubs for future tasks -> add an explicit step in each dependent task brief: replace the no-op stub with implementation, to guarantee no placeholder remains in working code
- When Task B tests functions from Task A file -> add those function signatures explicitly to Task A What-to-do section, so every exported function has a clear owner
- When task-creator writes hints for a file already implemented in the codebase -> read the actual code of that file BEFORE writing hints, to avoid hints that contradict existing implementation
- When Task A TDD Anchor names a test file that is the primary deliverable of Task B -> remove the test from Task A TDD Anchor and add a reference to the owning task, one file one owner
- When a task's deliverable is a SKILL.md file -> assign skill: skill-master and reviewers: skill-checker, to avoid wrong skill/reviewer values caught only by validators
- When producer/consumer tasks split across waves or parallel producers must interoperate -> read consumer tasks and pass exact interface contracts (field names, types, shapes) to each producer, to avoid producer-centric design and implicit-consensus failures
- When sizing work from a derived/structural artefact (catalog, index, schema, block-map, file list) -> open one sample of the actual content the artefact represents and resize if signal differs, to avoid surface-proxy fallacy where structural metadata is uncorrelated with semantic complexity of described content
- When drafting the spec for the next task in a sequence after the previous task exited review with non-trivial findings -> enumerate recurring themes from the previous task's review-fix commits and deviation log and pre-bake them as explicit AC/constraints in the next spec, to prevent review-debt amnesia across plans
- When request to make a build-time artifact (file/config/code constant) editable from a UI -> enumerate the in-place mutation alternative (server action rewrites existing artifact + revalidates) and reject it on explicit operational tradeoffs before designing new storage, to avoid new-storage default bias where "user wants to edit X" automatically justifies new persistence
- When brand or product-family name appears in retrieved context without enumerating exact members available -> enforce explicit anti-pattern examples in the grounding rule (not just generic "use only the source"), to prevent pretrained-brand leak where the model fills in plausible-sounding members from pretraining
- When module exposes a primary acquire path and a secondary swap/inject path for the same managed resource -> replay the primary path's full invariant-establishing setup on every instance entering the secondary path, to avoid twin-path invariant drift where injected instance silently lacks invariants the rest of the code assumes
