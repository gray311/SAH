# Adaptive v1 final-code local GPU validation

## Current full-surface subagent smoke (2026-07-29)

The current Adaptive-only pipeline was exercised against a real local
Qwen3.5-9B vLLM service on GPU 0 with `max_evals=30` in proposal metadata.

- both configured child analyzers executed once;
- the coordinator returned a valid
  `sah.adaptive-v1-analysis-brief/1` object;
- the in-memory trace retained one coordinator root with two nested
  `SUB_AGENT` branches;
- the standalone Adaptive H1 produced 1/1 valid native `h2spec/1.0`;
- the candidate package loaded through the shared SAH materializer;
- actual Qwen preflight counted 3,850 analyzer tokens and about 5.1k proposer
  tokens, below the 9,000 / 23,000 hard limits;
- lifecycle logs recorded vLLM startup, normal shutdown, and GPU cleanup.

Two preceding fail-closed attempts exposed and fixed real integration defects:
NexAU tool-free children require `max_iterations=2`, and the exact dossier must
be injected into each child's system context instead of relying on the
coordinator model to reproduce it. Both failed attempts also stopped their
vLLM process groups and released GPU 0.

Artifacts:
`/home/nli61/workspace/harness_train/.tools/adaptive-v1-subagent-smoke-20260729T023930/attempt3/round000`.

The subsequent CP-26 formal preflight also exposed a launch-only context
contract mismatch: a local vLLM service was started at 32,768 tokens while
the unchanged SAH inner H2 declares 131,072 tokens. One 17-edit trajectory
therefore reached 24,577 input tokens plus an 8,192-token output reservation
and failed closed with HTTP 400. The invalid campaign was terminated and GPU
0 was released. Formal reruns use SAH's native 131,072-token service limit and
check the package/service contract before starting rollouts; the Adaptive
analyzer/proposer retains its separate bounded 32K path.

The first warm-history proposal then exposed a second compression edge case:
both read-only specialists returned valid bounded JSON, but the coordinator
expanded their results into 13 near-duplicate directions and exhausted its
output allocation mid-string. The warm round failed closed before rollouts.
The final path keeps the two NexAU child summaries and uses a deterministic
schema-aware merge whenever coordinator synthesis is invalid. The merge is
strictly lossy and bounded (4 evidence items plus 3/3/3 avoid, direction, and
uncertainty items), validates every evidence ID, and records its synthesis
mode in analysis metadata.

The formal CP-26 run subsequently exposed a semantic compression issue rather
than a size failure: a specialist described a high raw score as a gain even
though its matched `learning_reward` and `relative_delta` were negative. The
merge-ready path now grounds selected evidence in deterministic dossier
metrics and labels unsupported directions as exploratory. This post-run
hardening is Adaptive-only; the frozen formal-run source snapshot and default
SAH H1 remain unchanged.

Later completed formal rounds exposed a generated-capability coherence issue.
Six tool proposals failed SAH review/self-test (undefined helpers, invalid
mock-context use, or a broken numeric construction). The frozen runner dropped
the failed tool but could still materialize surviving prompts or skills that
referred to it. The merge-ready path now requires generated implementations to
be self-contained, enforces any requested tool fraction after review, and
marks the **entire** candidate `review_rejected` if any generated tool or
middleware is dropped. The audit independently rejects a valid package with a
failed review log. A separate successful one-round tool repair revealed that
the frozen training row still contained pre-repair code; the current path
keeps that raw text only as trace provenance and trains on the reviewed
partial spec that actually ran.

The merge-ready path additionally fixes a later-round ratchet issue found by
static audit: inherited generated capabilities are no longer mislabelled as
fresh edits, and only capabilities explicitly declared by the current
proposal are re-reviewed. It also enforces the documented `ToolContext`
boundary by rejecting Adaptive tool code that reaches private or dynamically
resolved context attributes. Both checks live in the Adaptive proposal
session; SAH's default diff/reviewer path remains unchanged.

Formal round 8 exposed an artifact-gate mismatch rather than a proposal or
rollout failure. Both child analyzers ran, but malformed/truncated synthesis
JSON forced the protocol's schema-grounded deterministic dossier fallback.
The frozen auditor incorrectly required `analysis.meta.valid=true` and stopped
after proposal, before any rollout or controller mutation. All three
experiment vLLM services shut down and released GPUs 0/2/3. Recovery preserved
the proposal artifacts and resumed only after a revised auditor independently
validated the fallback brief schema and every evidence ID against the recorded
dossier. The merge-ready auditor now accepts exactly two analysis contracts:
a valid coordinator/subagent result, or an invalid-model-output marker paired
with a nonempty-error, schema-valid grounded fallback. Any other
source/synthesis combination fails closed.
The trace also showed that the design child reached its 1,024-token generation
cap in the final JSON string. The merge-ready child summaries now have a
1,536-token output allowance while retaining the same 4/3/3/3 item caps,
180-character strings, 18,000-character dossier, and 9,000-token input
preflight. This gives bounded JSON enough room to close without reintroducing
the original context overflow.

