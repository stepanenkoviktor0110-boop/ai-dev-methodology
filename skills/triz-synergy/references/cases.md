# Worked cases

Four cards from one project, worked through 2026-07-28, and a fifth from 2026-08-09. Four cases
resolved and verified, one a failure of the method — it is here not for completeness but because it
shows the main way to fake a resolved contradiction.

One further card, from a different project and dated 2026-08-05, is the case for the validation gate
(step 6 of [triz-combinatorics](../../triz-combinatorics/SKILL.md)). It is deliberately left
unnumbered and stands after the failure: it records not a resolved contradiction but what the gate
catches in a cover that already looked finished.

One further worked case — layer priority — has no verification, so it gets no card here; it is
worked through in [moves.md](moves.md), move 2. The silent refusal in the log, move 5, had none
either until 2026-08-09, when the same move was worked a second time with a measurement; that second
run is card 4 above.

Six cases in total, four with a recorded check, three of those numeric — case 1's check is a live
dialogue, not a figure.

Figures and wording are as in the source material. They have not been rewritten for elegance: the
value lies precisely in the real numbers and the real mistake.

**Where cards come from.** Every run leaves a file in the local store,
`~/.claude/triz-runs/<YYYY-MM-DD>-<slug>.md`, whose fixed sections are specified in step 6 of
[triz-combinatorics](../../triz-combinatorics/SKILL.md). Sections 1, 2, 3, 4 and 6 of that file are
the five fields of a card here — contradiction, IFR, resource, move, check — so a card is a
selection out of the run file rather than a retelling of it. The run files are not
committed — they describe other people's codebases — so cards are copied here, not linked.
All the cards below except case 4 predate that convention and have no run file behind
them; case 4 is the one card ever taken from a run file — `2026-08-09-triz-on-itself.md`.
When reading check 4 of [SKILL.md](../SKILL.md), that is the offset to subtract.

## Summary table

| Contradiction | IFR | Resource | Check |
|---|---|---|---|
| The guard must be strict (let no invented price through) and lenient (not cut the genuine ones) | a price cannot end up attached to the wrong product | the product name, which the model reproduces verbatim | live dialogue: the foreign price was gone, the cutting stopped |
| A value is human-readable and serves as the comparison key | comparing display forms is impossible | whitespace collapsing, living for years in a neighbouring module | 0 out of 8 → 8 out of 8 across eight phrasings |
| The guard suppresses enumeration and does not suppress the requested listing | a list of five products physically cannot count as enumeration | structure of the string: item link + price = a result | five cards pass the threshold, six sections do not |
| Behaviour is uniform for everyone and different for the client | the conflict is unexpressible | — | **not confirmed**: the IFR turned out to be an illusion, see below |
| The trigger must fire only by hand and must fire without the owner | a visible sign that goes unnoticed is unexpressible | the conditional line the session summary already prints | fires on 2 repositories of 4, silent on the 2 whose ratios rest on 2–3 commits |

---

## Case 1. Strict and lenient at the same time

**Contradiction.** The guard must be strict — let no invented price through — and lenient — not
cut the genuine ones. The dial was turned both ways, and both ways were wrong.

**IFR.** A price cannot end up attached to the wrong product.

**Resource.** The product name, which the model reproduces verbatim. The key was already in the data.

**Move.** Bind to the owner + do it the other way round: the fact is obtained by the object's key
rather than looked for nearby. A check of "does such a number occur at all" catches invention and
lets substitution through — and substitution is the worse case, because it looks credible. After
binding to the owner, the class of defect stopped existing rather than starting to be detected.

**Check.** Live dialogue: the foreign price was gone, the cutting of genuine ones stopped.

---

## Case 2. Readable by a human and serving as a key

**Contradiction (physical).** A value must be readable by a human and simultaneously serve as a
comparison key that survives retyping. One string cannot be both.

**IFR.** Comparing display forms is impossible.

**Resource.** Whitespace collapsing, living for years in a neighbouring module. Reused one to one.

**Move.** Separation in structure + mediator: a separate comparison key, a separate display form.
The collapsing touches formatting only; a difference of substance stays a difference.

**Check.** Eight phrasings of one thought: **0 out of 8** before the fix, including the
unambiguous one, **8 out of 8** after, by the same experiment. That experiment is worked through as
the exemplary one in SKILL.md, section "Discriminating experiment"; only the figures are recorded here.

---

## Case 3. Suppress enumeration, do not suppress what was asked for

**Contradiction.** The guard must suppress enumeration and simultaneously not suppress the listing
it asked for itself.

**IFR.** A list of five products physically cannot count as enumeration.

**Resource.** Structure of the string: item link + price = a delivered result. A choice option has
one or the other. The distinguishing feature was already in the data; it simply was not read.

**Move.** Separation on condition + local quality: the threshold applies to sections and does not
apply to product cards.

**Check.** A boundary experiment on both sides: five cards pass the threshold, six sections do not.

