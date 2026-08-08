---
name: artifact-report
description: Turn a raw SAH artifact directory (inspection bundle, campaign round, audit or replay output, case-study dir) into a single self-contained HTML report where every claim links to the artifact it was read from. Use whenever asked to render, write up, summarize, or present results as an HTML report or page; to make a bundle browsable or shareable; to build an evidence-linked or evidence-credited report; or to visualize what a round, replay, or audit actually showed.
---

# Reporting a raw artifact directory

A campaign leaves behind a directory of JSON, logs, and status markers that is
complete but unreadable. This skill turns one such directory into a single HTML
file a colleague can open and trust — because every number in it is a link back
to the artifact it came from.

This is a **read-and-credit job, not a summarization job**. The bundle is the
authority. You are building a navigable index over it with a narrative attached,
not a replacement for it.

## The one rule

> **Every claim carries a link to the artifact it was read from, and no number
> appears that you did not personally read out of a file.**

Not "derived from", not "consistent with" — read out of. If you computed a
percentage, show the two inputs and their sources. If the bundle does not record
something, the report says the bundle does not record it. A confident,
unsourced number in a clean-looking report is worse than no report: it launders
a guess into a citation.

Its corollary, which is where these reports actually earn their keep:

> **Reproduce the bundle's own limitations; never smooth them over.**

An inspection bundle that says "a single pair estimates the total prompt effect,
not which sentence mediated it" has done the hard intellectual work already.
Dropping that sentence to make the headline land harder is the failure mode this
skill exists to prevent.

## Workflow

### 1. Inventory before reading

`find` the directory two levels deep and read its `README.md` and `manifest.json`
first — inspection bundles carry a schema string (e.g. `ac2-round-inspection/1.0`)
and a file-order convention that tells you what everything is. Note the
`run_dir` it shadows; the bundle is a copy, and the report should say so.

Then read **everything small**: every `*.json` audit, every status marker file
(`PASSED`, `FAILED`, `PASSED_REAUDIT`, `STARTED`), every `README.md`. Logs and
full trajectories are large — go into those only for a specific claim.

### 2. Find the finding

Most bundles have a scoreboard and, underneath it, a result that matters more.
The scoreboard is the easy part; the finding is why someone built the bundle.
Ask what the directory contains beyond the scores:

| what you see | what it usually means |
|---|---|
| a `causal_attribution/` or `*_control/` dir | someone doubted the headline number and tested it |
| a `paired_*`, `patched_*`, `contract_*` replay | a bug was found and the fix was verified end-to-end |
| a `FAILED` next to a `PASSED_REAUDIT` | an assertion was wrong, not the run — read both |
| a README section on policy or "after the fix" | the round's real output is a rule change, not a score |

Lead the report with the finding, not the leaderboard. A report whose headline
is "cand03 scored 0.9958" buries the fact that the round proved score-based
ranking was measuring the wrong thing.

### 3. Build the claim→evidence ledger

Before writing HTML, list every claim you intend to make and, next to it, the
exact file and field. Claims that survive this get written; claims that do not
get dropped. Cite the field, not just the file — `paired_effect.json → causal_delta`
beats `paired_effect.json`.

Quote the bundle verbatim for anything contested or self-critical. Its own
wording is evidence; your paraphrase is not.

### 4. Write the report into the bundle

Put `REPORT.html` **inside the directory it describes**. All evidence links are
then relative and the report travels with the bundle when it is copied, tarred,
or moved between filesystems. An absolute `/lustre/...` link is dead the moment
anyone opens the report anywhere else.

Inline `assets/report.css` and `assets/report.js` from this skill directly into
the file. One file, no CDN, no `fetch()`, no build step — these get opened from
`file://` on machines with no network. `report.js` gives you `tip()`, `dotPlot()`,
`divergingBars()`, `decomposition()`, and `initTheme()`; the CSS gives you
`.ev` evidence chips, `.claim` blocks, `.tile` stat tiles, `.pill` status pills,
and a validated light/dark palette.

Structure that has worked: header with provenance → a lead paragraph stating the
whole argument in three moves → stat tiles → one section per move → the policy
or consequence section → a guide to reading the raw bundle.

### 5. Charts

**Invoke the `dataviz` skill before writing any chart code.** Its palette is
already the one in `assets/report.css`, and the three helpers in `report.js`
encode decisions it will make you justify:

- **Scores near 1.0 → dot plot, never bars.** Bars need a zero baseline; every
  score sits above 0.95, so bars would be either flat or dishonestly truncated.
  A dot plot may use a non-zero axis because position, not length, is the encoding.
- **Signed quantities → diverging bars around a true zero.** Advantages, deltas,
  effects. The two hues must be the diverging pair, and the sign should double as
  the semantic label ("↑ reinforce" / "↓ suppress").
- **"How much of this is really attributable to X" → decomposition bar** stacked
  from zero, so segment widths compare directly.

Then render it and look at it: `google-chrome --headless --disable-gpu
--no-sandbox --hide-scrollbars --window-size=1180,6000 --virtual-time-budget=4000
--screenshot=/tmp/r.png "file://<abs path>"`, slice the PNG with PIL, and read the
slices. Label overflow past the right margin and bars colliding with their own
labels are invisible in source and obvious on screen. Headless Chrome ignores
`--force-dark-mode` for `prefers-color-scheme`; to check dark, write a temp copy
with `data-theme="dark"` stamped on `<html>` and delete it after.

### 6. Verify before shipping

Every one of these has caught a real defect in this project's reports:

- **Every link resolves.** `ls` each relative href. The AC2 bundle's README names
  `config/examples/ac2_paired.yaml` as its runnable template and that file does
  not exist on any branch — shipped as a link, it is a dead end that looks
  authoritative. Render an absent path as a dashed `.ev.missing` span saying so.
- **Every number traces.** Walk the ledger from step 3 and re-grep one value per
  claim out of its cited file.
- **Status markers are read in full, not by filename.** A `FAILED` file next to a
  `PASSED_REAUDIT` means the assertion was over-strict; reporting the `FAILED`
  alone inverts the conclusion.
- **Stated caveats survived.** Grep the bundle's own READMEs for "single",
  "cannot", "not", "diagnostic", "required" — those sentences are the ones most
  likely to have been dropped, and they are the ones that matter.
- **Percentages show their inputs.** "9.25%" is unfalsifiable; "0.002376 /
  0.025693" is checkable.
- **No zero-for-missing.** A field the bundle never recorded renders as "—", never
  as `0`. (Same rule as `exp-index`, same reason.)

### 7. Report to the user

Say where the file is, how claims are credited, and — explicitly — anything you
flagged rather than smoothed: dead links, over-strict failure markers, single-sample
caveats, fields the bundle never recorded. Leave the file untracked unless asked
to commit.

## Worked example

`references/ac2-round001.md` walks the AC2 round-1 report end to end: the source
bundle, the finding it leads with, every claim→evidence mapping, the three charts
and why each form was chosen, and the two things it flagged instead of smoothing.
Read it before starting a similar report; the shape transfers.
