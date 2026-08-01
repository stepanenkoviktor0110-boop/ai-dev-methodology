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

Not TRIZ theory. A five-step procedure, a written toolkit of moves, and a mandatory
settlement by experiment. Every move rests on a real case that was worked through; there are
five cases, and several moves share one case. No move without a case behind it appears here.

The skill is tied to no stack and no project: it works anywhere there is code and data. The
one machine-dependent detail is the root of neighbouring projects in step 3a, which is
substituted in.

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
| A ready recipe from a neighbouring project **is already known** | reproduce it one to one (global rule 3) |

That last row is only about a recipe already known. A suspicion that a recipe exists somewhere
does not take you out of the skill: whether it exists is settled by the search inside step 3a,
which is part of the procedure.

The first row rules out an unknown subsystem. When the subsystem is known but the specific
object inside it is not, that is **not grounds to leave**: the object is found in step 1 by a
discriminating experiment, which is exactly how it was found in the flagship case.

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
from the result work out which element carries both requirements. In the flagship case it was
exactly the result "0 out of 8, including the unambiguous phrasing" that showed the object was
the value string at reconciliation, not the understanding of the text. The same experiment is
repeated in step 5 after the fix.

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
rg -nlS "<symptom|mechanism name>" ~/.claude/skills
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

Separation by relation is often **implemented** structurally (two fields, two channels): the type
answers "why are we separating", the structure answers "with what".

Accounts of the cases in the last column: "comparison key" and "enumeration threshold" —
[references/cases.md](references/cases.md); "layer priority" and "silent refusal" —
[references/moves.md](references/moves.md), moves 2 and 5 (there is no numeric check for those in
the source material, which is the weakest point of the bottom two types).

> On where the features came from: the first three types are taken from worked cases directly.
> The feature for "by relation" was derived from the logging case — there was no direct case for
> that type in the source material.

One move closed the contradiction entirely — go to step 5. [triz-combinatorics](../triz-combinatorics/SKILL.md)
holds the minimal set of moves covering every part of the contradiction; go there in three cases:
a move is chosen but does not close everything; there are several candidates and it is unclear
which to take; **no row of the table fits while the step-3 search did yield a resource** — the
last means not a dead end but a bundle of several roles, and that is exactly how the guard case
was solved.

**Done when:** a concrete artifact is named — a field, a function, a channel — along with the
place it will appear. If the type was chosen because an example looked similar rather than by
the feature, the type is not chosen: go back to step 1 and clarify which element carries both
requirements.

If no type fits and both step-3 searches came back **empty** — second pass of the procedure with
a different statement of the object; after the second pass, leave on budget. A resource was
found — that is a different branch, and it leads into combinatorics, not around the loop again.

### Step 5. Settle it by experiment, not by argument

A statement without a discriminating experiment is a hypothesis, however elegant. The rules are
in the section below.

If the object was found by experiment in step 1 — repeat **that same** experiment, not a similar
one. If the object was known from the start, or the settling experiment is different in nature
(localisation looked for a cause, settlement measures a result) — set up a new discriminating
experiment by the rules of that section and record how it differs from the locating one.

Separately: list **every** point where the fixed operation lives, and apply the solution at all
of them. One call site fixed out of three existing ones will bring the class of defect back, and
that gets written down as "the method did not work".

## Toolkit

Seven moves. The wording is universal — applicable to any code and data; the "Example" column
shows how the move looked on a real case and does not bound its scope.

A move did not come out of one pass over the table — open [references/moves.md](references/moves.md):
each move there comes with a full example, what was there, what was done, how it was checked.

