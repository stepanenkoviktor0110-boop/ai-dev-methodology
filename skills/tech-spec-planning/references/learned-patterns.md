# Learned Patterns — Tech Spec Planning

> Loaded by audit agents and retrospective only. Orchestrator loads only Promoted Patterns (in SKILL.md).

- When adding auth flow to imported data -> verify credentials existence AND isActive flag explicitly in the integration spec, to avoid missing auth discovered at user verification
- When an external service returns an unexpected result during research -> run escalating diagnostics (parameters -> curl -> re-read docs) before declaring a blocker
- When output format requirements arrive iteratively -> agree on complete output structure with a mockup before writing code, to avoid rewriting implementation on each clarification
- When an external system returns empty results -> enumerate and check all available channels/endpoints before concluding data is absent
- When speccing a complex project with server-side actions -> include performance timing baseline in the MVP scope to detect degradation before it reaches production
- When diagnosing performance problems on a low-traffic server -> check default timeout/connection pool/cache limits in configuration before optimizing code
- When planning file sync between two repo versions -> launch code-research to classify diff depth before writing scope, to avoid describing a mechanical sync that requires manual review
- When a feature combines client-only storage with server-side automation -> verify data-access layer compatibility before making architecture decisions, to avoid a storage-layer conflict mid-spec
- When spec narrows a criterion discussed in the interview (A or B -> only A) -> add to Technical Decisions: decided NOT to include B, because... to avoid extra validation rounds
- When adding a metric to a dashboard without explicit time horizon -> clarify with user: launch / daily / all-time, before writing spec
- When proposing hosting/stack for a new project -> clarify deployment region and regulatory constraints BEFORE proposing solutions, to avoid rewriting the architectural stack after discussion
- When completing the Implementation Tasks section -> check for Files-to-modify overlap within each wave, to prevent merge conflicts during parallel execution
- When designing a feature with user file uploads to disk -> explicitly describe the file delivery mechanism (protected API, not static) in Architecture, to prevent IDOR through unauthorized direct file access
- When a feature reads methodology files via GitHub Contents API -> verify whether those files are committed in the target repositories BEFORE writing AC, to avoid data unavailable for all projects due to .gitignore
- When writing curl commands in AVP for authenticated endpoints -> include auth header AND add a test without-key -> 401 to avoid false QA pass with broken authorization
- When config contains a whitelist/filter for limiting processing -> clarify at which pipeline stage the filter is applied and move it before the resource-intensive operation
- When asked to remove X from repository -> clarify: git untrack only (git rm --cached + .gitignore) or physical deletion from disk, to avoid destroying local files with a git operation
- When needing to obtain configuration from a provider (DNS, settings) -> ask the client first whether they have access to the provider's control panel, to avoid waiting for support response when the client can get the data themselves
- When a tech-spec decision narrows or defers a requirement from user-spec -> check whether that requirement appears in the user-spec AC BEFORE writing the Decision, to avoid introducing scope reduction without explicit user agreement
- When a user rejects a proposed architectural simplification -> ask 'what distinction is lost by the simplification?' before continuing, to surface the missing key abstraction before implementation (triad #137)
