# Abstraction Gate

> Mandatory before writing any entry. Ensures entries capture cognitive errors, not events.

## Step A — Name the cognitive error
In 3-5 words. Examples:
- "partial mutation bias" (local change → assume global invariant holds)
- "existence ≠ active use", "scope anchoring", "authority by proximity", "silent dependency assumption"

Can't name it → skip.

## Step A2 — Knowledge vs Reasoning gate
What fixes the problem — "learn a fact" or "change how you reason"?
- Fix = learn a fact (checklist item, OWASP rule, linting rule, framework API, docs) → **knowledge, skip.**
- Fix = change the reasoning process (no checklist would catch this, expert still falls for it) → **reasoning, proceed.**
- Indicator: if the pattern reduces to a checklist entry — it's knowledge. If no existing checklist covers it — it's reasoning.

## Step B — Domain-strip test
Mechanical, not mental. Do NOT skip sub-steps.

**B1. Write draft** triad (Trigger → Action → Goal) using whatever words come naturally.

**B2. List every domain noun** in the draft: tool names, file names, framework names, platform names, role names, project-specific terms, technical stack terms. Write the list explicitly.

**B3. Replace each domain noun** with its abstract equivalent or delete it. If a field becomes empty or loses meaning → the pattern is domain-specific, skip it.

**B4. Verify:** read the stripped version aloud. Would someone working on a completely different project (mobile game, hardware driver, marketing campaign) understand and benefit from this rule? No → rewrite or skip.

| Level | Example | Verdict |
|-------|---------|---------|
| Bad | "проверить project-knowledge перед деплоем на Vercel" | 3 domain nouns → domain-specific |
| Bad | "после объединения задач пересчитать wave по depends_on" | Domain-specific → meaningless after strip |
| Medium | "после мутации графа перевалидировать топологический порядок" | Structural, but no cognitive error |
| Good | "решение казалось очевидным из категории объекта — не проверил данные о конкретном случае. Ошибка: category default bias" | Cognitive error, domain-free, transferable |

**Common failure mode:** writing abstract Cognitive Error name but leaving domain nouns in Trigger/Action/Goal fields. ALL THREE fields must pass domain-strip independently.

## Step C — Triad orientation
- Trigger = **situation type** (NOT event)
- Action = **corrective thinking rule**
- Goal = **cognitive trap name to avoid**