| Trigger feature | The move | Example |
|---|---|---|
| About to add an entity — a field, a module, a service, a dependency — for the sake of one property | **ready resource**: first list what already exists nearby and goes unused; a solution that adds nothing is the stronger one | whitespace collapsing, living for years in a neighbouring module, closed the value reconciliation |
| The same condition is worked out afresh in every case, branches keep multiplying | **prior action**: move the resolution to an earlier stage where it is done once | layer priority declared once in the text itself instead of resolving the conflict in every case |
| One object must serve two incompatible consumers | **mediator**: introduce a derived object for the second function, leave the original alone. Acceptance: the derived value is idempotent, it erases only presentational difference, a difference of substance stays a difference, and it is computed symmetrically for both sides at one point | the comparison key alongside the display form |
| A single rule is applied to inputs that are different in kind | **local quality**: make the rule non-uniform — different parts or classes of input behave differently; the class feature comes from step 3b | the enumeration threshold applies to sections but not to product cards |
| Refusal is silent: events of different nature look identical and need opposite treatment | **feedback**: make the difference observable in the channel people actually look at | "the model got it wrong" and "we disagree with ourselves" separated in the log; a silent refusal does not count as a system error, which is why nobody goes looking for it |
| A value is checked "for plausibility", with no source | **bind to the owner**: obtain the value by the key of the owning object rather than looking for it nearby. Answers the question "where does the value come from" | a free-floating number can be neither confirmed nor refuted: a check of "does such a value occur" catches invention and lets substitution through, and substitution looks entirely credible |
| Writing a detector for a bad result | **do it the other way round**: do not catch the bad outcome, make it unproducible. Answers "catch or exclude"; often carried out by binding to the owner | the fact is obtained by the owner's key → the class of defect stopped existing rather than starting to be detected |

Checking "do it the other way round" for a fake is the same control question from step 2: did the
outcome become impossible, or did it move?

The full list of forty classical moves and the contradiction matrix are **deliberately excluded**:
a move with no attached example from practice produces a plausible-looking TRIZ shape instead of a
resolved contradiction, and an unused list is worse than no list. When a case with an example
appears, the move gets written in here together with its example.

## Discriminating experiment

**Rule: the experiment must DISCRIMINATE between hypotheses, not confirm the favourite one.**

How to set one up:

1. list at least two competing causes;
2. devise an observation that yields a different result under each;
3. run it on the narrowest mechanism, without the rest of the path;
4. intermittent behaviour — at least three clean runs;
5. after the fix — repeat **the same** experiment, not a similar one.

**The exemplary case.** The owner's hypothesis: the bot does not understand the colloquial "up to
about five thousand". The experiment: eight phrasings of the same thought, from colloquial to the
unambiguous "up to 5000 roubles", each on its own and inside a dialogue.

The result — **0 out of 8**, including the unambiguous one. That is precisely what discriminated
the hypotheses: had understanding been what broke, the unambiguous phrasing would have worked. Not
one worked — so the matter was not the words but the reconciliation. After the fix — **8 out of 8**
by the same experiment.

An experiment that only tests the favourite hypothesis will confirm it nearly always. The
diagnostic power comes from the fact that under the second cause the result would have differed.

## Checklist

1. Is the contradiction stated as a pair of requirements on one object?
2. Is a physical contradiction named, not only a technical one?
3. Is the IFR written in the form "the harmful outcome is impossible"?
4. Was it checked that the IFR does not merely move the problem?
5. Was the search for a ready resource run — in the code (`grep` across neighbouring modules and clients) and in the structure of the data?
6. Was the separation type chosen deliberately — by its feature, not by resemblance to an example?
7. Was an experiment set up that discriminates between hypotheses rather than confirming the favourite?
8. Was the same experiment repeated after the fix, and was the solution applied at every point?
9. Is the solution locked in by a test on the **class** rather than on the case — one that fails for any member of the class, not only for the original example?

An unanswered item is not "we skipped it" but a stop: go back to the corresponding step.

## Transitions

- one move was not enough → [triz-combinatorics](../triz-combinatorics/SKILL.md), then back to step 5;
- fix found → `code-writing` (test on the class first, checklist item 9);
- the solution changes the architecture → `tech-spec-planning`; the same for leaving on the two-pass budget;
- the resolution turned out to be a repeatable lesson → `/quick-learning`;
- a ready recipe was found at a neighbouring client → reproduce it one to one, global rule 3.

The method under other names in the project rules: "unsolvable = stop and check where this is
already solved" — step 3; "go by experiment, not by contemplation" — step 5; "fix the cause of the
class, not the consequence" — step 2; "blocker → root fix on the class" — the whole procedure.
