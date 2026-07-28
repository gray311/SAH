# Adaptive v1 local GPU loop validation

- Date: 2026-07-28
- Result: PASS
- SAH substrate: `f9868c3ea06e1323d67e3817065035287662108e`

This validation used ignored local fixtures and did not add model weights,
datasets, adapters, or runtime traces to the repository. It contains two
complementary checks:

1. an earlier five-round controller/training loop with real Qwen3.5-9B
   inference, NexAU inner execution, and one real LoRA
   backward/update/save; and
2. a final two-round format revalidation after moving the Adaptive outer
   proposer into a declarative NexAU H1 package and removing the
   Adaptive-only H2 overlay.

The five-round run validates the controller, replay, update, adapter serving,
and long-loop behavior. Its outer proposals used the earlier direct
OpenAI-compatible endpoint adapter, so it is not used as evidence for the
final NexAU H1 format. The final two-round run is the format/runtime evidence
for the code on this branch.

## Final NexAU-format revalidation

Both rounds used real Qwen3.5-9B vLLM inference for:

- Adaptive outer H1 via `nexau.AgentConfig.from_yaml` and a fresh `Agent` per
  sequential sample;
- every accepted inner H2 via the unchanged SAH NexAU runner.

| protocol round | NexAU outer traces | one assistant call each | valid native SAH H2 | NexAU inner traces | inner errors | controller decision |
|---:|---:|---|---:|---:|---:|---|
| 0 | 4 | yes | 3 | 8 / 8 non-empty | 0 | `waiting_for_plateau` |
| 1 | 4 | yes | 3 | 8 / 8 non-empty | 0 | `skipped_no_future_round` |

All six generated candidate `spec.yaml` files passed the unmodified SAH
`h2spec/1.0` validator, and all six packages loaded through NexAU
`AgentConfig.from_yaml`. Round 1 reused the same atomic protocol state and its
outer context included round 0's archive/evidence. The final state recorded
`rounds_seen=2` and collected rounds `[0,1]`.

## GPU/service isolation

- In the final two-round format check, one isolated GPU 0 vLLM service backed
  both the sequential H1 and H2 calls; no other user's service or GPU was
  reused.
- In the earlier five-round training check, GPU 0 served the active proposer
  adapter for outer proposals, GPU 1 served the unchanged base checkpoint for
  inner execution, and the real LoRA update used a separate GPU.
- All services were stopped after the loop; the final audit showed all four
  GPUs at 0 MiB with no remaining compute process.

## Earlier five-round controller/training result

| protocol round | proposer | valid candidates | outer traces | inner results | controller decision |
|---:|---|---:|---:|---:|---|
| 0 | base model | 4 / 8 | 8 | 10 | `train_required` |
| 1 | committed adapter | 3 / 4 | 4 | 8 | `skipped_no_future_round` in the original two-round smoke |
| 2 | same committed adapter | 1 / 4 | 4 | 4 | `skipped_no_signed_contrast` |
| 3 | same committed adapter | 3 / 4 | 4 | 8 | `skipped_no_signed_contrast` |
| 4 | same committed adapter | 3 / 4 | 4 | 8 | `skipped_no_future_round` |

All 24 earlier outer trajectories were non-empty. All 38 inner results retained
non-empty trajectories, and none reported an inner error. Controller state
finished with `rounds_seen=5`, collected rounds `[0,1,2,3,4]`,
`policy_updates=1`, and the committed adapter still active. As noted above,
these outer traces predate the final NexAU H1 normalization.

Round 1 was originally collected as the final round of the initial two-round
smoke. The extension resumed the same atomic state for rounds 2–4 with a
five-round horizon. Its no-update decision would also have been
`skipped_no_signed_contrast` if that longer horizon had been declared in the
first run, so this resume did not suppress a usable policy update.

## Real policy update

Round 0 produced six signed policy rows: four positive actions and two
fail-closed compiler rejections. A rank-8 LoRA weighted policy-gradient step
then completed on the same Qwen3.5-9B weights:

- trainable parameters: `1,114,112`;
- gradient norm before clipping: `1.0408626794815063`;
- parameter delta L2: `0.01534217948182527`;
- adapter digest changed from
  `03906ece3aeb1613de503fb3a18e41eec8c79fed420fcc21e8c3357c4983ffba`
  to
  `c0d2c4fb169070626e5bbbeb97983ab2498b84b8b2cc644108211baca295f450`;
- peak allocated CUDA memory: `29,647,298,560` bytes.

The update manifest was committed only after save success. The next four
earlier rounds all used that committed adapter for proposal. The local replay
conversion preserved all 6/6 signed rows and emitted `tools=[]`, matching the
Adaptive plain-text action contract. The final two-round format revalidation
did not trigger another optimizer step: its small fixture reached the score
ceiling and the declared second round had no future round that could consume a
new adapter.

## What the later rounds establish

The fixture reached its exact score ceiling (`1.0`) in round 0. Later valid
candidates could therefore be neutral but not positively improve the record.
The controller correctly accumulated evidence and advanced the plateau counter
without manufacturing positive credit or repeatedly training on negative-only
data. This is the expected Adaptive v1 safety behavior: the loop continued,
while optimizer work was skipped when no signed causal contrast existed.

Consequently, the earlier run proves one real policy update followed by four
adapter-backed protocol rounds and correct no-op gating; it does not claim
multiple useful weight updates on a saturated task. The final two-round run
separately proves the outer NexAU H1 → native SAH H2 → inner NexAU execution
path and cross-round archive carryover.

## Cleanup record

Every vLLM service used by these checks was stopped at experiment exit. The
final audit on 2026-07-28 reported all four GPUs at 0 MiB, no compute
processes, and no remaining experiment process.

## Remaining environment-specific check

The production `train_mphi_step.sh` path uses the original Slime/4-GPU,
Weave, merge, Lustre, and Slurm environment. Those external services are not
available on this local node, so that scheduler-specific path was syntax- and
unit-tested but not submitted. The local GPU run instead proves the underlying
forward/backward/optimizer/save/serve and protocol state transitions.
