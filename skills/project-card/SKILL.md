---
name: project-card
disable-model-invocation: true
description: |
  Generates an HTML project card carrying the full technical picture: server, domain, repo,
  CI/CD, DNS, analytics, logins and passwords, useful commands. Styled in the project's own
  brand (colours, fonts, logo). Built to print to PDF (Ctrl+P) on a single A4 sheet.

  Use when: "карточка проекта", "project card", "project-card",
  "собери карточку", "техническая карточка", "инфо по проекту",
  "собери данные проекта", "сделай паспорт проекта"
---

# Project Card

Generates a one-page HTML card holding every technical detail of a project for its owner or team.
The card is styled in the project's own brand, carries editable fields for passwords, and is
optimised for printing to PDF (A4, single sheet).

The card itself is written in Russian — it is read by the owner. These instructions are not.

## Phase 1: Collect the data

### 1.1 Brand style

Find it in the project automatically; do NOT ask the user:

1. **Colours** — in SCSS/CSS files (`globals.scss`, `_variables.scss`, `tokens.json`, `tailwind.config`), constants, theme files
2. **Font** — in `layout.tsx`, CSS imports, Google Fonts config
3. **Logo** — in `public/` (logo.png, logo.svg, favicon)
4. **Nothing found** — use a neutral dark theme: `#1a1a2e` background, `#e0e0e0` text, `#4fc3f7` accent, Inter/system font

### 1.2 Infrastructure data

Collect automatically from:

- **project-knowledge** (`deployment.md`, `architecture.md`, `project.md`) — the main source
- **git remote** — repository URL, branches
- **.env.example** — environment variables (never the secret values)
- **package.json** — stack, name
- **Dockerfile / docker-compose.yml** — containers
- **CI/CD** (`.github/workflows/`, `vercel.json`, `netlify.toml`) — deploy
- **.vercel/project.json** — Vercel project
- **ecosystem.config.*js** — PM2 configuration

### 1.3 What to gather

Gather as much of the following as applies to the project:

| Block | What to gather |
|------|------------|
| **Site** | Production URL, redirects, subdomains |
| **Repository** | GitHub URL, development branch, deploy branch, CI/CD type |
| **Server** | IP, SSH access, OS, Node/Python/etc version, process manager, port, path on the server, nginx/caddy config |
| **DNS** | Provider (Cloudflare, Route53...), records, SSL mode, proxy |
| **Domain** | Registrar, nameservers |
| **Analytics** | Service (Umami, Plausible, GA), URL, login |
| **Database** | Type (PostgreSQL, MySQL, MongoDB...), host, database name |
| **Hosting/PaaS** | Vercel, Railway, Fly.io, VPS — provider-specific details |
| **Stack** | Framework, runtime, key dependencies |
| **Secrets** | Where they live (GitHub Secrets, .env, Vault) — list the names, never the values |
| **Env variables** | The list from .env.example with descriptions |
| **Docker** | Containers, compose files, volumes |

### 1.4 Ask for what is missing

After the automatic pass, show the user what was found and ask about:

1. **Passwords and logins** — for every service with a sign-in (analytics, domain registrar, hosting panel, CI/CD)
2. **Missing data** — anything not found in the documentation
3. **Additional services** — "есть ли ещё сервисы, которые нужно добавить?"

> **CRITICAL:** Never print passwords or secrets into tool-call logs or chat text. Every sensitive value goes into the HTML file and nowhere else.

## Phase 2: Generate the card

### 2.1 HTML structure

A single-page HTML file, A4 format:

```
PROJECT-CARD.html  ← file name, add to .gitignore
```

**Required elements:**
- `@page { size: A4; margin: 0; }` — for printing
- `print-color-adjust: exact` — keep colours in the PDF
- `-webkit-print-color-adjust: exact` — for Chrome
- `overflow: hidden; max-height: 297mm` — do not spill past the sheet
- A Google Fonts `<link>` if the project's font comes from Google Fonts

### 2.2 Design

**Built on the project's brand:**
- Background: the darkest colour in the palette, or the primary darkened
- Accent (section headings, links): the bright/contrasting brand colour
- Text: light on a dark background
- Card blocks: slightly lighter than the background with a thin border
- Logo in the header: if it is dark on a dark background, add a white plate (`background: #fff; padding; border-radius`)

**Layout:**
- Header: logo + name + "Техническая карточка — {месяц} {год}"
- Body: a 2–3 column grid of cards with key-value rows
- Footer: "Конфиденциально • Не распространять"

**Sizes for A4:**
- Body font: 10–11px
- Section headings: 10px uppercase, letter-spacing
- Values: 10px
- Body padding: 24–28px
- Gap between cards: 10px
- Card padding: 8–10px

### 2.3 Passwords — editable fields

For every password or login the user did NOT provide, insert:

```html
<span contenteditable="true" style="border-bottom:1px dashed {accent-color};padding:0 4px;min-width:80px;display:inline-block;outline:none">впиши сюда</span>
```

If the user did provide a value, insert it as plain text.

### 2.4 Gitignore

Add to the project's `.gitignore`:

```
# private project card
PROJECT-CARD.*
```

## Phase 3: Show and iterate

1. Report that the file was created
2. Offer to open it in a browser and check
3. Remind: fill the `contenteditable` fields → Ctrl+P → PDF
4. If something does not fit on the sheet — shrink, regroup, or drop the least important part
5. Iterate on the user's feedback (colour, placement, data)

## Checks against state

```bash
# 1. the card was written
rg -c . PROJECT-CARD.html

# 2. it is excluded from the repository
rg -n "PROJECT-CARD" .gitignore

# 3. no secret leaked into anything tracked by git
git status --short
```

Check 2 returning nothing means the next commit carries the passwords into the repository — fix it
before telling the user the card is ready.

Fitting on one A4 sheet and the logo's contrast against the background cannot be read off disk —
they are checked by the user in the browser, which is what Phase 3 step 2 is for.
