# Codex Model Profiles

Stable model tiers for this methodology. Tiers are optimized for **coding workflows** based on SWE-Bench Pro benchmarks.

**IMPORTANT:** Only models available in Codex CLI are used. Check `/model` in Codex to see your available models.

## Tier Mapping — NO FALLBACKS

Each tier has exactly ONE model. If the model is unavailable — STOP and tell the user. Do NOT silently switch to another model.

| Tier | Model | Reasoning | Typical use | Benchmark |
|------|-------|-----------|-------------|-----------|
| `tier_high` | `gpt-5.4` | `high` (`xhigh` for hardest) | Workers, complex architecture, hard debugging, security-critical | SWE-Bench Pro 57.7% — flagship. Comparable to Anthropic Opus |
| `tier_medium` | `gpt-5.3-codex` | `medium` | Reviewers, validators, medium complexity execution | SWE-Bench Pro ~56% — purpose-built for agentic coding. Comparable to Anthropic Sonnet |
| `tier_low` | `gpt-5.4-mini` | `low` | Simple checks, formatting, deterministic routine tasks | SWE-Bench Pro 54.4% — fast, low cost. Comparable to Anthropic Haiku |

**Why `gpt-5.3-codex` for tier_medium:**
- SWE-Bench Pro: ~56% vs 54.4% (gpt-5.4-mini) — codex wins on coding tasks
- Purpose-built for agentic coding (the exact use case of this framework)
- Supports reasoning effort levels (low/medium/high/xhigh)

**NOT available in Codex CLI:** `gpt-5.4-nano`. Do not use it.

## Selection Rules

1. If task can break production or security boundaries → `tier_high`.
2. If task is a reviewer/validator or normal implementation helper → `tier_medium`.
3. If task is deterministic and low-risk → `tier_low`.
4. If model is unavailable → **STOP. Tell user.** Do NOT auto-switch to another model.

## Verification

To confirm models actually switch when spawning subagents:
- Check OpenAI Usage Dashboard (dashboard.openai.com → Usage) after a wave — you MUST see multiple model names in the API calls.
- Or run: `CODEX_LOG_LEVEL=debug codex ...` and grep for model names in the log.
- If only one model appears — tier switching is NOT working. Fix config before proceeding.
