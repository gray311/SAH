# Adaptive v1 local GPU loop validation

- Date: 2026-07-28
- Result: PASS
- SAH substrate: `f9868c3ea06e1323d67e3817065035287662108e`

This validation used an ignored local fixture and did not add model weights,
datasets, adapters, or runtime traces to the repository. It exercised real
Qwen3.5-9B inference, NexAU inner execution, a real LoRA backward/update/save,
adapter-backed proposal, and five consecutive Adaptive protocol rounds.

## Role isolation

- GPU 0 served the active proposer adapter for outer proposals only.
- GPU 1 served the unchanged base checkpoint for inner execution only.
- The real LoRA update used a separate GPU.
- All services were stopped after the loop; the final audit showed all four
  GPUs at 0 MiB with no remaining compute process.

## Five-round result

| protocol round | proposer | valid candidates | outer traces | inner results | controller decision |
|---:|---|---:|---:|---:|---|
| 0 | base model | 4 / 8 | 8 | 10 | `train_required` |
| 1 | committed adapter | 3 / 4 | 4 | 8 | `skipped_no_future_round` in the original two-round smoke |
| 2 | same committed adapter | 1 / 4 | 4 | 4 | `skipped_no_signed_contrast` |
| 3 | same committed adapter | 3 / 4 | 4 | 8 | `skipped_no_signed_contrast` |
| 4 | same committed adapter | 3 / 4 | 4 | 8 | `skipped_no_future_round` |

All 24 outer trajectories were non-empty. All 38 inner results retained
non-empty trajectories, and none reported an inner error. Controller state
finished with `rounds_seen=5`, collected rounds `[0,1,2,3,4]`,
`policy_updates=1`, and the committed adapter still active.

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
rounds all used that committed adapter for proposal. The local replay
conversion preserved all 6/6 signed rows and emitted `tools=[]`, matching the
Adaptive plain-text policy format.

## What the later rounds establish

The fixture reached its exact score ceiling (`1.0`) in round 0. Later valid
candidates could therefore be neutral but not positively improve the record.
The controller correctly accumulated evidence and advanced the plateau counter
without manufacturing positive credit or repeatedly training on negative-only
data. This is the expected Adaptive v1 safety behavior: the loop continued,
while optimizer work was skipped when no signed causal contrast existed.

Consequently, this run proves one real policy update followed by four
adapter-backed protocol rounds and correct no-op gating; it does not claim
multiple useful weight updates on a saturated task.

## Remaining environment-specific check

The production `train_mphi_step.sh` path uses the original Slime/4-GPU,
Weave, merge, Lustre, and Slurm environment. Those external services are not
available on this local node, so that scheduler-specific path was syntax- and
unit-tested but not submitted. The local GPU run instead proves the underlying
forward/backward/optimizer/save/serve and protocol state transitions.
