---
name: triz-combinatorics
description: |
  Finds the minimal set of moves that closes a contradiction entirely: decomposes the
  contradiction into parts, generates candidates in a fixed form, kills the unfit with
  binary filters, and takes the minimal cover. Added complexity is penalised, not paid for.
  Invoked from step 4 of the triz-synergy skill. Also holds the validation gate — step 6 —
  which runs before any experiment and applies even when a single move closed the
  contradiction and no combination was needed.

  Use when: "один ход не закрыл противоречие", "связка приёмов", "комбинация ходов",
  "какой вариант решения лучше", "несколько решений, непонятно какое",
  "минимальное решение", "оптимальный вариант", "проверить решение перед экспериментом",
  "прогнать валидаторов по решению"
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

## Step 6. Validation gate

The cover is internally consistent **by construction**: every part got a mark. That says nothing
about whether the named resources exist, whether two candidates cancel each other outside the
table, or whether one of them is a separate decision wearing the costume of a move. Those are the
holes the table cannot represent, and every class of them listed below comes from one worked case:
"The validation gate" in the parent skill's [cases.md](../triz-synergy/references/cases.md).

Why a validator rather than another pass by the author: the "failure of the method" in that same
file was also a validator's finding. Whoever stated the IFR does not see its illusion — that is the
one regularity both cases share.

**Precondition: the cover is written to a file, not left in the dialogue.** Validators read
artifacts.

**Where.** `~/.claude/triz-runs/<YYYY-MM-DD>-<slug>.md` — a local store, outside every project and
outside the methodology repository, never committed. A run describes someone else's codebase and
usually their business detail; neither belongs in a published repo. The path is the same wherever
the run happens, so a contradiction met mid-bugfix in any project has somewhere to go without that
project needing a scaffold of its own.

**Headings are fixed**, because the checks below and the case card both read them by name:

| Heading | What it carries, and why it earns its place |
|---|---|
| `## 1. Requirements and IFR` | the pair from step 1 and the IFR |
| `## 2. Candidates` | every candidate as its tuple, material named as a **checkable fact** — file, function, figure. "A ready resource exists" is not checkable; "`significantWords`, called only from `repairOrphanCategories`" is |
| `## 3. Parts` | the parts table, and which candidate covers which |
| `## 4. Constraints` | the project's obvious limits, written as boundaries rather than wishes. Without them no validator can tell a simplification from a demolition, and the one question the owner actually cares about goes unanswered |
| `## 5. Gate` | validator findings, each with a verdict |
| `## 6. Check` | filled at step 5 of triz-synergy, after the experiment |

Sections 1 and 2 plus section 6 are exactly the five fields of a card in
[cases.md](../triz-synergy/references/cases.md) — Contradiction, IFR, Resource, Move, Check — so a
finished run yields its card by selection, not by retelling. Sections 3, 4 and 5 stay in the run
file; a card has no counterpart for them and does not need one.

Three lenses, run in parallel:

| Validator | Lens | What it answers |
|---|---|---|
| `skeptic` | material | Does every named resource exist, and is it unused for what the tuple claims? Figures recomputed, not trusted |
| `reality-checker` | consequences | What has to be touched, what breaks for someone who already has the thing installed, which consumers are hit that the cover never names |
| `userspec-adequacy-validator` | proportion | Is each candidate solving a real problem or simplifying for its own sake; is anything here a separate decision smuggled in as a move |

Classes of hole, each one observed:

| Class | How it looks | What it costs |
|---|---|---|
| **mutual contradiction inside the cover** | two candidates each close their part and cancel one another | the cover is invalid — **back to step 4** |
| **a smuggled decision** | a candidate changes behaviour rather than the carrier of the contradiction | out of the bundle, into a decision of its own with its own record |
| **an unnamed consumer** | something depends hard on the element being removed | either it survives as a target, or the cover grows by the rework — and stops being minimal |
| **an entity claimed as removed** | the summary says "one screen fewer" while a candidate adds one | recount: the count is part of the claim |
| **a ceiling read as a guarantee** | a figure measured on canonical data, applied to input typed by hand | the figure stays, its scope gets written beside it |

Rules:

- **a mutual contradiction sends you back to step 4, not on to step 5.** The other classes are
  recorded and reshape the plan without invalidating the cover.
- **validators disagree with each other.** Prefer the one that reproduced the mechanism over the one
  that reasoned about it. Record the disagreement and how it was settled — an unrecorded one comes
  back later as a fact.
- an empty finding is a result, not a failed run.

**Done when:** every finding carries a verdict — folded into the plan, or rejected with a reason. A
finding left without a verdict is a stop.

## Exit

Through the gate of step 6, then return to step 5 of
[triz-synergy](../triz-synergy/SKILL.md): the discriminating experiment on the chosen set,
application at every point, a test on the class.

The order matters, and why it does is stated once, in step 5 of the parent skill.

## Checks against state

```bash
RUN=~/.claude/triz-runs/<YYYY-MM-DD>-<slug>.md

# 1. the four pre-gate sections exist
rg -c "^## [1-4]\. " "$RUN"

# 2. constraints were written as boundaries, not left as a heading
rg -A20 "^## 4\. Constraints" "$RUN" | rg -c "^[0-9]+\.|^- "

# 3. all three validators are named in the gate section
rg -c "skeptic|reality-checker|userspec-adequacy-validator" "$RUN"

# 4. no finding was left with an empty verdict cell
rg -n "^\|[^|]*\|[^|]*\| *\|" "$RUN"
```

Check 1 must print **4** before the gate is run at all; a missing section is the step to go back to.

Check 2 must print **at least 1**. Zero means no validator can tell a simplification from a
demolition, and the gate will read as passed while answering the wrong question.

Check 3 must print **at least 3**. Fewer means a lens was skipped — and the lens that finds nothing
is what makes the others worth reading.

Check 4 must return **nothing**. Any row it prints is a finding without a verdict, which is a stop
by the rule above, not a formality.