An independent prefix audit after formal round 8 validated all 9/9 completed
round directories and all 160/160 planned inner NexAU results. It recomputed
each matched outcome/promotion mean from the individual repeat outputs,
matched every request seed and executed harness path to provenance, checked
all evaluator ledgers at `max_evals=30`, and cross-checked summary samples
against the rollout plan. All 160 top-level runs completed, but their
intermediate edit attempts exposed a recurring H2 reliability pattern:
815 overlap rejections, 143 missing-`np` failures, 71 out-of-square circles,
62 NumPy index errors, and 61 missing-`construct_circles` failures.

The merge-ready Adaptive H1 is therefore versioned as
`adaptive-h1/3.3-complete-field-contracts`: it states that native
`h2spec/1.0` text fields are whole-field replacements and that imports,
constants, and helpers inside `EVOLVE-BLOCK` are mutable. A proposed H2 that
permits a full rewrite must preserve those definitions rather than falsely
describing them as frozen outside the editable region. This correction is
Adaptive-only and does not edit SAH's default inner or outer prompt.

The subsequent merge-ready revision is
`adaptive-h1/3.4-diverse-native-contracts`. It retains those complete-field
contracts, rotates a preference-only design-domain hint across a small
candidate batch, rounds any positive generated-tool quota upward, and requires
that a forced generated tool be submitted by the current proposal rather than
inherited from its base. Runtime `adaptive-runtime/1.1-nexau-compat` also omits
the unsupported `retry_backoff_max_seconds` key from Adaptive-owned NeXAU
packages. Default SAH materialization still emits its original key and layout.

Formal round 9 then reevaluated the same working harness at
`2.541421356237309` in both matched repeats, while the frozen state still
carried its prior `2.5257106781186542` estimate. That made the next prompt
report a `2.54142` seed-program score beside a stale `2.52571` harness score.
Controller `adaptive-controller/1.3-reestimated-frontiers` now refreshes
unchanged working and champion scores from their latest matched base means
without awarding proposal credit or changing the behavior-equivalence gate.

Formal round 11 exposed a second bounded-analysis edge case: coordinator JSON
contained three valid recent evidence IDs and one real but out-of-window ID,
while one child summary ended as truncated JSON. The frozen runner correctly
rejected the unsupported reference and used its grounded dossier fallback.
Merge-ready `adaptive-analysis/1.4-closed-reference-recovery` improves the quality
recovery without weakening grounding. Root-cause inspection showed that the
older successful-action ID still appeared in the dossier's compact optimizer
memory but was absent from `known_evidence_ids`, which only followed the recent
evidence slice. The builder now reserves bounded evidence slots for retained
successful actions and removes any memory ID that cannot be grounded, making
the reference closure explicit. Rebuilding the formal round-11 inputs retained
eight evidence rows, included the older confirmed action, and remained within
the same 6,000-token estimate.
Round auditor `adaptive-round-audit/1.4-closed-analysis-refs` independently
requires the declared known-ID set to equal the groundable evidence rows and
rejects any retained optimizer-memory reference outside that set.

As a second line of defense, the runtime deterministically removes genuinely
out-of-dossier model references and records a warning, then replaces every
retained finding with dossier metrics. If coordinator synthesis is unusable
and only one child JSON is complete, it preserves that child's bounded
read-only summary and records the missing child instead of discarding both.
Replaying the exact formal round-11 coordinator output retained its three
supported evidence rows and passed the strict brief validator. Replaying the
same nested traces through the partial-child path retained four grounded
performance evidence rows, recorded the truncated design child, and emitted
no unsupported design direction.

Formal round 11 then triggered the first full 47-row policy update. The local
single-GPU reference trainer reached CUDA OOM on row 5 and correctly left the
controller at `pending_training` with no adapter committed. Replaying the
exact signed batch with gradient checkpointing and per-row tensor cleanup
finished all 47 rows, produced finite gradients and a nonzero LoRA parameter
delta, loaded through vLLM, and only then passed `commit-update`. This validates
the fail-closed controller boundary; production SAH continues to use its
existing four-GPU Weave/slime trainer rather than the local recovery driver.

Formal round 12 exposed a separate evaluator-lifecycle defect. One generated
candidate entered an infinite construction loop. The frozen local wrapper
bounded each call at the dataset's 390-second timeout, while the production
SAH Slurm entry already defaulted to 120 seconds. More importantly, the
outer evaluator timeout killed only its direct worker; candidate subprocesses
created by third-party evaluators could survive as orphan CPU processes. The
merge-ready path now fixes `MAX_EVALS=30` and `EVAL_TIMEOUT=120` as paired
Adaptive invariants, records the timeout in the rollout plan, audits it, and
runs every evaluator in a fresh process group that is terminated after both
normal and timed-out evaluations. A regression test launches a real sleeping
descendant and proves it is gone when evaluation returns. These changes are
versioned as `adaptive-controller/1.4-bounded-evaluator`,
`adaptive-runtime/1.2-process-group-cleanup`, and
`adaptive-round-audit/1.5-bounded-evaluator`.

## Historical restricted-surface validation

> Historical restricted-surface validation. This run predates Adaptive's
> switch to SAH's complete native `h2spec/1.0` proposal surface. It remains an
> ablation record and does not validate generated tools, skills, or middleware.

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
