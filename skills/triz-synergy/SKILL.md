---
disable-model-invocation: true
name: triz-synergy
description: |
  Resolves contradictions in development: states a pair of mutually exclusive requirements
  on one object, hunts for a resource already present in the code and in the data,
  separates by structure / time / condition / relation, and settles the result with a
  discriminating experiment.
  On-demand only — invoke explicitly, when a sign of contradiction is visible.

  Use when: "триз", "triz", "разбор противоречия", "чиним одно — ломается другое",
  "фиксим A — падает B", "ручку крутят в обе стороны",
  "возврат одного и того же класса дефекта", "баг вернулся под новым лицом",
  "это ограничение платформы, только обходной путь"
---

# TRIZ synergy — resolving contradictions in development

Not TRIZ theory. A five-step procedure, a written toolkit of moves, and a mandatory settlement by
experiment. Every move rests on a real case that was worked through; no move without a case behind
it appears here. Tied to no stack and no project — it works anywhere there is code and data.

Provenance of every rule below — where it came from, how thin the evidence is, the exemplary
experiment in full, the mapping to the older project rules — is in
[references/rationale.md](references/rationale.md). Open it when a rule looks arbitrary; a run does
not need it.

## Threshold

Invoked on request; never picked up automatically. Call it when a **sign of contradiction**
is visible:

- fixing one thing breaks another;
- the dial gets turned both ways and both ways are wrong (stricter cuts the living, looser lets
  things through);
- the same class of defect returns wearing a new face after every fix;
- someone said "that's a platform / base-layer limitation, only a workaround is possible".

**Do NOT call it when:**

| Situation | Do this instead |
|---|---|
| The symptom drifts and even the guilty subsystem is unknown | coarse localisation first: logs, reproduction, bisect |
| An ordinary bug: one cause, one fix, nobody suffers | just fix it |
| Adding a capability that did not exist | tech-spec-planning / code-writing |
| An argument about priorities, deadlines, taste | not a contradiction in an object; the owner decides |
| A parameter needs tuning and both sides agree which way | tune it and measure |
| The whole surface of the decision is a handful of lines in a document you control | judge it directly. A pair of requirements can be stated truthfully over almost anything; that it **can** be stated is not the threshold |
| A ready recipe from a neighbouring project **is already known** | reproduce it one to one (global rule 3) |

The known-recipe row and the unknown-subsystem row are read wrongly more often than the rest;
neither takes you out of the skill as readily as it looks (rationale, "Reading the threshold").

Budget: two full passes of the procedure. If after the second the object of the contradiction
is not found, or no separation fits, record the outcome and leave for tech-spec-planning — the
method does not carry this one.

## Procedure: five steps

### Step 1. State the contradiction as a pair of requirements on one object

Not "it works badly", but "X must be A and simultaneously not-A". Until that is stated there is
nothing to resolve and you will be tuning parameters.

- **technical**: strengthening one property degrades another ("stricter filter → cuts the real ones");
- **physical**: one and the same element must hold mutually exclusive properties
  ("this string must be human-readable and be the comparison key").

Physical is the stronger form: it points directly at the separation. Always drive a technical
contradiction down to a physical one — ask "which specific element carries both requirements?".

**If the object is unknown, find it by a discriminating experiment, not by guessing.** Run the
experiment by the rules in the "Discriminating experiment" section; here it works as a locator:
list two competing causes, set up an observation that yields a different result under each, and
from the result work out which element carries both requirements. The same experiment is repeated in
step 5 after the fix.

**Done when:** the pair is written as two predicates over one value, and on a concrete example
it is visible that both cannot hold at once. If the predicates apply to different objects, this
is not a contradiction — leave the skill and record that explicitly.

### Step 2. State the ideal final result (IFR)

The formula: **"the problem solves itself, because the harmful outcome became IMPOSSIBLE"**.
Not "catch the error", but "make the error unexpressible".

The IFR need not be reachable — it sets the direction and rules out crutch solutions.

**Control question, immediately after stating the IFR:**

> Did the harmful outcome become impossible, or did I just move it somewhere else?

