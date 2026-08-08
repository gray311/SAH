# Worked example — the AC2 round-1 report

Source bundle: `results/debug-evolve-qwen35-6186121/ac2_round001/`
Output: `REPORT.html`, written **into** that directory.
Branch: the bundle and its report live on `results/ac2-round001-6186121`
(commit `e106501`); this skill lives on the branch where `.claude/skills/` is.

Shadowing `$RUN_ROOT/campaigns/debug-evolve-qwen35-6186121`, schema
`ac2-round-inspection/1.0`, task `eft__math__second_autocorr_ineq`, K = 8.

## What the inventory turned up

| path | what it gave the report |
|---|---|
| `manifest.json` | task, round, K, shared proposer-conditioning sha, per-candidate scores and result paths, training block |
| `README.md` | the candidate/reward/advantage table, the file-order convention, the H1-vs-H2 training statement |
| `training/training_contract.json` | reward formula, `SAH_ADV=v2`, `rloo+max(a=0.3)`, `base_score`, group hygiene flags, `loss_target` |
| `training/reward_advantage_table.csv` | the numeric table actually plotted |
| `training/11_*`–`16_*` | exact argv, grad norm, adapter hashes, merged-model audit, live serve-protocol smoke test |
| `deep_dive/candidate_matrix.json` | per-candidate changed fields, component lineage, ledger, and the step-by-step eval trace (this is where the three invalid intermediate evals came from) |
| `deep_dive/MECHANICAL_DIGEST.md` | proposer/executor call chronology and the prompt deltas |
| `causal_attribution/README.md` | **the finding**, and the five training-policy rules |
| `paired_replay_cand01/paired_effect.json` | the matched-pair assertions and `causal_delta` |
| `patched_replay_cand03/enactment_budget_audit.json` | skill mount/load/injection counts, budget ledger, tool order |
| `contract_replay_cand03/{FAILED,PASSED_REAUDIT,component_contract_audit.json}` | the over-strict assertion case |

## The finding it leads with

Not "cand03 scored 0.9958". The bundle contains a matched-seed control showing
that cand01's gross gain of +0.025693 over the seed program decomposes into
+0.023317 already produced by the **parent** H2 route and only +0.002376 —
**9.25%** — attributable to the candidate harness. Ranking candidates by absolute
score therefore rewards executor-route luck as much as harness quality, and the
bundle's response was to redefine proposer reward as the mean matched effect
`candidate_score − parent_control_score`.

The report is structured so a reader meets that in the lead paragraph and again
as its own section, with the scoreboard demoted to section 1.

## Claim → evidence mapping

| claim | evidence |
|---|---|
| 8/8 candidates score-eligible and completed | `manifest.json` |
| all candidates share byte-identical proposer conditioning | `manifest.json → proposer_model_conditioning_sha256` |
| 7 changed only `system_prompt`; cand03 added skill `c2-optimization` | `candidate_matrix.json → changed_fields, component_lineage` |
| per-candidate score / reward / advantage | `training/reward_advantage_table.csv` |
| three candidates burned an eval on an invalid program | `candidate_matrix.json → steps[].error` |
| reward is gap-closure vs `base_score = 0.999789`, not the score | `training_contract.json → reward_and_advantage` |
| advantages sum to ≈0; 3 positive / 5 negative | `training_contract.json → advantage_sum` |
| gradient step landed: grad norm 0.07394, 256 adapter tensors | `training/12_optimizer_step_audit.json` |
| merged model serves and parses tool calls | `training/15_merged_serve_protocol.json` |
| loss target is H1 assistant tokens; H2 is evidence, not a target | `training_contract.json → loss_target`, `README.md` |
| no candidate improved on the incumbent, yet training was not suppressed | `training_contract.json → raw_improved, training_suppressed` |
| paired effect +0.002376 = 9.25% of gross | `paired_effect.json → causal_delta`, `causal_attribution/README.md` |
| candidate and control produced different programs | `paired_effect.json → *_program_sha256` |
| the "Gaussian tail" is mathematically exponential decay | `causal_attribution/README.md`, `cand01/06_executor_full_trajectory.json` |
| the step family was already available to the base executor | `causal_attribution/README.md`, `paired_replay_cand01/control/` |
| cand03's skill was mounted but never loaded | `candidate_matrix.json → cand03.skill_audit` (`mounts 1, loads 0`) |
| root cause was executor policy, not a registry failure | `causal_attribution/README.md § cand03` |
| patched runtime injects the playbook before the first edit | `enactment_budget_audit.json → skill_audit` |
| the five post-fix training rules | `causal_attribution/README.md § Training policy after the fix` |

## Charts and why each form

1. **Best score per candidate — dot plot.** Every value sits in 0.954–0.996. Bars
   would need a truncated baseline. Dashed reference lines mark the seed
   (0.954827) and the base (0.999789); stems run from the seed so the visible
   span is exactly the gain. `✦` marks the one candidate that added a component.
2. **Advantage per candidate — diverging bars.** True zero, blue positive / red
   negative, and the legend states the *meaning* of the sign ("reinforce" /
   "suppress" H1 actions) rather than just "positive/negative".
3. **cand01 gain decomposition — stacked from zero.** 90.75% parent-route in
   neutral gray, 9.25% candidate-attributable in series-1 blue. The narrow blue
   segment's label sits outside the bar, which is why `decomposition()` takes a
   large right margin.

All three carry hover tooltips with the full-precision values, so the rounded
on-chart labels never have to be trusted.

## The two things it flagged instead of smoothing

1. **`contract_replay_cand03/FAILED`** (returncode 1) sits next to
   `PASSED_REAUDIT`, which says the Slurm exit "reflected an over-strict
   literal-heading assertion; all causal component-contract gates passed on the
   immutable trajectory". The report shows the full assertion list with the one
   advisory failure marked, and states this explicitly — reporting the `FAILED`
   alone would invert the conclusion.
2. **`config/examples/ac2_paired.yaml`**, named by `causal_attribution/README.md`
   as the runnable campaign template, **does not exist** (the repo has only
   `adaptive_full.yaml` and `sah_v3_deep.yaml`). Rendered as a dashed
   `.ev.missing` span saying so, not as a link.

And one caveat carried rather than dropped: the 9.25% rests on a **single**
matched pair, which the bundle itself says is insufficient for stable training
credit (`reward.paired_repeats` ≥ 3 for real campaigns). The report states it as
an existence proof that gross gain overstates harness credit, not as a calibrated
coefficient.
