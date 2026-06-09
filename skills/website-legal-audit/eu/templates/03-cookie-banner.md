---
doc: Cookie banner — текст и логика (opt-in, reject-all)
norm: ePrivacy Art. 5(3); GDPR Art. 4(11), 7; EDPB
draft: true
vars: [SITE_URL]
---

> ⚠️ Draft — lawyer review required. Это не документ на страницу, а спецификация
> баннера для разработчика: текст + обязательная логика.

# Cookie banner specification

## Required behaviour (иначе нарушение)

1. **Prior consent**: non-essential cookies/scripts (analytics, marketing,
   embeds) MUST NOT load until the user consents. Strictly necessary cookies —
   allowed without consent.
2. **Reject all**: a "Reject all" button with the SAME visual prominence as
   "Accept all" (size, colour, position). No reject hidden on a second layer.
3. **No pre-ticked** category toggles. All off by default except strictly
   necessary.
4. **Granular**: user can accept/reject per category (Functional / Analytics /
   Marketing).
5. **No dark patterns**: do not colour "Accept" to dominate, do not nag-loop.
6. **Withdrawable**: a persistent "Cookie settings" link lets users change choice
   anytime.

## First-layer banner text

> **We value your privacy**
> We use cookies to run this site and, with your consent, to analyse traffic and
> personalise content. You can accept all, reject all, or choose categories.
> See our [Cookie Policy]({{SITE_URL}}/cookie-policy).
>
> [Reject all]   [Cookie settings]   [Accept all]
>
> (Three buttons of equal prominence; "Reject all" and "Accept all" identical in
> size and style.)

## Second-layer (settings)

> ☐ Functional cookies
> ☐ Analytics cookies
> ☐ Marketing cookies
> (Strictly necessary — always on, shown as locked.)
> [Save choices]
