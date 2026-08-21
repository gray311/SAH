# CP26 — Qwen3.8-27B — two-round evolve release

This release contains the versionable evidence for the formal CP26
(`eft__math__circle_packing`) experiment:

- Qwen3.8-27B as proposer and frozen executor.
- Two complete evolve rounds.
- One real LoRA/FSDP proposer update between rounds.
- Eight proposer harnesses, eight candidate executor rollouts, and eight
  paired same-seed controls per round.

The experiment was run on 2026-08-20 in
`cp-q27-full2r-guard512-20260820_180000`.

## Result

| Stage | normalized score | raw `sum_radii` | selected candidate |
|---|---:|---:|---|
| Initial program | 0.3642368945 | 0.9597642170 | seed |
| Round 0 ratchet | 0.9563198357 | 2.5199027670 | cand00 |
| Round 1 ratchet | 0.9959631266 | 2.6243628386 | cand02 |

Round 1 `cand02` scored `0.9959631265863883` against its paired control
`0.9789794997638883`, a causal delta of `+0.016983626822499986`.

## Model topology

- Frozen executor: `Qwen/Qwen3.8-27B`, TP=2 × 4 replicas.
- Round 0 proposer: frozen-base Qwen3.8-27B.
- Round 1 proposer: seven charged slots from the round-0 merged 27B update,
  plus one frozen-base 27B diversity slot.
- Context length: 49,152; context guard safety: 512 tokens.

The actual round-1 server commands are preserved in
`round001/artifact_index.json`. Those commands, rather than the pre-resolution
static topology view, are authoritative for the loaded checkpoints.

## Contents

- `round000/`, `round001/`: self-contained per-round bundles. Each candidate
  contains proposer exact input, proposer full trajectory, raw harness
  submission, generated harness, executor exact input, executor full
  trajectory, reward, output program, GRPO row, Qwen replay row, paired-control
  trajectory, and paired-control reward.
- `COMPONENT_CHANGES.md`: component-level accounting for all 16 generated
  harnesses.
- `EXPERIMENT_SUMMARY.md`: full human-readable experiment report.
- `experiment_summary.json`: machine-readable cross-round result.
- `evidence/`: round summaries, ratchet/gate audits, training manifests,
  recovery manifests, model/runtime provenance, and Slurm completion records.
- `FULL_RUN_INVENTORY.json`: content-addressed inventory of the complete raw
  run (3,872 entries, 58,684,943,678 bytes).
- `MANIFEST.sha256`: SHA-256 for every versioned release file.

Open `round000/REPORT.html` or `round001/REPORT.html` for the visual reports.

## Training evidence

The update used Ray/FSDP world size 8 and LoRA rank 64 / alpha 128. It trained
318,767,104 of 27,675,495,664 parameters (1.1518%) for three optimizer steps,
then merged the adapter into a full 27B export.

`evidence/training/merged_manifest.json` records
`weights_changed_vs_previous_manifest=true` and hashes both merged weight
shards. The actual model tensors and adapter checkpoints are intentionally not
stored in Git.

## Recovery disclosure

Three round-1 paired controls initially hit a moving vLLM diagnostic boundary:
42,500 input tokens plus 6,653 requested output tokens exceeded the 49,152
context by one token. The failed attempts were preserved in the raw run and the
same-seed controls were recovered with the documented context-guard overlay.

Logical trajectory accounting is 48 across the two rounds; transparent
physical-attempt accounting is 51. All 32 official candidate/control
trajectories are eligible, completed, and error-free. See
`evidence/recovery/`.

## Storage policy

This Git release contains all lightweight, paper-facing trajectory and harness
artifacts plus hashes/provenance for the full raw run. It deliberately excludes:

- the 54.7 GB merged model tensors;
- the 3.6 GB adapter checkpoints;
- duplicated runtime source snapshots;
- vLLM/Ray server logs and bulky mutable run state.

Those objects are represented by `FULL_RUN_INVENTORY.json` and the merged
model manifest. This keeps the release reviewable and follows the repository
policy of not committing model weights or complete raw run trees.

## Verify

```bash
sha256sum -c MANIFEST.sha256
```
