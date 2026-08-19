# Hadamard max-det: proposer evolution process

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
| 1 | 1040 | 8 | 0.143274854 | 0.143274854 | 0.456712924 | 0.31343807 | `executor_gain_from_round_seed` |
| 2 | 1041 | 8 | 0.456712924 | 0.456712924 | 0.510438297 | 0.053725373 | `executor_gain_from_round_seed` |
| 3 | 1042 | 8 | 0.510438297 | 0.510438297 | 0.531723804 | 0.021285507 | `executor_gain_from_round_seed` |
| 4 | 1043 | 8 | 0.531723804 | 0.531723804 | 0.531723804 | 0 | `no_gain_over_round_seed` |
| 5 | 1044 | 8 | 0.531723804 | 0.531723804 | 0.545691796 | 0.0139679921 | `executor_gain_from_round_seed` |
| 6 | 1045 | 8 | 0.545691796 | 0.545691796 | 0.561608145 | 0.0159163488 | `executor_gain_from_round_seed` |
| 7 | 1046 | 8 | 0.561608145 | 0.561608145 | 0.561608145 | 0 | `no_gain_over_round_seed` |
