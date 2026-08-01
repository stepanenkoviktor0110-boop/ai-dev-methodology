# Worked cases

Four cards from one project, worked through 2026-07-28. Three cases resolved and verified, one a
failure of the method — it is here not for completeness but because it shows the main way to fake
a resolved contradiction.

Two further worked cases — layer priority and the silent refusal in the log — have no numeric
verification, so they get no cards here; they are worked through in [moves.md](moves.md), moves 2
and 5. Five cases in total, three of them with a recorded check.

Figures and wording are as in the source material. They have not been rewritten for elegance: the
value lies precisely in the real numbers and the real mistake.

## Summary table

| Contradiction | IFR | Resource | Check |
|---|---|---|---|
| The guard must be strict (let no invented price through) and lenient (not cut the genuine ones) | a price cannot end up attached to the wrong product | the product name, which the model reproduces verbatim | live dialogue: the foreign price was gone, the cutting stopped |
| A value is human-readable and serves as the comparison key | comparing display forms is impossible | whitespace collapsing, living for years in a neighbouring module | 0 out of 8 → 8 out of 8 across eight phrasings |
| The guard suppresses enumeration and does not suppress the requested listing | a list of five products physically cannot count as enumeration | structure of the string: item link + price = a result | five cards pass the threshold, six sections do not |
| Behaviour is uniform for everyone and different for the client | the conflict is unexpressible | — | **not confirmed**: the IFR turned out to be an illusion, see below |

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
