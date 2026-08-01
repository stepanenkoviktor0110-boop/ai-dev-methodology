# Skill refinement patterns

What to change when touching a skill, and how to tell whether the change landed. Applies to
skill-trainer embedding rules, to skill-checker auditing, and to editing a skill by hand.

Each pattern: **trigger** — what you see; **do** — the change; **why** — what breaks without it;
**verify** — how to tell it worked.

## Contents

- P1 Split a closing checklist by class
- P2 State what each check's result must be
- P3 Name a user check as a user check
- P4 Route reviewers by artifact content, not by producer
- P5 Replace round counters with a convergence condition
- P6 No model and no effort in a skill body
- P7 English body; Russian only where the language is the content
- P8 Move accumulated lists out of the body
- P9 Every named skill, agent and command must exist
- P10 No machine-specific paths, no pinned versions
- P11 Documentation must match the repository
- P12 Fix the writers before the executors
- P13 Embed a lesson as a command when state can settle it
- P14 Update the conventions doc in the same pass

---

## P1. Split a closing checklist by class

**Trigger.** The skill ends with a checklist of tick-boxes (`## Self-Verification` or similar).

**Do.** Classify every item and act by class:

| Class | Recognised by | Action |
|---|---|---|
| machine | names an external artifact — a file, a frontmatter field, a commit, a lock, a CI run — whose state a command can read | keep, but rewrite as the command |
| reasoning | judges the quality or completeness of the executor's own work ("all phases completed", "every criterion is met") | delete |
| not a check | a rule copied out of the body of the same skill ("agents run in parallel", "max 2 entries") | delete; the rule stays in the body |

**Why.** An executor already reviews its own work; a written instruction to verify compounds with
that and buys nothing. And a rule restated as a tick-box catches nothing — whoever broke it in the
body will not catch themselves with a copy of it.

**Verify.** No `## Self-Verification` heading remains. Every line under `## Checks against state`
is a runnable command naming a path, a git invocation or an rg pattern.

## P2. State what each check's result must be

**Trigger.** A check block lists commands and stops there.

