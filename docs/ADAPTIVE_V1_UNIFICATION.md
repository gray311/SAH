# Adaptive v1 × SAH unification

This branch keeps current SAH as the substrate and adds Adaptive v1 as an
optional outer-loop protocol. Nothing is pushed automatically. The default
`sah` protocol continues through the existing H1 YAML proposer, reward, and
every-round training path.

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
| proposer | one outer LLM policy, sampled sequentially K times |
| analyzer | deterministic trace/archive/context builder, not an LLM agent |
| builder | deterministic typed action compiler, not an LLM agent |
| validator/dedup | deterministic and fail-closed |
| reviewer | excluded and disabled in v1 |
| inner executor | a separate frozen inner Agent (`M0 + H2`) |

The older four-role wording describes a previous Codex pipeline, not the final
Adaptive v1 experiment. The port preserves the final runtime topology and the
verbatim Adaptive proposer system prompt.

## What is shared

Adaptive reuses these SAH components directly:

- the current `h2spec/1.0` full candidate genome;
- generated tools, skills, and middleware already inherited by SAH;
- `outer.materialize` and the NexAU candidate package layout;
- the frozen `inner.harness_runner` and evaluator budget;
- split proposer/executor serving and vLLM lifecycle cleanup;
- the Weave/slime LoRA trainer, merger, and replay encoding.

Adaptive adds no duplicate task registry, evaluator, inner runner, model
service, or candidate filesystem.

The adapter itself is split along the same boundary:

- `src/protocols/adaptive_v1.py`: small public facade;
- `src/protocols/adaptive_v1_proposal.py`: prompt, context, action, compiler;
- `src/protocols/adaptive_v1_controller.py`: reward, frontiers, plateau, commit.

## What remains protocol-specific

| concern | `sah` | `adaptive_v1` |
|---|---|---|
| proposal | existing H1 NexAU agent emits YAML | one plain-JSON policy, sequential K sampling |
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

Adaptive does not extend or relax `outer/harness_spec.py`. It reads SAH's full
base spec, changes only shared safe fields, calls the existing materializer,
then applies an Adaptive-only runtime overlay to that candidate package. Plain
SAH materialization therefore does not gain context compaction or other
Adaptive fields. A prompt-only Adaptive action also does not silently enable
compaction; the middleware appears only after a context-compaction edit (and
is then inherited by that Adaptive working state).

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
- committed proposer batches and the active adapter.

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
leaves the controller truthfully uncommitted.

## Local validation

No model service or GPU is needed for the protocol suite:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
bash -n scripts/unified_campaign.sh scripts/_outer_round_worker.sh \
  scripts/outer_round.sbatch scripts/train_mphi_step.sh
python -m compileall -q src tests
git diff --check
```

The tests exercise exact prompt provenance, sequential diversity, compilation
and SAH package preservation, overlay isolation, dual-frontier selection,
plateau-triggered signed batches, explicit commit/recovery, final-round skip,
Adaptive plain-text replay, and the unchanged default SAH collector.

Local result on 2026-07-28: all 11 offline tests passed, as did Python
compilation, shell syntax checks, and `git diff --check`. A separate local GPU
smoke also completed five protocol rounds using a real Qwen3.5-9B vLLM
executor and a real LoRA optimizer step; see
[`ADAPTIVE_V1_GPU_SMOKE.md`](ADAPTIVE_V1_GPU_SMOKE.md). The production
Slime/Slurm job was not run because its external Lustre, Weave, and scheduler
environment is not available in this workspace.