**What it teaches.** The resource lay not in the code but in the structure of the input. Grep over
the code does not find it — an inventory of real examples of each class does (step 3b of the
procedure).

---

## Failure of the method

**What was stated.** The IFR "make the contradiction unexpressible": if the client layer is a set
of declared values rather than free prose, a contradicting phrase has nowhere to live.

**What the validator showed.** An illusion. **A slot is a string too**, and a rule can be written
into it exactly the same way. The contradiction did not disappear, it moved from one field to
another.

**What actually provided the protection.** Not the schema but the detector — that is, an ordinary
check. And it could have been hung on the existing prose, with no migration at all.

**Lesson.** After stating the IFR, ask yourself the control question:

> Did the harmful outcome become IMPOSSIBLE — or did I just move it somewhere else?

If it moved, this is not a resolution but a rearrangement. It sounds cheap and costs dearly: a
rearrangement looks like an elegant TRIZ solution and drags a migration behind it that solves
nothing.

**Operational form of the check** (step 2 of the procedure): state a negative test — a check for
the harmful outcome — that after the solution becomes impossible to write. If the test can still be
written, merely for a different field, it is a rearrangement.

Note whose finding this was: **the validator's**. The illusion was not spotted by the person who
stated the IFR — it never is. That is the case for the gate below.

---

## Case 4. Only by hand, and without the person

**Contradiction (physical).** One trigger must be closed to automatic invocation — the procedure is
expensive and its failure mode is producing a plausible TRIZ shape — and open to automatic
recognition, because the sign is visible exactly when the person is busy with the bug.

**IFR.** A visible sign that goes unnoticed is unexpressible. Honestly: **this one moved rather than
disappeared.** A detector can miss. Recorded as a separation, not a removal.

**Resource.** The end-of-session summary already prints one conditional line to the owner. No new
branch was needed in the skill that hosts it — the shape existed.

**Move.** Separation by relation + mediator + feedback: the executor gets a detector, the owner keeps
the launch. The detector names a file and stops.

**Check.** Four repositories. Fires where contradictions were really worked — `answer_guard.py`
26/36 = 72% against a 27% baseline, `deploy.yml` 11/16 = 69% against 15% — and silent where the
ratio rests on two or three commits. Discriminating, not confirming: under "it is only activity",
`config.py` and `cli.py` at 50 commits each would rank with `criteria_navigator.py` at 55; they sit
at 26% and 32% while it sits at 71%.

**What it teaches.** The first form of the signal was rejected by a validator as a claim with no case
behind it, and the validator was right: measured, the raw `fix:` count is noise. The signal that
survived carries two guards that came out of the measurement rather than out of taste — a baseline
per repository, because baselines ranged 5%–27%, and a floor of 8 fix commits. The move it belongs
to, "feedback", had no recorded check before this; it has one now.

---

## The validation gate: what it caught in a finished cover

A different project, 2026-08-05. An offline app that names the card to pay with at the till.
Contradiction: the record of a condition must be fully specified — otherwise the wrong card is
named — and must arise with almost no input, since it is retyped every month for every category of
every card.

Combinatorics gave a four-element cover, each part covered exactly once, three of the four moves on
ready material. It passed its own checklist. Then three validators were run over it.

**`skeptic` found nothing — and that was worth having.** It reproduced the matching logic
independently and recomputed every figure: 632 of 771 name matches, 139 misses each occurring
once, 44 of 51 cards without slots. All confirmed to the digit. An empty finding from the material
lens is what makes the consequence lens worth reading.

**`reality-checker` found the hole that invalidated the cover.** Two candidates cancelled each
other: one made monthly confirmation a single tap, the other made a validity date compulsory — so
the single tap either silently stamps a fresh date, which is exactly the IFR the document had
rejected a paragraph earlier, or demands the date and stops being a single tap. The parts table
showed nothing: each candidate closed its own part honestly. Also found: a hard dependency of the
monthly notification on the very screen being removed, and a new screen introduced by one candidate
while the summary advertised one screen fewer.

**`userspec-adequacy-validator` found the smuggled decision.** One of the four changed which cards
take part in the ranking at all. That is not a simplification of a form; it is a product decision,
and the project already had the precedent for how such a thing is recorded — a separate line in the
project document, not a bullet inside a UI task.

**Disagreement between validators, and how it was settled.** `reality-checker` claimed a figure had
been computed over data absent at runtime. `skeptic` had reproduced the mechanism and shown it had
not. The one that reproduced won. What survived from the objection was real all the same, and got
written beside the figure: 82% measures canonical names, while a person types by hand — a ceiling,
not a guarantee.

**What it teaches.** A cover is consistent by construction: the table is filled in, therefore it
looks complete. The gate checks what the table cannot represent — that the material exists, that
the candidates do not cancel one another outside their own cells, and that none of them is a
different kind of decision in disguise. Three of the five hole classes in step 6 come from this one
case; the mutual contradiction was the one that sent the work back to step 4.
