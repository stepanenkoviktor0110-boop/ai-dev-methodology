---
doc: Privacy Policy (GDPR Art. 13/14)
norm: GDPR Art. 12-14
draft: true
vars: [CONTROLLER_NAME, CONTROLLER_ADDRESS, CONTROLLER_EMAIL, DPO_CONTACT, EU_REP, SITE_URL, DATA_CATEGORIES, PROCESSING_PURPOSES, LEGAL_BASIS, RECIPIENTS, RETENTION, INTL_TRANSFER, SUPERVISORY_AUTHORITY]
---

> ⚠️ Draft — have a lawyer review before publishing. Fill all `{{...}}`. Keep
> blocks marked "[if ...]" only when the condition holds.

# Privacy Policy

Last updated: {{DATE}}

## 1. Who we are (Controller)

{{CONTROLLER_NAME}}, {{CONTROLLER_ADDRESS}}, is the data controller for personal
data processed via {{SITE_URL}}. Contact: {{CONTROLLER_EMAIL}}.

[if DPO_CONTACT] Data Protection Officer: {{DPO_CONTACT}}. [/if]
[if EU_REP] Our representative in the EU (Art. 27 GDPR): {{EU_REP}}. [/if]

## 2. What data we process

We process the following categories of personal data: {{DATA_CATEGORIES}}
(e.g. name, email, phone, usage and device data).

## 3. Purposes and legal bases

| Purpose | Legal basis (Art. 6) |
|---------|----------------------|
| {{PROCESSING_PURPOSES}} | {{LEGAL_BASIS}} |

Where we rely on legitimate interests, the specific interest is: {{LEGAL_BASIS}}
(describe concretely — "business purposes" is not sufficient).

## 4. Recipients

We share personal data with: {{RECIPIENTS}} (e.g. hosting provider, analytics
provider, payment processor), only as necessary for the purposes above.

## 5. International transfers

[if INTL_TRANSFER]
We transfer personal data outside the EU/EEA to {{INTL_TRANSFER}}. Such transfers
are safeguarded by an adequacy decision or Standard Contractual Clauses (SCC) per
Art. 44–49 GDPR. A copy of the safeguards is available on request.
[/if]
[if !INTL_TRANSFER] We do not transfer personal data outside the EU/EEA. [/if]

## 6. Retention

We keep personal data for: {{RETENTION}} (period or criteria). After that it is
deleted or anonymised.

## 7. Your rights

You have the right to access, rectify, erase, restrict or object to processing,
and to data portability. Where processing is based on consent, you may withdraw
it at any time without affecting prior processing. To exercise your rights,
contact {{CONTROLLER_EMAIL}}; we respond within one month (Art. 12(3)).

## 8. Complaints

You may lodge a complaint with a supervisory authority: {{SUPERVISORY_AUTHORITY}}.

## 9. Cookies

We use cookies and similar technologies. See our Cookie Policy at
{{SITE_URL}}/cookie-policy.

## 10. Changes

We may update this Policy; the current version is published at {{SITE_URL}}.
