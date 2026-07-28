# Adaptive v1 × SAH unification

This branch keeps current SAH as the substrate and adds Adaptive v1 as an
optional outer-loop protocol. The default `sah` protocol continues through the
existing H1 YAML proposer, reward, and every-round training path.

Port provenance:

- SAH substrate: `f9868c3ea06e1323d67e3817065035287662108e`;
- Adaptive v1 source implementation
  (`harnessopt.py`, `strategies.py`, `evogate_policy_optimizer.py`):
  `dcbc45a2fed3cd7d6700c87a583d85952cfc695c`;
- frozen proposer prompt SHA-256:
  `02ef7c5aff2eba3d5e522ee96c48e9e7e1b1b855d5c0091455c7d2855f5f4013`.

## Agent topology (important)

The final Adaptive v1 runtime does **not** have an LLM
`Analyzer → Proposer → Builder → Reviewer` team.

| role | Adaptive v1 implementation |
|---|---|
| proposer | one fixed NexAU H1 Agent, sampled sequentially K times |
| analyzer | deterministic trace/archive/context builder, not an LLM agent |
| builder | deterministic typed action compiler, not an LLM agent |
| validator/dedup | deterministic and fail-closed |
| reviewer | excluded and disabled in v1 |
| inner executor | a separate frozen NexAU Agent (`M0 + H2`) |

The older four-role wording describes a previous Codex pipeline, not the final
Adaptive v1 experiment. The port preserves the final runtime topology and the
verbatim Adaptive proposer system prompt.

## What is shared

Adaptive reuses these SAH components directly:

- the current `h2spec/1.0` full candidate genome;
- generated tools, skills, and middleware already inherited by SAH;
- `outer.materialize` and the NexAU candidate package layout;
- NexAU `AgentConfig.from_yaml` and `Agent` for both outer and inner execution;
- the frozen `inner.harness_runner` and evaluator budget;
- split proposer/executor serving and vLLM lifecycle cleanup;
- the Weave/slime LoRA trainer, merger, and replay encoding.

Adaptive adds no duplicate task registry, evaluator, inner runner, model
service, or candidate filesystem.

Adaptive's fixed H1 is also a normal declarative NexAU package:

```text
src/protocols/adaptive_v1_harness/
├── agent.yaml
└── system.md
```

`system.md` is byte-for-byte the final Adaptive v1 proposal prompt. A fresh
NexAU Agent is constructed for each sequential sample, and its actual message
history is recorded as the outer trajectory. As in SAH, `agent.yaml` is the
single source of truth for H1 sampling; runtime code overrides only the served
endpoint/model, timeout, and per-sample seed. Every round records an
`h1_version` and whole-package hash.

The adapter itself is split along the same boundary:

- `src/protocols/adaptive_v1.py`: small public facade;
- `src/protocols/adaptive_v1_proposal.py`: prompt, context, action, compiler;
- `src/protocols/adaptive_v1_controller.py`: reward, frontiers, plateau, commit.

## What remains protocol-specific

| concern | `sah` | `adaptive_v1` |
|---|---|---|
| proposal | existing H1 NexAU Agent emits YAML | dedicated H1 NexAU Agent emits one sparse JSON action, sequential K sampling |
| per-batch diversity | independent threaded H1 runs | later samples see all prior valid actions |
| action | full/partial H2 YAML | sparse semantic edit atoms compiled into H2 |
| context | SAH task prompt + feedback | bounded archive/evidence/context with exact v1 fallback |
| reward | existing SAH v2 group reward | anchored sign-preserving relative credit |
| frontier | next best H2 | separate exploratory working and protected champion |
| proposer update | every accepted step/campaign rule | 3-round confirmed-record plateau + signed contrast |
| final round | campaign-owned | update explicitly skipped because it cannot be used |
| reviewer | SAH generated-code review remains | disabled, matching Adaptive v1 |

Promotion feedback is used only for the champion frontier. It is never copied
into Adaptive proposer context, archive rewards, or training rows.

## Isolation guarantee

`--protocol` defaults to `sah`. The original functions remain the default
branch in `outer.outer_round`; the Adaptive module is imported only after
selecting `adaptive_v1`.

Adaptive does not extend or relax `outer/harness_spec.py`. Its deterministic
compiler accepts only fields already represented by native `h2spec/1.0`:
`system_prompt`, `agent.max_iterations`, `sampling.temperature`, and
`sampling.max_tokens`. The public pointers use those same native paths
(`/agent/max_iterations`, `/sampling/temperature`, and
`/sampling/max_tokens`); legacy Adaptive aliases remain accepted. Unsupported
context/profile operations fail closed.

Every accepted action is compiled into a complete native SAH spec, validated
by the unmodified SAH schema, and passed directly to the existing
`outer.materialize`. The resulting candidate has exactly the SAH NexAU package
shape (`agent.yaml`, `prompt.md`, `spec.yaml`, `tools/`, `skills/`,
`middlewares/`). `spec.yaml` contains the full native H2 spec and uses SAH's
own `spec_hash`; there is no Adaptive runtime overlay or post-materialization
patch.

