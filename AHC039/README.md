# AHC039: proposer evolution process

This directory mirrors the public `CP26/roundXX/candidateXX` layout.
It contains exact proposer trajectories, proposer submissions, materialized
harness packages, executor results, and best programs retained by the legacy
production series. Source-round gaps can mark distinct campaign segments or
proposer checkpoints; local round order follows the paper curve and must not be
assumed to be a single uninterrupted program lineage.

## Evidence boundary

Historical production results usually saved `trajectory: null` for the executor.
Accordingly, `executor_trajectory.json` is included only when the source really
contains it. Its absence must not be interpreted as proof that a mounted tool was
or was not called. `executor_result.json` remains the exact source artifact.

A reported round gain is also separated from an inherited stronger seed. The
`lineage_status` column prevents an imported program from being presented as a
within-round executor discovery.

## Round index

| Local | Source | Candidates | Base | Selected seed | Selected best | Executor gain | Lineage status |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 490 | 8 | 2.476554 | 0 | 1.64987259 | 1.64987259 | `executor_gain_from_round_seed` |
| 2 | 491 | 8 | 2.476554 | 0 | 2.47328889 | 2.47328889 | `executor_gain_from_round_seed` |
| 3 | 492 | 8 | 2.476554 | 0 | 1.27507111 | 1.27507111 | `executor_gain_from_round_seed` |
| 4 | 493 | 8 | 2.476554 | 0 | 0.903991111 | 0.903991111 | `executor_gain_from_round_seed` |
| 5 | 494 | 8 | 2.476554 | 0 | 2.47635111 | 2.47635111 | `executor_gain_from_round_seed` |
| 6 | 580 | 16 | 2.476554 | 2.48093481 | 2.48093481 | 0 | `inherited_seed_only_no_executor_gain` |
| 7 | 581 | 16 | 2.48093481 | 2.48240889 | 2.48240889 | 0 | `inherited_seed_only_no_executor_gain` |
| 8 | 582 | 16 | 2.48240889 | 2.48436 | 2.48436 | 0 | `inherited_seed_only_no_executor_gain` |
| 9 | 583 | 16 | 2.48436 | 2.48011852 | 2.48011852 | 0 | `no_gain_over_round_seed` |
| 10 | 584 | — | — | — | — | — | source_round_missing |
| 11 | 720 | 16 | 2.48436 | 2.47960148 | 2.47960148 | 0 | `no_gain_over_round_seed` |
| 12 | 721 | 16 | 2.48436 | 2.47726963 | 2.47726963 | 0 | `no_gain_over_round_seed` |
| 13 | 722 | 16 | 2.48436 | 2.48211259 | 2.48211259 | 0 | `no_gain_over_round_seed` |
| 14 | 723 | 16 | 2.48436 | 2.48232148 | 2.48232148 | 0 | `no_gain_over_round_seed` |
| 15 | 724 | 16 | 2.48436 | 2.48286074 | 2.48286074 | 0 | `no_gain_over_round_seed` |
| 16 | 725 | 16 | 2.48436 | 2.48162074 | 2.48162074 | 0 | `no_gain_over_round_seed` |
| 17 | 726 | 16 | 2.48436 | 2.48079704 | 2.48079704 | 0 | `no_gain_over_round_seed` |
| 18 | 727 | 16 | 2.48436 | 2.47882519 | 2.47882519 | 0 | `no_gain_over_round_seed` |
| 19 | 728 | 16 | 2.48436 | 2.48168296 | 2.48168296 | 0 | `no_gain_over_round_seed` |
