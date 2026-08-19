# Multi-task proposer evolution artifacts

The task directories follow the same `roundXX/candidateXX` organization as
the fully traced CP26 release. See each task README for the legacy evidence
boundary and lineage audit.

| Directory | Task | Source rounds | Candidate packages | Full executor trajectories |
|---|---|---:|---:|---:|
| [CP26](CP26/) | Circle packing (n=26; retained reference campaign) | 14 | 112 | 101 |
| [ERDOS_MIN_OVERLAP](ERDOS_MIN_OVERLAP/) | Erdős min-overlap | 36 | 336 | 0 |
| [AC2](AC2/) | Autocorrelation II | 24 | 224 | 0 |
| [AHC039](AHC039/) | AHC039 | 18 | 248 | 0 |
| [EPLB](EPLB/) | EPLB | 5 | 40 | 0 |
| [AC2_REPAIRED_FULL_TRACE](AC2_REPAIRED_FULL_TRACE/) | Autocorrelation II (post-fix audit round) | 1 | 8 | 8 |

The existing `CP26/` directory is a newer fully traced campaign and retains
complete executor trajectories. The exported legacy tasks do not manufacture
those missing conversations.

## Source availability

- Hadamard max-det is not included: the curve references source rounds
  1040--1046, but those original round directories are no longer present in
  either retained run root. Publishing an empty or reconstructed trace would
  be misleading.
- AHC039 contains all 18 source rounds that remain available. The curve also
  references source round 584, which is missing and is recorded as
  `source_round_missing` in `AHC039/evolution.json`.
- `AC2_REPAIRED_FULL_TRACE/` is a separate post-fix audit round. It provides a
  complete message-level example; it is not spliced into the historical AC2
  score curve.

## How to read the artifacts

For legacy campaigns, use `candidate_summary.json` and `round_summary.json` to
distinguish a within-round executor gain from a stronger inherited seed. A
materialized component only proves that it was offered to the executor. Runtime
use may be claimed only when an executor trajectory or a trusted component audit
records it. The repaired AC2 round has both; the historical exports do not.
