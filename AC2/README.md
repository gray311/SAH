# Autocorrelation II: proposer evolution process

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
| 1 | 390 | 8 | 0.999788894 | 0.955049505 | 1.00383877 | 0.0487892694 | `executor_gain_from_round_seed` |
| 2 | 391 | 8 | 1.00383877 | 1.02579444 | 1.02579444 | 0 | `inherited_seed_only_no_executor_gain` |
| 3 | 392 | 8 | 1.02579444 | 1.02579444 | 1.02579444 | 0 | `no_gain_over_round_seed` |
| 4 | 393 | 8 | 1.02579444 | 1.02579444 | 1.0266518 | 0.000857360281 | `executor_gain_from_round_seed` |
| 5 | 394 | 8 | 1.0266518 | 1.0266518 | 1.02872075 | 0.00206895136 | `executor_gain_from_round_seed` |
| 6 | 395 | 8 | 1.02872075 | 1.02872075 | 1.0333589 | 0.00463815157 | `executor_gain_from_round_seed` |
| 7 | 396 | 8 | 1.0333589 | 1.0333589 | 1.03430515 | 0.000946248606 | `executor_gain_from_round_seed` |
| 8 | 397 | 8 | 1.03430515 | 1.03430515 | 1.03430515 | 0 | `no_gain_over_round_seed` |
| 9 | 560 | 16 | 0.999788894 | 1.03430515 | 1.03492408 | 0.000618926387 | `inherited_stronger_seed_plus_executor_gain` |
| 10 | 561 | 16 | 1.03492408 | 1.03492408 | 1.03663078 | 0.00170670595 | `executor_gain_from_round_seed` |
| 11 | 700 | 16 | 1.03663078 | 1.03663078 | 1.03841162 | 0.00178083364 | `executor_gain_from_round_seed` |
| 12 | 701 | 16 | 1.03841162 | 1.03841162 | 1.03895652 | 0.000544901801 | `executor_gain_from_round_seed` |
| 13 | 840 | 8 | 1.03895652 | 1.03841162 | 1.03841162 | 0 | `no_gain_over_round_seed` |
| 14 | 841 | 8 | 1.03895652 | 1.03895652 | 1.03895652 | 0 | `no_gain_over_round_seed` |
| 15 | 842 | 8 | 1.03895652 | 1.03895652 | 1.03895652 | 0 | `no_gain_over_round_seed` |
| 16 | 843 | 8 | 1.03895652 | 1.03895652 | 1.04198934 | 0.00303282512 | `executor_gain_from_round_seed` |
| 17 | 844 | 8 | 1.04198934 | 1.04198934 | 1.04200121 | 1.18668038e-05 | `executor_gain_from_round_seed` |
| 18 | 845 | 8 | 1.04200121 | — | — | — | `no_executor_result` |
| 19 | 846 | 8 | 1.04200121 | 1.04200121 | 1.04200121 | 0 | `no_gain_over_round_seed` |
| 20 | 847 | 8 | 1.04200121 | 1.04200121 | 1.04200226 | 1.05253529e-06 | `executor_gain_from_round_seed` |
| 21 | 848 | 8 | 1.04200226 | 1.04200226 | 1.04200226 | 0 | `no_gain_over_round_seed` |
| 22 | 849 | 8 | 1.04200226 | 1.04200226 | 1.04200226 | 0 | `no_gain_over_round_seed` |
| 23 | 850 | 8 | 1.04200226 | 1.04200226 | 1.04200226 | 0 | `no_gain_over_round_seed` |
| 24 | 851 | 8 | 1.04200226 | 1.04200226 | 1.04200226 | 0 | `no_gain_over_round_seed` |