The proposer context includes the complete current native H2 spec, not an
Adaptive-only flattened surrogate. The mutable contract remains sparse, so
seeing inherited tools/skills/middleware does not authorize modifying them.

The shared additions are backward-compatible:

- an optional inner request seed (unset for SAH);
- recursive score discovery, compatible with the original one-level layout;
- an explicit replay batch input (the existing `--rounds` input remains);
- vLLM shutdown/GPU cleanup logging.

## Modes

```bash
# Existing SAH campaign; delegates to fresh_campaign.sh.
bash scripts/unified_campaign.sh sah <task> <steps> <round_base> [force_tool_frac] [workspace]

# Adaptive v1; defaults to K=4 and 3 matched outcome/promotion repeats.
bash scripts/unified_campaign.sh adaptive_v1 <task> <rounds> <round_base> [workspace]
```

`round_base` is only the collision-free SAH artifact directory number. Adaptive
context, proposal IDs, generation seeds, plateau timing, and final-round logic
use a separate zero-based protocol round, so a campaign stored in
`round300..round309` still behaves exactly like Adaptive rounds `0..9`.

Useful Adaptive environment knobs:

```text
K=4
MAX_EVALS=20
ROLLOUT_REPEATS=3
PROMOTION_REPEATS=3
ROLLOUT_SEED=104729
PLATEAU_ROUNDS=3
CONFIDENCE_Z=0
PROPOSER_SEED=23
```

`CONFIDENCE_Z=0` matches fixed-instance Adaptive v1 tasks where no independent
uncertainty protocol was available. Use a positive value only when repeated
matched scores support it.

## State and recovery

The Adaptive state is a task-keyed atomic JSON file containing:

- working and champion packages;
- public outcome attempts and operator statistics;
- pending/replay policy examples;
- confirmed-record plateau counters;
- committed proposer batches and the active adapter;
- an explicit pending-training record when a signed batch has not yet been
  committed.

Campaign startup reads this state through:

```bash
PYTHONPATH=src python -m protocols.adaptive_v1 campaign-status \
  --state <adaptive_v1_state.json> --task <task_id>
```

It restores the next protocol round, working H2, active adapter, and previous
LoRA checkpoint. Existing pending train/merge job IDs are resumed rather than
submitted twice, and partial/untracked artifact rounds fail closed instead of
being overwritten.

Collection writes `adaptive_train_batch.jsonl` and a digest-bound manifest
only when training is required. It does **not** claim training succeeded.
After the external SAH trainer and merge finish, the campaign calls:

```bash
PYTHONPATH=src python -m protocols.adaptive_v1 commit-update \
  --state <adaptive_v1_state.json> \
  --manifest <round>/adaptive_train_manifest.json \
  --adapter <merged_mphi> \
  --checkpoint <lora_checkpoint>
```

Only this commit clears pending examples, moves them to replay, resets the
plateau window, and increments `policy_updates`. A failed/interrupted trainer
leaves the controller truthfully uncommitted and blocks collection of a later
round.

Matched rollout evidence also fails closed: a missing base outcome aborts
collection; a missing champion reference or candidate promotion can never be
replaced with outcome evidence and therefore cannot advance the champion.
`adaptive_rollout_plan.json` records every channel, package, repeat, and
request seed.

## Local validation

No model service or GPU is needed for the protocol suite:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
bash -n scripts/unified_campaign.sh scripts/_outer_round_worker.sh \
  scripts/outer_round.sbatch scripts/train_mphi_step.sh
python -m compileall -q src tests
git diff --check
```

The tests exercise exact prompt provenance, the declarative Adaptive NexAU H1
package, actual NexAU trace preservation, sequential diversity, native SAH
schema compilation/package parity, dual-frontier selection,
plateau-triggered signed batches, missing-reference fail-closed behavior,
explicit adapter/working-frontier recovery, pending-batch blocking,
final-round skip, Adaptive plain-text replay, and the unchanged default SAH
collector.

Local result on 2026-07-28: all 18 Adaptive protocol tests passed, as did Python
compilation, shell syntax checks, and `git diff --check`. Final-format GPU
revalidation completed two consecutive rounds with real Qwen3.5-9B inference:
8/8 outer traces came from NexAU H1 Agents with exactly one assistant call,
6 candidates were valid native SAH H2 packages, and all 16 NexAU inner traces
were non-empty with no inner errors. The second round inherited the first
round's archive/context. An earlier five-round loop additionally completed a
real LoRA optimizer step; see
[`ADAPTIVE_V1_GPU_SMOKE.md`](ADAPTIVE_V1_GPU_SMOKE.md). The production
Slime/Slurm job was not run because its external Lustre, Weave, and scheduler
environment is not available in this workspace.