The real failure sits exactly here: the IFR "a slot instead of free prose" turned out to be an
illusion — **a slot is a string too**. Full account: [references/cases.md](references/cases.md),
"Failure of the method".

**Done when:** you have stated a negative test — a check for the harmful outcome — that after
the solution becomes **impossible to write**. If the test can still be written, only against a
different field, that is a rearrangement, not a resolution.

### Step 3. Look for a resource already present in the system

The best solution does not add an entity, it notices an unused one. The resource sits in two
different places, and they are searched differently.

#### 3a. Resource in the code — the search

Derive the queries from the step-1 statement rather than guessing. Take:

- the field names on both sides that are compared or that conflict;
- the name of the type/structure the object of the contradiction belongs to;
- the call site of the operation that breaks;
- vocabulary by problem class: canonicalisation — `normaliz|canonical|slug|trim|collapse|\s+`,
  thresholds — `limit|threshold|max_|quota`, priorities — `priority|override|precedence`,
  identity — `key|hash|fingerprint|dedup`;
- the name of the symptom as the owner says it.

```bash
# 1. Is the mechanism already solved nearby, in the current project?
rg -nS "<query from the list above>" --glob '!node_modules' --glob '!.git' .

# 2. Solved at neighbouring projects/clients on the same stack?
#    <PROJECTS_ROOT> — the root holding the other projects (on this machine "D:/МОИ ПРОЕКТЫ").
rg -nlS "<query>" --glob '!node_modules' --glob '!.git' "<PROJECTS_ROOT>"

# 3. Is there an account of it in the knowledge base and the methodology lessons?
#    -L is not optional: most skills are junctions, and without it ripgrep
#    walks past them. Measured 2026-08-09 — the bare form saw 2 files where
#    -L saw 12, and an empty result here is recorded as a result.
rg -L -nlS "<symptom|mechanism name>" ~/.claude/skills
```

Found a ready mechanism — **reproduce it one to one, do not improve it by your own theory**.
Reproduce first, optimise after (global rule 3).

#### 3b. Resource in the data — inventory of the input

Grep finds mechanisms but does not find discriminators: those live in the structure of the
input, and are usually simply never read. What to do:

1. collect 3–5 **real** examples of each input class the method must tell apart;
2. write out the actual fields and shape of each — not from the schema and not from memory, but
   as it arrived;
3. find the minimal feature present in every example of class A and in no example of not-A;
4. no such feature — record that explicitly: separation on condition is impossible on this data,
   move to the other separation types;
5. real examples unobtainable (reproduces only in production, logs not retained) — record that
   explicitly and stop 3b. Synthetic examples in place of real ones yield a fictitious feature:
   it will separate an invention, not the real populations.

That is how the resource was found in the enumeration-threshold case: a product card has both a
link to the item and a price, while a choice option has one or the other. The feature was in the
string; nobody had read it.

**Done when:** the results of both searches are named. An empty result is a result too — it gets
recorded explicitly rather than skipped.

### Step 4. Separate

The separation is the resolution of a physical contradiction. Four types, chosen by feature:

| Type | Choosing feature | Typical moves | Case |
|---|---|---|---|
| **in structure** | the requirements are placed on the object "as a whole", but the object splits into parts or representations | mediator, local quality | comparison key / display form |
| **in time** | the requirements are needed at different moments in the object's life | prior action | layer priority declared once |
| **on condition** | the requirements are needed for different inputs, and the data **already contains** a feature telling the inputs apart (found by step 3b) | local quality, ready resource | enumeration threshold: cards and sections |
| **by relation** | the object must be A for one consumer and not-A for another | feedback, mediator | silent refusal in the log |
| **no separation** | the object of the contradiction can be removed entirely: do not check the value, derive it from its owner | do it the other way round, bind to the owner | the guard and the price |

The fifth row is not "we picked nothing" — it is an outcome in its own right, and a stronger one
than any separation: there is nothing to separate once the carrier of the contradiction has
ceased to exist. It is tested like the others, by the control question of step 2.

Reaching it is not a matter of inspiration. Ask three questions in order, and answer each by naming
a thing or by "no":

