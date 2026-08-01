---
disable-model-invocation: true
name: website-legal-audit
description: >
  Audits a website for legal compliance and produces a remediation plan. Jurisdiction is chosen
  by flag: ru (Russia — 152-FZ, advertising law, consumer rights), eu (GDPR, ePrivacy), both.
  Includes a technical detector for third-party scripts, checklists with severity, and assembly
  of a legal document pack from templates.
  Use when: "проверь сайт на соответствие закону", "аудит сайта 152-ФЗ",
  "нужна политика конфиденциальности", "составь юридические документы для сайта",
  "website legal audit", "GDPR compliance check", "проверь сайт на персональные
  данные", "соответствует ли сайт закону".
---

# Website Legal Audit

> ⚠️ Не юрист. Все выводы и документы — рабочий черновик под финальную проверку юристом.
> Законы меняются — перед сдачей сверяй даты и нормы (см. `Источники` в файлах веток).

The audit's outputs — reports, checklists and the document pack — are written in Russian for the
owner and their client. These instructions are not.

## What the skill does

1. Audits the site against presentation and disclosure requirements.
2. Produces a report: a "requirement / status / severity / legal basis" table.
3. Produces a remediation plan.
4. Assembles the missing legal documents from templates.

## Jurisdiction flag (required)

The skill is invoked with one of these flags, which decides which branch is loaded — nothing else
is pulled into context:

| Flag   | When                                      | Load               |
|--------|-------------------------------------------|--------------------|
| `ru`   | Audience and business in Russia only      | `ru/SKILL.md`      |
| `eu`   | Audience in the EU, GDPR applies          | `eu/SKILL.md`      |
| `both` | Both a Russian and an EU audience         | `both/SKILL.md`    |

No flag passed → ask the user: «РФ, ЕС или обе юрисдикции?» — and only then load the matching
branch. Do not read all branches at once.

## Process (common to every branch)

1. **Inputs** — site type (landing page / online shop / services), the audience's jurisdiction,
   which forms collect data, which third-party services are in use. Keep trivial questions to a
   minimum: whatever is visible on the site, find it yourself with the detector.
2. **Technical scan** — `common/detector.md`: third-party scripts (analytics, fonts, widgets),
   presence of a policy and links to it, cookie banner, hosting geolocation.
3. **Document review and checklist** — from the `references/` of the chosen branch, each item
   PASS / FAIL / N/A plus severity (blocker / major / minor).
4. **Technical report** — per `common/report-template.md` (for whoever implements the fixes).
5. **Remediation plan** — a prioritised list; where documents are missing, hand off to the
   assembler sub-skill in `<branch>/templates/` (variable questionnaire → filled document).
6. **Client report** — per `common/client-report.md`: short, in plain language, with references to
   the law (for the business owner).

## Navigation

- Technical detector: `common/detector.md`
- Technical report form: `common/report-template.md`
- Client report (non-technical): `common/client-report.md`
- Russia: `ru/SKILL.md`
- EU: `eu/SKILL.md`
- Both: `both/SKILL.md`

## Rules

- Severity follows risk: `blocker` — a direct fine or shutdown (no regulator notification, no
  consent, personal data held abroad); `major` — a breach without an immediate fine; `minor` —
  a recommendation or hygiene item.
- Every statement about a rule carries a reference to the law and the date of the revision. If a
  rule is out of date, say so and do not invent a replacement.
- Mark generated documents `draft: true` and attach the lawyer disclaimer.

## Checks against state

```bash
# 1. only the requested jurisdiction branch was loaded
rg -l "" ru/SKILL.md eu/SKILL.md both/SKILL.md

# 2. every generated document carries the draft flag and the disclaimer
rg -L "draft: true" <output-dir>/*.md

# 3. no checklist item was left without a severity
rg -n "FAIL" <report-path> | rg -v "blocker|major|minor"
```

Checks 2 and 3 must both return nothing. A document without the draft flag reads as legal advice,
and a FAIL without a severity gives the owner no way to decide what to fix first.
