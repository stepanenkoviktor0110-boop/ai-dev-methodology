# Why the method is shaped this way

Provenance and justification, moved out of SKILL.md. The body is read on every invocation; this
file is read only when a rule there looks arbitrary and you want to know where it came from.

Nothing here is a step of the procedure. If you are executing a run, you do not need this file.

## Contents

- What the six cases are, and what "no move without a case" costs
- Reading the threshold: the known recipe, and the unknown subsystem
- Where the features of the separation table came from
- Why the forty classical moves are excluded
- The exemplary discriminating experiment, in full
- The method under other names in the project rules

---

## What the six cases are, and what "no move without a case" costs

Six cases in total, worked through 2026-07-28, 2026-08-05 and 2026-08-09. Several moves share one
case, so seven moves rest on six cases rather than on seven. Four carry a recorded check and **three
of those four are numeric** — eight phrasings 0/8 → 8/8; the boundary five cards / six sections; and
the recurring-defect ratio measured across four repositories. The fourth check is qualitative: a
live dialogue in which the foreign price was gone and the cutting of genuine ones stopped. One case,
layer priority, has no recorded check at all, which is why it gets no card in [cases.md](cases.md)
and is worked through in [moves.md](moves.md), move 2, instead.

That is the honest state of the evidence, and it is thinner than a table of seven moves suggests.
The rule that produces it — no move enters the toolkit without a case behind it — is what keeps
the skill from turning into a list of plausible TRIZ shapes. It also means the toolkit grows only
as fast as the method is actually used.

The competing reading is worth holding open: seven moves and six cases may simply mean the method
is needed rarely, not that it is starved. Nothing recorded so far discriminates between those two.

The one machine-dependent detail in the whole skill is the root of neighbouring projects used in
step 3a, which is substituted in per machine. Everything else is tied to no stack and no project.

## Reading the threshold: the known recipe, and the unknown subsystem

Two rows of the "do NOT call it" table get read wrongly more often than the rest.

**"A ready recipe is already known."** That row is only about a recipe **already known**. A
suspicion that a recipe exists somewhere does not take you out of the skill: whether it exists is
settled by the search inside step 3a, which is part of the procedure, not a precondition for
entering it.

**"The symptom drifts and even the guilty subsystem is unknown."** That row rules out an unknown
*subsystem*. When the subsystem is known but the specific object inside it is not, that is **not
grounds to leave**: the object is found in step 1 by a discriminating experiment. That is exactly
how it was found in the flagship case — the result "0 out of 8, including the unambiguous
phrasing" is what showed the object was the value string at reconciliation, not the model's
understanding of the text.

## Where the features of the separation table came from

The choosing features for the first three separation types — in structure, in time, on condition —
are taken from worked cases directly.

The feature for **separation by relation** was derived from the logging case. There was no direct
case for that type in the source material, so its feature is reasoned rather than observed — though
its move has carried a measurement since 2026-08-09, when the same move was worked a second time.

The weakest row is now **in time**: its move, prior action, still carries no check of any kind. That
is stated here rather than smoothed over.

## Why the forty classical moves are excluded

The full list of forty classical moves and the contradiction matrix are deliberately absent.

A move with no attached example from practice produces a plausible-looking TRIZ shape instead of a
resolved contradiction — the reader recognises the vocabulary, fills it in, and comes away with a
document that reads like a resolution and changes nothing. An unused list is worse than no list,
because it invites exactly that.

When a case with a real example appears, the move gets written into the toolkit together with its
example. That is the only way in.

## The exemplary discriminating experiment, in full

The rules for setting one up are in SKILL.md. This is the case they were derived from.

**The owner's hypothesis:** the bot does not understand the colloquial "up to about five thousand".

**The experiment:** eight phrasings of the same thought, from colloquial to the unambiguous "up to
5000 roubles", each on its own and inside a dialogue.

**The result: 0 out of 8**, including the unambiguous one.

That is precisely what discriminated the hypotheses. Had understanding been what broke, the
unambiguous phrasing would have worked. Not one worked — so the matter was not the words but the
reconciliation of the value. After the fix: **8 out of 8**, by the same experiment.

An experiment that only tests the favourite hypothesis will confirm it nearly always. The
diagnostic power comes entirely from the fact that under the second cause the result would have
differed.

## The method under other names in the project rules

The same method appears in the project rules under wording that predates this skill:

- "unsolvable = stop and check where this is already solved" — step 3;
- "go by experiment, not by contemplation" — step 5;
- "fix the cause of the class, not the consequence" — step 2;
- "blocker → root fix on the class" — the whole procedure.
