# Autocorrelation II: repaired fully traced round

This is a post-fix AC2 round exported in the same `roundXX/candidateXX` organization as CP26. It is separate from the historical multi-round curve in `../AC2/`: every candidate here retains the complete proposer and executor message trajectories.

Each candidate contains exact proposer/executor inputs, trajectories, the proposer submission, the generated harness JSON, a materialized `harness/` package, the exact executor result, and its output program. Runtime component audits in `executor_result.json` are the source of truth for enactment; component names alone are not evidence of use.

- Candidates: 8
- Selected candidate: candidate04
- Selected best score: 0.995758332188
- Full proposer trajectories: 8/8
- Full executor trajectories: 8/8
