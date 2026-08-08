# Moves with full examples

The expanded version of the "Toolkit" table from SKILL.md. Open it when a move did not come out of
one pass over the table.

Each move: trigger feature → the move → an example in three parts (what was there, what was done,
how it was checked). All examples are real cases from one project, worked through 2026-07-28.
Where the source material records no check, that is said outright rather than filled in.

---

## 1. Ready resource

**Trigger feature.** About to add an entity — a field, a module, a service, a dependency — for the
sake of one property.

**The move.** Before adding an element, list what already exists nearby and goes unused: a field, a
key, a structure, a ready function in a neighbouring module, an invariant of the data. A solution
that adds nothing is stronger than one that adds.

**Example.**
- *What was there.* Values failed to reconcile because of formatting. The obvious pull was to write
  a normalisation of our own for this case.
- *What was done.* Found the whitespace collapsing that had lived for years in a neighbouring
  module and reused it one to one, rather than rewriting it "more correctly".
- *How it was checked.* The same experiment with eight phrasings: 0 out of 8 before, 8 out of 8 after.

**Link to the rule.** The mechanism is already solved somewhere → reproduce it one to one, optimise
after (global rule 3). Departing from a working recipe on an unverified theory is a known rake, not
an improvement.

---

## 2. Prior action

**Trigger feature.** The same condition is worked out afresh in every case, branches keep multiplying.

**The move.** Move the resolution of the conflict to an earlier stage where it is done once. The
conflict is resolved before it arises.

**Example.**
- *What was there.* Layers overlapped; residual overlaps will always exist, and each had to be
  worked out separately — the set of special cases kept growing.
- *What was done.* Declared the priority once in the text itself, instead of resolving the conflict
  in every case. The implicit was made explicit, once.
- *How it was checked.* No separate check of this move is recorded in the source material. The move
  is counted among those that worked, but no figures were given for it.

**Not to be confused** with the failed attempt to remove the same conflict by migrating prose into a
schema — that is a different move with a different result, worked through in [cases.md](cases.md),
section "Failure of the method".

---

## 3. Mediator

**Trigger feature.** One object must serve two incompatible consumers.

**The move.** Introduce a derived object for the second function; leave the original alone.

**Acceptance conditions for the derived value** are in the "Toolkit" table of SKILL.md, row
"mediator". Without them the move produces a new defect in place of the old one: too aggressive a
normalisation yields false matches.

**Example.**
- *What was there.* A value had to be readable by a human and simultaneously serve as a key that
  survives retyping. One string cannot be both: comparing display forms produces a divergence where
  there is no difference of substance.
- *What was done.* Split them: a separate comparison key, a separate display form. The collapsing
  touches formatting only.
- *How it was checked.* Eight phrasings of one thought: 0 out of 8 → 8 out of 8 after the fix, by
  the same experiment.

---

## 4. Local quality

**Trigger feature.** A single rule is applied to inputs that are different in kind.

**The move.** Make the rule non-uniform: different parts of the object, or different classes of
input, behave differently.

**Example.**
- *What was there.* The guard had to suppress enumeration and simultaneously not suppress the
  listing it asked for itself. Stricter cuts what was asked for, looser lets enumeration through.
- *What was done.* The distinguishing feature was already in the structure of the string: a product
  card has both an item link and a price; a choice option has one or the other. The resource was in
  the data, it simply was not read. The threshold was applied to sections and not to cards.
- *How it was checked.* A boundary experiment on both sides: five cards pass the threshold, six
  sections do not.

---

## 5. Feedback

**Trigger feature.** Refusal is silent: events of different nature look identical and need opposite
treatment.

**The move.** Make the difference observable in the channel people actually look at.

**Example.**
- *What was there.* Two different events — "the model got it wrong" and "we disagree with
  ourselves" — looked identical. A silent refusal is not a system error, so nobody goes looking for
  it: it does not crash, is not logged as a failure, does not reach the metrics.
- *What was done.* Separated the two events in the log.
- *How it was checked.* No check of this move is recorded in the source material.

**Second example, 2026-08-09, with a check.** A sign of contradiction is visible during ordinary
work — the same file keeps being repaired — but the person seeing it is busy with the bug and does
not call the method. The channel people actually look at is the end-of-session summary.

- *What was there.* The proposed difference was a raw count of `fix:` commits. Measured, it is not a
  difference at all: one repository showed 67% built from two fixes out of three.
- *What was done.* Made the difference observable as a ratio against the repository's own baseline,
  with a floor of 8 fix commits, printed as one line where a conditional line was already printed.
  It names the file; it never invokes anything.
- *How it was checked.* Four repositories. Fires on the two carrying real contradictions —
  `answer_guard.py` at 72% against a 27% baseline, `deploy.yml` at 69% against 15% — and silent on
  the two whose high ratios rest on two or three commits. It is not activity: `config.py` and
  `cli.py` carry 50 commits each, as many as `criteria_navigator.py` at 55, and sit at 26% and 32%
  while the navigator sits at 71%. The two files it ranks highest are the ones behind cases 1 and 3
  of [cases.md](cases.md) — found by hand at the time, named by the signal from history alone.

---

## 6. Bind to the owner

**Trigger feature.** A value is checked "for plausibility", with no source.

**The move.** Obtain the value by the key of the owning object rather than looking for it nearby.
Answers the question "where does the value come from".

**Why a presence check is weaker.** A free-floating value can be neither confirmed nor refuted — it
has no owner. A check of "does such a value occur at all" catches invention and **lets substitution
through**. Substitution is worse than invention: it looks credible, because the value is genuine —
just not from that object.

**Example.**
- *What was there.* The guard had to be strict — let no invented price through — and lenient — not
  cut the genuine ones. The dial was turned both ways, and both ways were wrong.
- *What was done.* Bound the fact to its owner: the price is obtained by the product's key. The
  resource turned out to be the product name, which the model reproduces verbatim.
- *How it was checked.* Live dialogue: the foreign price was gone, the cutting of genuine ones
  stopped.

---

## 7. Do it the other way round

**Trigger feature.** Writing a detector for a bad result.

**The move.** Do not catch the bad outcome, make it unproducible. Answers the question "catch or
exclude". Often carried out by move 6: binding to the owner is a way of making the outcome
unproducible.

**Example.**
- *What was there.* The task was stated as "catch the wrong price" — that is, a detector was being
  built.
- *What was done.* Turned it over: the price is obtained by the object's key rather than looked for
  nearby. After that the class of defect **stopped existing rather than starting to be detected**.
- *How it was checked.* The same live dialogue as in move 6.

**Checking the move for a fake.** The control question of step 2: did the outcome become impossible,
or did I just move it somewhere else? The failure of the method happened on exactly a fake of this
move — [cases.md](cases.md), section "Failure of the method".