1. can the **owner of the fact** supply it, so it is obtained by key rather than looked for nearby?
2. can something **already upstream** — a caller, a platform, a layer that ran earlier — carry it?
3. does a **change of conditions** remove the need for the value at all?

An unanswered question here is visible, which a decision to "remove the object" is not. The guard
case is the answer to the first: the price came from the product's key, and the class of defect
stopped existing rather than starting to be detected.

Separation by relation is often **implemented** structurally (two fields, two channels): the type
answers "why are we separating", the structure answers "with what".

Accounts of the cases in the last column: "comparison key" and "enumeration threshold" —
[references/cases.md](references/cases.md); "layer priority" and "silent refusal" —
[references/moves.md](references/moves.md), moves 2 and 5. The "in time" row is the weakest — no
check behind its move at all; the "by relation" feature was reasoned rather than observed, though its
move has carried a measurement since 2026-08-09.

One move closed the contradiction entirely — go to step 5, through the gate all the same. A single
move carries the same holes as a bundle: a resource that turns out not to exist, a consumer nobody
named, a change of behaviour dressed as a simplification.

Go to [triz-combinatorics](../triz-combinatorics/SKILL.md) for the minimal set in three cases: a
move is chosen but does not close everything; there are several candidates and it is unclear which
to take; **no row of the table fits while the step-3 search did yield a resource** — the last means
not a dead end but a bundle of several roles, and that is exactly how the guard case was solved.

**Done when:** a concrete artifact is named — a field, a function, a channel — along with the
place it will appear. If the type was chosen because an example looked similar rather than by
the feature, the type is not chosen: go back to step 1 and clarify which element carries both
requirements.

If no type fits and both step-3 searches came back **empty** — second pass of the procedure with
a different statement of the object; after the second pass, leave on budget. A resource was
found — that is a different branch, and it leads into combinatorics, not around the loop again.

### Step 5. Settle it by experiment, not by argument

**First the gate, then the experiment** — [triz-combinatorics](../triz-combinatorics/SKILL.md),
step 6: the chosen set written to a file, three validators over it, every finding with a verdict.
The gate is static and cheap, the experiment is live and dear, and a set whose material does not
exist will happily yield a measurement of a fantasy. A mutual contradiction found there sends you
back to step 4, not on to the experiment.

A statement without a discriminating experiment is a hypothesis, however elegant. The rules are
in the section below.

If the object was found by experiment in step 1 — repeat **that same** experiment, not a similar
one. If the object was known from the start, or the settling experiment is different in nature
(localisation looked for a cause, settlement measures a result) — set up a new discriminating
experiment by the rules of that section and record how it differs from the locating one.

Separately: list **every** point where the fixed operation lives, and apply the solution at all of
them, as a line `Applied at:` naming each. One call site fixed out of three existing ones will bring
the class of defect back, and that gets written down as "the method did not work".

**Lock it in with a test on the class, not on the case** — one that fails for any member of the
class, not only for the original example. A test that only pins the example lets the next member of
the same class through, which is indistinguishable from never having fixed it.

**Then write the result into `## 6. Check` of the same run file** — the one the gate already
required, at `~/.claude/triz-runs/<YYYY-MM-DD>-<slug>.md`. With that line the file holds all five
fields of a case card, and the card is taken from it by selection rather than written afresh: a
move with no case behind it never enters the toolkit, and a case that costs a separate act of
writing never gets written. A run abandoned on the two-pass budget is recorded the same way, under
what was tried — the method not carrying a contradiction is itself worth knowing.

## Toolkit

Seven moves. The wording is universal — applicable to any code and data; the "Example" column shows
how the move looked on a real case and does not bound its scope. A move that did not come out of one
pass over the table — open [references/moves.md](references/moves.md), where each carries a full
example: what was there, what was done, how it was checked.

