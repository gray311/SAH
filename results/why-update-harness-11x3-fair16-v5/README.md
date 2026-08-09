# CP rounds 3–4 artifacts

This directory contains the complete saved artifacts for logical rounds 3 and
4 of `eft__math__circle_packing` (CP) from campaign
`why-update-harness-11x3-fair16-v5`.

Included method lanes:

- `update_harness`: 8 proposer trajectories + 8 solution trajectories per round
- `update_context`: 8 proposer trajectories + 8 solution trajectories per round
- `update_executor`: 16 solution trajectories per round

The directory hierarchy mirrors the campaign run tree. Logical round numbers
are zero-based and are stored as `round003` and `round004`. Each copied round
contains its original `ROUND_COMPLETE` marker along with prompts, trajectories,
generated harnesses or executor outputs, rewards, rollout results, runtime
telemetry, and audit metadata.

Open `INDEX.html` for the cross-method comparison. Every copied round also has
its own self-contained `REPORT.html`; numeric claims link to the exact relative
artifact and field used as evidence. `render_reports.py` regenerates the seven
HTML files and fails if any evidence link is dead.
