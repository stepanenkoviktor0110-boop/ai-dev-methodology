---
name: triz-combinatorics
description: |
  Finds the minimal set of moves that closes a contradiction entirely: decomposes the
  contradiction into parts, generates candidates in a fixed form, kills the unfit with
  binary filters, and takes the minimal cover. Added complexity is penalised, not paid for.
  Invoked from step 4 of the triz-synergy skill.

  Use when: "один ход не закрыл противоречие", "связка приёмов", "комбинация ходов",
  "какой вариант решения лучше", "несколько решений, непонятно какое",
  "минимальное решение", "оптимальный вариант"
---

# TRIZ combinatorics — the minimal set of moves

A continuation of step 4 of [triz-synergy](../triz-synergy/SKILL.md). There one move is chosen.
Here: what to do when one is not enough.

## Threshold

Come here if, at step 4 of the parent skill, the chosen move does not close the contradiction
entirely, or there are several candidates and it is unclear which to take.

A third entry: no row of the separation table fitted, but the step-3 search did yield a resource.
That is not a dead end — it is the sign of a bundle of several roles.

**One move closed the contradiction — stop. That is the optimum; combinatorics is not needed.**
Of the five worked cases, a bundle was needed in two.

## Form of a combination

A combination is not an arbitrary subset of moves but a tuple with fixed roles. The moves are not
interchangeable; they occupy different positions:

```
[goal] + [separation type | none] + [mechanism ×1..k] + [material]
```

| Role | What goes in | Can it be omitted |
|---|---|---|
| **goal** | "do it the other way round": the outcome is impossible, not caught | yes — then the contradiction is separated rather than removed |
| **separation type** | in structure / in time / on condition / by relation | yes — if the object of the contradiction disappears entirely |
| **mechanism** | mediator, local quality, feedback, prior action, bind to the owner | no — without a mechanism it is a slogan |
| **material** | a ready resource from step 3a/3b, or new code | no — the source is always named |

Material is filled in for every tuple, but only new code counts toward added entities: a ready
resource costs zero. Otherwise "minimal set" is unmeasurable — the same bundle counts as two
elements one time and three the next.

Every bundle actually observed; there are no others in the material:

- **the guard and the price**: goal "do it the other way round" + mechanism "bind to the owner" + material "the product name", no separation — the object disappeared;
- **the comparison key**: separation in structure + mechanism "mediator" + material "whitespace collapsing from a neighbouring module";
- **the enumeration threshold**: separation on condition + mechanism "local quality" + material "a feature in the structure of the string" — one mechanism, combinatorics was not needed.

## Step 1. Decompose the contradiction into parts

The parts come from the **pair of requirements of step 1**, not from the IFR: the IFR is a single
statement, one part follows from it, and the cover degenerates — every candidate closes
everything. The guard case has two parts, one per requirement of the pair: someone else's price
must not pass **and** the genuine one must not be cut. The IFR meanwhile stays the yardstick at
step 3, filter 1.

**Done when:** for every part, any candidate can be answered with "yes/no, it closes it". A part
that always gets "partially" is stated wrongly — split it further.

## Step 2. Generate candidates

Mechanically, by the form above. Mechanisms are taken **only** from the seven moves of
triz-synergy — an eighth invented on the spot has been checked by nothing.

Discard immediately: a mechanism that needs a feature in the data when the inventory of the input
(step 3b of the parent skill) did not find one.

**Done when:** every candidate is written as a tuple rather than a phrase, and all five rows of
the separation table have been gone through, including "no separation". However many candidates
came out, that is how many there are: padding with blanks to fill a quota means feeding the
step-3 filters garbage.

## Step 3. Kill the unfit

Binary elimination; there is no ranking here. A candidate is out entirely if at least one holds:

1. the harmful outcome after it is not removed but relocated (the control question of step 2 of the parent skill);
2. no discriminating experiment can be devised that would tell it apart from a neighbouring candidate — meaning it is a restatement, not a solution;
3. it needs data or a feature that the real examples do not contain.

Zero survivors — return to step 1 of triz-synergy: the object of the contradiction is named wrongly.

## Step 4. Minimal cover

A "candidate × part" table, marks for closes or does not.

1. take the candidate closing the most parts;
2. it closed them all — **stop, that is the answer**;
3. it did not — add whoever closes what is left uncovered. Not whoever is more elegant, not whoever you like;
4. repeat until no part is uncovered.

**Each part is covered by exactly one candidate.** Two candidates on one part is a sign that this
is one solution under two names (the characteristic case: separation "on condition" and the move
"local quality"). The extra one is removed; it is never free.

**Done when:** the set is minimal — removing any element leaves a part uncovered. Verified by
enumeration: take one out at a time and look.

## Step 5. Rank, if there are several minimal sets

The order is strict; compare on the first criterion that differs:

1. **removal beats separation** — a set carrying the "goal" role, after which the carrier of the contradiction disappears, wins over a set that only separates the contradiction into parts. At an equal count of entities this is the only thing that distinguishes them;
2. **how many entities it adds** — a ready resource beats new code, zero new entities beats one;
3. **how many application points** must be touched;
4. **what settles it** — is there a boundary experiment on both sides;
5. **cost of error** — applies only when no candidate removes the harmful outcome and the choice is among separating ones: then a detector over the existing text is cheaper than a migration and gives the same protection. Outside that condition the criterion does not work — in the guard case the detector was precisely the harm that filter 1 removes.

Sets indistinguishable on all five — take any and record that the choice was arbitrary. That is
more honest than inventing a fifth criterion to fit the desired answer.

## Exit

Return to step 5 of [triz-synergy](../triz-synergy/SKILL.md): the discriminating experiment on the
chosen set, application at every point, a test on the class.

## Checklist

1. Is the contradiction decomposed into parts on which a candidate is judged "yes/no"?
2. Is every candidate written as a tuple — goal, separation, mechanism, material?
3. Was binary elimination run before ranking rather than instead of it?
4. Is the set minimal — does the cover break when any element is removed?
5. Did two candidates for the same part end up in the set?
