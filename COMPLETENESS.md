# Artifact completeness audit

This release contains two different evidence classes. They must not be treated
as interchangeable.

## Full message-level traces

| Directory | Rounds | Candidates | Proposer trajectories | Materialized harnesses | Executor trajectories |
|---|---:|---:|---:|---:|---:|
| `CP26/` | 14 | 112 | 112 | 102 | 101 |
| `AC2_REPAIRED_FULL_TRACE/` | 1 | 8 | 8 | 8 | 8 |

`CP26/` is the only retained multi-round campaign with executor conversations.
The repaired AC2 bundle is one fully traced audit round, not a multi-round
evolution chain.

## Legacy retained artifacts (partial)

| Directory | Completed rounds | Candidates | Proposer trajectories | Materialized harnesses | Executor results | Executor trajectories |
|---|---:|---:|---:|---:|---:|---:|
| `ERDOS_MIN_OVERLAP/` | 36 | 336 | 336 | 313 | 312 | 0 |
| `AC2/` | 24 | 224 | 224 | 206 | 199 | 0 |
| `AHC039/` | 18 | 248 | 248 | 235 | 235 | 0 |
| `EPLB/` | 5 | 40 | 40 | 34 | 34 | 0 |
| `HADAMARD_MAX_DET/` | 7 | 56 | 56 | 48 | 48 | 0 |

The gaps between candidate count and harness count are proposer submissions
that failed validation, so no executor rollout was launched. Additional gaps
between harnesses and executor results are interrupted or failed launches.

For every completed legacy rollout, `provenance.json` records that the runner
was called with `--no-trajectory`. Consequently, these directories can support
claims about:

- what the proposer read and submitted;
- which H2 package was materialized;
- seed score, best score, evaluation ledger, and final program;
- whether a score jump came from the executor or from an inherited seed.

They cannot support claims about:

- the executor's exact messages or intermediate reasoning;
- whether a mounted custom tool was actually called;
- whether a middleware message fired, unless a separate trusted runtime audit
  explicitly records that event.

Recovering those claims requires replaying the chosen historical harnesses with
trajectory retention enabled. Missing conversations must not be synthesized.

## Initial executor trace anchors

Each legacy task directory also contains `initial_executor_trace/`, recovered
from a trajectory-enabled run that predates its proposer-evolution campaign:

| Task directory | Complete executor messages |
|---|---:|
| `ERDOS_MIN_OVERLAP/` | 130 |
| `AC2/` | 133 |
| `AHC039/` | 124 |
| `EPLB/` | 130 |
| `HADAMARD_MAX_DET/` | 124 |

These anchors show exact initial executor behavior and tool exchanges. They are
not counted as evolved-candidate trajectories in the table above, and they must
not be attached retrospectively to a later harness.
