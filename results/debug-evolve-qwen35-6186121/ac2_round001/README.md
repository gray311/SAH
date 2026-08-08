# AC2 round-1 inspection bundle

This bundle is a lossless view over `/lustre/fsw/portfolios/av/projects/av_alpamayo_reasoning/users/yingzim/runs/campaigns/debug-evolve-qwen35-6186121`. Original artifacts remain the
source of truth; every exported JSON keeps complete message content.

- Task: `eft__math__second_autocorr_ineq`
- Harness candidates: `8`
- All candidates share identical proposer model-conditioning content:
  `True` (per-message envelope IDs are preserved separately)
- Executor results currently present: `8/8`
- Training rows currently present: `8/8`

For each `candidates/candXX/` directory, read files in numeric order:

1. `01_proposer_exact_input.json`
2. `02_proposer_full_trajectory.json`
3. `03_proposer_raw_submission.txt`
4. `04_generated_harness.json`
5. `05_executor_exact_input.json`
6. `06_executor_full_trajectory.json`
7. `07_executor_reward.json`
8. `08_executor_output_program.py`
9. `09_proposer_grpo_training_row.json`
10. `10_qwen_training_replay_row.json`

The reward-to-training mapping is in `training/reward_advantage_table.json`
and `training/training_contract.json`. A positive advantage increases the
likelihood of the exact H1 assistant decisions that produced that harness; a
negative advantage decreases it. H2 messages are evidence used to compute the
outcome, not the proposer model's token-level training target.

## Candidate outcomes and proposer update direction

| candidate | executor score | reward | advantage | proposer update |
|---|---:|---:|---:|---|
| cand00 | 0.992403556451 | -0.007386896644 | +0.057463333848 | increase H1 action likelihood |
| cand01 | 0.980520432265 | -0.019272529950 | -0.008883756437 | decrease H1 action likelihood |
| cand02 | 0.970224531137 | -0.029570605056 | -0.033556731517 | decrease H1 action likelihood |
| cand03 | 0.995758332188 | -0.004031412546 | +0.092250506045 | increase H1 action likelihood |
| cand04 | 0.960746421564 | -0.039050715931 | -0.046861469416 | decrease H1 action likelihood |
| cand05 | 0.985711531352 | -0.014080334763 | +0.012388885624 | increase H1 action likelihood |
| cand06 | 0.954826984197 | -0.044971403187 | -0.053245732860 | decrease H1 action likelihood |
| cand07 | 0.976878832658 | -0.022914898480 | -0.019555035287 | decrease H1 action likelihood |

After the one-step LoRA job completes, the exact argv, checkpoint audit, full
trainer log, merged-weight audit, serve-protocol validation, and final audit
are copied losslessly to `training/11_*` through `training/16_*` by rerunning
this builder.
