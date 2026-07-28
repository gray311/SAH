# Adaptive v1 final-code local GPU validation

- Date: 2026-07-28
- Result: PASS
- Tested branch commit: `4dc9a8b`
- SAH substrate: `f9868c3ea06e1323d67e3817065035287662108e`

This check ran the final unified code for four protocol rounds with real
Qwen3.5-9B inference, NexAU outer and inner Agents, matched outcome/promotion
rollouts, one real rank-8 LoRA optimizer step, adapter serving, and a
cross-process campaign resume.

The dataset, model weights, adapter, raw traces, and experiment logs stayed in
ignored local fixtures. They are not committed to the repository.

## Run topology

Phase 1 used a base Qwen3.5-9B vLLM service for rounds 0 and 1. After round 1
produced a digest-bound training manifest, that service was stopped and a real
LoRA update ran on a different authorized GPU. `commit-update` recorded the
adapter only after the optimizer and save completed.

Phase 2 started in a new shell/Python process. It recovered protocol round 2,
the working H2, the adapter path, the previous checkpoint, and the committed
batch from `campaign-status`. It then served:

- trained `mphi-final` on GPU 0 for Adaptive H1 proposals; and
- unchanged base `qwen3.5-final` on GPU 1 for frozen H2 execution.

This makes rounds 2 and 3 direct evidence that the committed update can be
loaded and consumed after an orchestration restart.

## Four-round result

| protocol round | proposer | valid native H2 | matched inner runs | controller decision |
|---:|---|---:|---:|---|
| 0 | base `qwen3.5-final` | 4 / 4 | 20 / 20 | `waiting_for_plateau` |
| 1 | base `qwen3.5-final` | 1 / 4 | 8 / 8 | `train_required` |
| 2 | trained `mphi-final` | 2 / 4 | 12 / 12 | `skipped_no_signed_contrast` |
| 3 | trained `mphi-final` | 2 / 4 | 12 / 12 | `skipped_no_future_round` |

All 52 planned rollout processes exited successfully. The final controller
state recorded:

- collected rounds `[0, 1, 2, 3]`;
- `next_protocol_round=4`;
- `policy_updates=1`;
- the round-1 adapter still active; and
- `pending_training=null`.

The fixture reached its score ceiling (`1.0`) in round 0. The later skip
decisions are therefore expected: the controller neither manufactures signed
credit at the ceiling nor trains an adapter that no future round can consume.

## Trace and package evidence

Every round recorded `h1_version=adaptive-h1/1.0` and the same whole-package
hash, `sha256:81eb14383fe5f483`.

- 16 / 16 outer trajectories were non-empty.
- 16 / 16 outer trajectories contained exactly one assistant message.
- Rounds 2 and 3 recorded `proposer.model=mphi-final`.
- All 9 accepted candidate specs passed the unmodified SAH
  `h2spec/1.0` validator.
- All 9 accepted packages loaded through NexAU `AgentConfig.from_yaml`.
- 52 / 52 inner result trajectories were non-empty.
- 52 / 52 inner runs ended with `stop_reason=completed`.
- No inner step reported an error, and every recorded score/advantage was
  finite.
- Seven invalid or duplicate proposals failed closed and were never executed
  as H2.
- Candidate packages contained no generated `__pycache__` directories.

The files retain the normal SAH layout: `round.json`, `prompts.json`,
`trajectories.json`, rollout results, `round_summary.json`, and
`next_bases.json`. Adaptive additionally records
`adaptive_rollout_plan.json`, the atomic protocol state, and (only when
required) a training batch plus digest-bound manifest.

## Real policy update

The round-1 batch contained eight policy rows:

- 4 positive;
- 3 negative; and
- 1 neutral.

The real Qwen3.5-9B LoRA step reported:

- trainable parameters: `1,114,112`;
- gradient norm before clipping: `0.1732354611158371`;
- parameter delta L2: `0.015336642475539794`;
- adapter digest before:
  `0908e76daceefbfcd81e8cbd342bc209155f94887b28f7988e5cd2310e8b9fb9`;
- adapter digest after:
  `dcf66cc32cb0e03d29a157e7529753c440e0d1222fc13137205e7dedd036f951`;
- peak allocated CUDA memory: `34,025,406,976` bytes.

The non-zero gradient and parameter delta plus the changed digest demonstrate
that an optimizer step changed the saved adapter. The phase-2 vLLM log then
explicitly reported loading that adapter as `mphi-final`.

## GPU and service cleanup

Only GPUs 0 and 1, both verified idle before launch, were used. GPUs 2 and 3
were occupied by pre-existing Ray/vLLM workloads and were not reused,
signalled, or stopped.

At successful experiment exit:

- both experiment vLLM process groups were stopped;
- GPU 0 reported `0 MiB`;
- GPU 1 reported `0 MiB`; and
- no experiment-owned trainer, vLLM, or supervisor process remained.

An earlier discarded launch stopped before rollout because an extra local
package-audit fixture used the wrong import working directory. The candidate
itself was valid; the fixture was corrected, independently checked, and the
clean four-round campaign above was restarted from scratch. Its process group
and GPU allocation were cleaned before the restart.

## Static checks

After the GPU run:

- all 18 Adaptive protocol tests passed;
- Python compilation passed;
- `bash -n` passed for the unified campaign, worker, sbatch, and trainer
  scripts; and
- `git diff --check` passed.

## Environment boundary

This is a real local GPU training/serve/resume validation, not a production
Slime/Slurm submission. The production `train_mphi_step.sh` path additionally
depends on external Lustre, Weave, Slime, pyxis/enroot, and scheduler services
that are not available in this workspace. That scheduler-specific path was
syntax- and unit-tested but not submitted here.