**Do.** After the block, say what each result has to be: the delta ("count 1 must have dropped by
the number of applied plus skipped triads"), or the required emptiness ("check 2 must return
nothing"), and what a mismatch means.

**Why.** A command whose output nobody interprets is decoration. The value is in knowing which
result is wrong, not in having run something.

**Verify.** Every check either carries an expected result or is self-evidently pass/fail.

## P3. Name a user check as a user check

**Trigger.** An item cannot be read off disk: visual fit on a page, contrast, "the layout looks
right".

**Do.** Say plainly that the user checks it, and at which step.

**Why.** Dressing an unverifiable item as an automated check hides the fact that nobody verified it.

**Verify.** No command in the check block claims to settle something visual.

## P4. Route reviewers by artifact content, not by producer

**Trigger.** A fixed set of reviewers is assigned per skill name or per task type.

**Do.** Select by what the diff or artifact actually contains. Reuse the condition already written
in each reviewer agent's own description instead of inventing one. Give a trivial change — a typo,
a renamed local, a version bump — no reviewer at all.

**Why.** A fixed fan-out costs more than it can find on a small change, and the routing conditions
are already written down where the reviewers are defined.

**Verify.** The routing table keys on content. A "no reviewer" row exists.

## P5. Replace round counters with a convergence condition

**Trigger.** "max 3 rounds", "up to N iterations".

**Do.** Continue while each round leaves strictly fewer open findings than the one before. On the
first round that does not reduce them, stop and escalate with what remains and what was tried.

**Why.** N is arbitrary. The real signal is whether the loop converges; one that stopped converging
will not converge on the next pass either, and one that is still converging should not be cut off
at an arbitrary number.

**Verify.** No numeric round cap. The escalation trigger is stated in words.

## P6. No model and no effort in a skill body

**Trigger.** A spawn names a model (`subagent (opus)`, `model: "sonnet"`), an effort level, or a
rule is justified by a named model's behaviour ("model N expands scope, so...").

**Do.** Remove all of it. A skill says what an agent does, not what runs it or how hard it thinks.
Put the reason for the change in the git commit.

**Why.** Both are configuration the owner sets deliberately in the harness and in each agent's
frontmatter; a skill that pins either overrides that and goes stale with it. And a description of
one model's behaviour is read by the next model as a statement about itself.

**Verify.** No model name and no effort level anywhere in the body. The agent's own frontmatter is
the exception — that is harness config, not text the model reads about itself.

## P7. English body; Russian only where the language is the content

**Trigger.** Russian prose in the body, headings, tables or pattern lists.

**Do.** Translate. Keep Russian in exactly four places: trigger phrases in `description` (matched
against what the owner types), strings the skill prints to the owner, Russian text used as data
(stop-word lists, legal templates), and generated deliverables the owner reads. Say once in the
file which parts stay Russian and why, so a later sweep does not "fix" them.

**Why.** Cyrillic costs roughly 1.5× the tokens for the same meaning, and the body is read by the
model while the deliverables are read by the owner — two audiences, no reason to mix them in one
file.

**Verify.** Remaining Cyrillic falls into one of the four cases.

## P8. Move accumulated lists out of the body

**Trigger.** SKILL.md carries a list that grows over time (learned patterns, catalogs) and a
`references/` file exists for exactly that.

**Do.** Move the list into references, leave one pointer line saying when to load it.

**Why.** The body is read on every invocation; a references file is read only when something needs
it.

**Verify.** Count the entries before and after — nothing lost. The body holds a pointer, not a list.

## P9. Every named skill, agent and command must exist

**Trigger.** The skill names another skill, an agent, or a slash command.

**Do.** Check it exists. Repoint or remove the dead ones.

**Why.** A dead reference fails silently at runtime: the call simply does nothing and the step is
skipped without a message.

**Verify.**

```bash
# names used in skills vs directories that exist
rg -o "Skill\((\w[\w-]*)" -r '$1' ~/.claude/skills/*/SKILL.md | sort -u
ls ~/.claude/skills/ ~/.claude/agents/
```

## P10. No machine-specific paths, no pinned versions

**Trigger.** An absolute path containing a user name, or a plugin path with a version in it.

**Do.** Resolve the path at runtime, or delegate to the skill that owns the resource.

**Why.** It breaks on another machine and after any upgrade — silently, because the command just
fails to find the file.

**Verify.** `rg "C:\\\\Users|/home/[a-z]+/" SKILL.md` returns nothing.

## P11. Documentation must match the repository

**Trigger.** project-knowledge or any catalog lists skills, pipelines or repositories.

**Do.** Check each named item exists. Remove what does not.

**Why.** These docs are read at the start of skill executions, so the drift propagates into every
plan built on them.

**Verify.** Every skill named in the docs has a directory; every repository named is one still
maintained.

## P12. Fix the writers before the executors

**Trigger.** A convention changes — language, rule format, checklist shape.

**Do.** Change what `quick-learning` writes and what `skill-trainer` embeds first, then sweep the
executing skills.

**Why.** Otherwise the next trainer run refills the old form into exactly the skills that were just
swept, and the work partly undoes itself.

**Verify.** `entry-format.md` and the trainer's agent prompt state the new convention before the
sweep starts.

## P13. Embed a lesson as a command when state can settle it

**Trigger.** A triad describes something a file, a field or a command's output can answer.

**Do.** Add it to the skill's `## Checks against state` as a command, not to the pattern list as
prose.

**Why.** This is the pattern that kept rebuilding the scaffolding: every lesson became prose, and
prose accumulated back into the tick-boxes that had just been removed.

**Verify.** The entry's `Carrier` field and where the rule landed agree.

## P14. Update the conventions doc in the same pass

**Trigger.** Any of the patterns above changes how skills are written.

**Do.** Write the new convention into `project-knowledge/references/patterns.md` in the same pass.

**Why.** The near-miss worth remembering: the conventions doc still said "the skill ends with a
`## Self-Verification` checklist" after every checklist had been removed. The next skill authored or
calibrated against it would have restored them, and the change would have decayed with nobody
noticing.

**Verify.** patterns.md describes what the skills now actually do.
