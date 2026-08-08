# Recurring-defect detector

Runs in two places, and they cover different gaps:

- **step 4 of quick-learning**, only when the signal gate already proceeded — a clean session costs
  nothing;
- **at session start**, as a `SessionStart` hook, which is what stops the sign being missed while the
  owner is mid-bugfix and no session boundary follows. The script is machine configuration, not skill
  content, so it lives in the harness at `~/.claude/hooks/recurring-defect.sh` rather than in this
  repository. This file is the method; that file is one deployment of it.

A file repaired far more often than the repository repairs anything is where a contradiction sits:
someone is turning a dial both ways. This names the file and stops. It **never** invokes anything —
`triz-synergy` is on-demand only, and a detector that launched it would fire the expensive procedure
on a noisy repository.

## The measurement

```bash
BASE=$(git log --oneline | wc -l)
ALLFIX=$(git log --grep="^fix" -i --oneline | wc -l)

# files repaired in this session, measured against the whole history
git log --grep="^fix" -i --name-only --pretty=format:"" -20 \
  | grep -Ev '(^|/)tests?/|(^|/)test_|_test\.|\.test\.|\.spec\.' \
  | sort -u | while read -r f; do
  [ -n "$f" ] || continue
  fx=$(git log --grep="^fix" -i --oneline -- "$f" | wc -l)
  tot=$(git log --oneline -- "$f" | wc -l)
  awk -v f="$f" -v fx=$fx -v tot=$tot -v af=$ALLFIX -v b=$BASE 'BEGIN{
    if (fx >= 8 && tot > 0 && (fx/tot) >= 2*(af/b))
      printf "%s %d/%d = %.0f%%\n", f, fx, tot, fx*100/tot }'
done
```

Report at most the two highest ratios — a list of five is a wall, not a signal. Output
non-empty → append one line, and nothing more:

`Файл чинят непропорционально часто: {file} ({fx}/{tot} = {pct}%, база репо {base}%). Похоже на противоречие — /triz-synergy разберёт.`

## Why these two guards, and not a round number

**Against the repository's own baseline, not an absolute threshold.** Baselines measured across four
repositories ranged from 5% to 27%. A fixed number would fire constantly in one and never in
another.

**At least 8 fix commits.** Below that the ratio is arithmetic on three commits. One repository
showed 67% built from two fixes out of three — noise wearing a signal's clothes.

## What the measurement showed

| Repository | Baseline | Top file | Ratio | Detector |
|---|---|---|---|---|
| Своя ИИ платформа | 27% | `app/services/answer_guard.py` | 72% (26/36) | fires |
| Фриланс дашборд | 15% | `.github/workflows/deploy.yml` | 69% (11/16) | fires |
| Пасека | 21% | `scripts/click-check.mjs` | 67%, from 2 fixes of 3 | silent |
| b24u-playbook | 5% | `today-status.ps1` | 29%, 6 fixes | silent |

It discriminates rather than confirms: under "this is only activity", `config.py` and `cli.py` at 50
commits each would rank alongside `criteria_navigator.py` at 55. They sit at 26% and 32%, on the
baseline, while the navigator sits at 71%.

The two files it ranks highest — `answer_guard.py` and `criteria_navigator.py` — are the ones behind
the worked cases "the guard and the price" and "the enumeration threshold". The signal named, from
history alone, two places where a contradiction was later found by hand.

## Known limits

- It locates a contradiction in a repository **with history**; it says nothing in one too young to
  have a baseline.
- It is blind between sessions — it speaks only when quick-learning already ran. A sign met while
  the owner is mid-bugfix and no session boundary follows is still missed.
- A test file tracks its subject and fires alongside it. Left in, it took one of the two reported
  slots and named the place its subject had already named, so test paths are now excluded. The cost
  is that a contradiction living genuinely in test code goes unreported — no case has shown one.
