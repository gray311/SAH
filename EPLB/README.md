# EPLB: proposer evolution process

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
| 1 | 430 | 8 | 0.126539279 | 0.12642027 | 0.12642027 | 0 | `no_gain_over_round_seed` |
| 2 | 431 | 8 | 0.126539279 | 0.126569006 | 0.126744726 | 0.000175720177 | `inherited_stronger_seed_plus_executor_gain` |
| 3 | 432 | 8 | 0.126744726 | 0.126728165 | 0.127074372 | 0.000346206498 | `executor_gain_from_round_seed` |
| 4 | 433 | 8 | 0.127074372 | 0.127163363 | 0.127163363 | 0 | `inherited_seed_only_no_executor_gain` |
| 5 | 434 | 8 | 0.127163363 | 0.127136659 | 0.127136659 | 0 | `no_gain_over_round_seed` |
