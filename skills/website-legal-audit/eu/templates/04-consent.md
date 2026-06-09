---
doc: Consent record (GDPR-compliant)
norm: GDPR Art. 4(11), Art. 7
draft: true
vars: [CONTROLLER_NAME, CONTROLLER_EMAIL, SITE_URL, CONSENT_PURPOSE]
---

> ⚠️ Draft — lawyer review required. Consent must be freely given, specific,
> informed and unambiguous; as easy to withdraw as to give. Keep a record of who
> consented, when, to what, and how.

# Consent

By ticking this box I give my consent to {{CONTROLLER_NAME}} to process my
personal data for the following purpose: {{CONSENT_PURPOSE}}.

I understand that:
- this consent is voluntary and not a condition of using {{SITE_URL}} unless
  strictly necessary;
- I can withdraw it at any time by contacting {{CONTROLLER_EMAIL}}, without
  affecting the lawfulness of processing before withdrawal;
- details are in the Privacy Policy.

☐ I consent to the processing described above   ← single purpose, not pre-ticked

---

## Consent log (store internally, Art. 7(1))

| Field | Value |
|-------|-------|
| Subject identifier | ... |
| Purpose | {{CONSENT_PURPOSE}} |
| Timestamp | ... |
| Consent text version | ... |
| Method (form/URL) | ... |
| Withdrawn (date) | ... |
