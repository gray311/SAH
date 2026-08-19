# Erdős min-overlap: proposer evolution process

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
| 1 | 350 | 8 | 0.83427712 | 0.769448826 | 0.999366296 | 0.22991747 | `executor_gain_from_round_seed` |
| 2 | 351 | 8 | 0.999366296 | 0.999641496 | 0.999641496 | 0 | `inherited_seed_only_no_executor_gain` |
| 3 | 352 | 8 | 0.999641496 | 0.999641496 | 0.999641496 | 0 | `no_gain_over_round_seed` |
| 4 | 353 | 8 | 0.999641496 | 0.999641496 | 0.999641496 | 0 | `no_gain_over_round_seed` |
| 5 | 520 | 16 | 0.83427712 | 0.999641496 | 0.999641496 | 0 | `inherited_seed_only_no_executor_gain` |
| 6 | 521 | 16 | 0.999641496 | 0.999641496 | 0.999641496 | 0 | `no_gain_over_round_seed` |
| 7 | 522 | 16 | 0.999641496 | — | — | — | `no_executor_result` |
| 8 | 523 | 16 | 0.999641496 | 0.999641496 | 0.999641496 | 0 | `no_gain_over_round_seed` |
| 9 | 660 | 16 | 0.999641496 | 0.999641496 | 0.99985521 | 0.000213714453 | `executor_gain_from_round_seed` |
| 10 | 661 | 16 | 0.99985521 | 0.99985521 | 0.99985521 | 0 | `no_gain_over_round_seed` |
| 11 | 800 | 8 | 0.99985521 | — | — | — | `no_executor_result` |
| 12 | 801 | 8 | 0.99985521 | 0.99985521 | 0.99988767 | 3.24600584e-05 | `executor_gain_from_round_seed` |
| 13 | 802 | 8 | 0.99988767 | 0.99988767 | 0.99988767 | 0 | `no_gain_over_round_seed` |
| 14 | 803 | 8 | 0.99988767 | 0.99988767 | 0.99988767 | 0 | `no_gain_over_round_seed` |
| 15 | 804 | 8 | 0.99988767 | 0.99988767 | 0.99988767 | 0 | `no_gain_over_round_seed` |
| 16 | 805 | 8 | 0.99988767 | 0.99988767 | 0.999903784 | 1.61134864e-05 | `executor_gain_from_round_seed` |
| 17 | 806 | 8 | 0.999903784 | 0.999903784 | 0.999903784 | 0 | `no_gain_over_round_seed` |
| 18 | 807 | 8 | 0.999903784 | 0.999944539 | 0.999968086 | 2.35473165e-05 | `inherited_stronger_seed_plus_executor_gain` |
| 19 | 808 | 8 | 0.999968086 | 0.999968086 | 0.999968086 | 0 | `no_gain_over_round_seed` |
| 20 | 809 | 8 | 0.999968086 | 0.999968086 | 1.00000869 | 4.06041239e-05 | `executor_gain_from_round_seed` |
| 21 | 810 | 8 | 1.00000869 | 1.00000869 | 1.00000869 | 0 | `no_gain_over_round_seed` |
| 22 | 811 | 8 | 1.00000869 | — | — | — | `no_executor_result` |
| 23 | 1000 | 8 | 0.999903784 | 0.999903784 | 0.999944539 | 4.07553588e-05 | `executor_gain_from_round_seed` |
| 24 | 1001 | 8 | 0.999944539 | — | — | — | `no_executor_result` |
| 25 | 1400 | 8 | 0.999944539 | 0.999944539 | 0.999944539 | 0 | `no_gain_over_round_seed` |
| 26 | 1401 | 8 | 0.999944539 | 0.999944539 | 0.999944539 | 0 | `no_gain_over_round_seed` |
| 27 | 1402 | 8 | 0.999944539 | 0.999944539 | 0.999944539 | 0 | `no_gain_over_round_seed` |
| 28 | 1403 | 8 | 0.999944539 | 0.999968086 | 0.999968086 | 0 | `inherited_seed_only_no_executor_gain` |
| 29 | 1404 | 8 | 0.999968086 | — | — | — | `no_executor_result` |
| 30 | 1405 | 8 | 0.999968086 | 1.00000869 | 1.00000869 | 0 | `inherited_seed_only_no_executor_gain` |
| 31 | 1406 | 8 | 1.00000869 | 0 | 1.00000869 | 1.00000869 | `executor_gain_from_round_seed` |
| 32 | 1407 | 8 | 1.00000869 | 1.00000869 | 1.00000869 | 0 | `no_gain_over_round_seed` |
| 33 | 1408 | 8 | 1.00000869 | 0 | 1.00000869 | 1.00000869 | `executor_gain_from_round_seed` |
| 34 | 1409 | 8 | 1.00000869 | 1.00000869 | 1.00000869 | 0 | `no_gain_over_round_seed` |
| 35 | 1410 | 8 | 1.00000869 | 1.00000869 | 1.00000869 | 0 | `no_gain_over_round_seed` |
| 36 | 1411 | 8 | 1.00000869 | 1.00000869 | 1.00000869 | 0 | `no_gain_over_round_seed` |
