# Stable Libraries Whitelist

Elements on this list are considered stable and familiar across multiple projects. The `stack-research` skill does NOT auto-trigger research for them. Caller must explicitly request research if needed (e.g., upgrading major version, investigating a specific feature).

## Criteria for inclusion

- 3+ years of production maturity.
- Used across multiple user projects without documentation-driven surprises.
- Major breaking changes are rare or well-announced ahead of time.
- Core API surface is stable enough that memory-based use is usually safe.

## Whitelist

### Node.js / JavaScript / TypeScript
- `react` (18+)
- `next` (Next.js 14+)
- `express`
- `fastify`
- `prisma` (ORM, not Prisma Data Platform)
- `vite`
- `tailwindcss` (v3+)
- `typescript`
- `zod`
- `better-sqlite3`

### Python
- `flask`
- `requests`
- `gspread`
- `fastapi`
- `pydantic`

### Telegram / bots
- `grammy`
- `node-telegram-bot-api`

### Infrastructure
- `docker`
- `git`

## NEVER whitelisted (always researched)

- All external AI APIs (Kandinsky, GigaChat, OpenAI, Anthropic, Study AI, Midjourney, Replicate, etc.)
- All payment APIs (Stripe, YooKassa, Tinkoff, PayPal)
- All messaging APIs (Twilio, SMS.ru, etc.)
- All deployment services (Vercel, Railway, Fly.io, Cloudflare)
- Any library with major version < 1.0
- Any library released within the last 12 months
- Any niche tool (Paged.js, remark/rehype plugins, MCP servers, etc.)
- Any service with a custom auth flow (OAuth variants, API keys with non-standard flows)

## Maintenance

Update this list when:
- A new library proves stable across 3+ projects (add).
- A whitelisted library has a breaking-change major version (remove until re-verified).
- User reports a documentation-driven surprise with a whitelisted library (remove).

Last updated: 2026-04-18