| Trigger feature | The move | Example |
|---|---|---|
| About to add an entity — a field, a module, a service, a dependency — for the sake of one property | **ready resource**: first list what already exists nearby and goes unused; a solution that adds nothing is the stronger one | whitespace collapsing, living for years in a neighbouring module, closed the value reconciliation |
| The same condition is worked out afresh in every case, branches keep multiplying | **prior action**: move the resolution to an earlier stage where it is done once | layer priority declared once in the text itself instead of resolving the conflict in every case |
| One object must serve two incompatible consumers | **mediator**: introduce a derived object for the second function, leave the original alone. Acceptance: the derived value is idempotent, it erases only presentational difference, a difference of substance stays a difference, and it is computed symmetrically for both sides at one point | the comparison key alongside the display form |
| A single rule is applied to inputs that are different in kind | **local quality**: make the rule non-uniform — different parts or classes of input behave differently; the class feature comes from step 3b | the enumeration threshold applies to sections but not to product cards |
| Refusal is silent: events of different nature look identical and need opposite treatment | **feedback**: make the difference observable in the channel people actually look at | "the model got it wrong" and "we disagree with ourselves" separated in the log; a silent refusal does not count as a system error, which is why nobody goes looking for it |
| A value is checked "for plausibility", with no source | **bind to the owner**: obtain the value by the key of the owning object rather than looking for it nearby. Answers the question "where does the value come from" | a free-floating number can be neither confirmed nor refuted: a check of "does such a value occur" catches invention and lets substitution through, and substitution looks entirely credible |
| Writing a detector for a bad result | **do it the other way round**: do not catch the bad outcome, make it unproducible. Answers "catch or exclude"; often carried out by binding to the owner | the fact is obtained by the owner's key → the class of defect stopped existing rather than starting to be detected |

The forty classical moves and the contradiction matrix are **deliberately excluded**; a move enters
this table only together with its case.

## Discriminating experiment

**Rule: the experiment must DISCRIMINATE between hypotheses, not confirm the favourite one.**

How to set one up:

1. list at least two competing causes;
2. devise an observation that yields a different result under each;
3. run it on the narrowest mechanism, without the rest of the path;
4. intermittent behaviour — at least three clean runs;
5. after the fix — repeat **the same** experiment, not a similar one;
6. measure **both sides** of the contradiction and the new harm. A fix that improves the side you
   were watching while quietly giving up the other reads as a success when only one side is
   measured — and so does one that buys the trade with a fresh failure elsewhere. Name what would
   count as the other side being damaged before running it.

An experiment that only tests the favourite hypothesis will confirm it nearly always. The diagnostic
power comes from the fact that under the second cause the result would have differed. The exemplary
case — eight phrasings, 0 out of 8 before, 8 out of 8 after — is worked through in the rationale.

## Checks against state

```bash
RUN=~/.claude/triz-runs/<YYYY-MM-DD>-<slug>.md

# 1. the run file exists and carries all six sections
rg -c "^## [1-6]\. " "$RUN"

# 2. the experiment was run and its result written, not merely planned
rg -A3 "^## 6\. Check" "$RUN"

# 3. every point of application was enumerated
rg -n "^Applied at:" "$RUN"

# 4. does the toolkit actually grow from runs? settled runs, against cards on file
rg -l "^## 6\. Check" ~/.claude/triz-runs/*.md 2>/dev/null | wc -l
rg -c "^## Case " references/cases.md
```

Check 1 must print **6**. Fewer means a section is missing and the gate did not complete — the
missing number tells you which step to return to.

Check 2 must print a non-empty block. Empty means the settlement never happened or was never
recorded; the case card cannot be taken from the file and no move may enter the toolkit from it.

Check 3 must print exactly one line. Nothing means the call sites were never listed, which is the
known way the class of defect comes back after a fix that looked complete.

Check 4 is the standing measurement of whether this arrangement works, and it settles over time
rather than in one session. The two numbers must not diverge: a settled run that left no card means
the card cost a separate act of writing after all — which is exactly what putting the card's fields
inside the run file was meant to remove. Cards written before the local store existed are the known
offset; subtract them before reading the gap.

## Transitions

- one move was not enough, or a set is chosen → [triz-combinatorics](../triz-combinatorics/SKILL.md), then back to step 5;
- fix found → `code-writing`, test on the class first;
- the solution changes the architecture → `tech-spec-planning`; the same for leaving on the two-pass budget;
- the resolution turned out to be a repeatable lesson → `/quick-learning`;
- a ready recipe was found at a neighbouring client → reproduce it one to one, global rule 3.
