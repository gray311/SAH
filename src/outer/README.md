# src/outer — the outer loop (M_phi + H1 → new H2)

**Outer loop:** `M_phi + H1 → K candidate H2`. **Inner loop** (src/inner):
`M0 + H2 → solution + reward`. RL (GRPO) updates **only** `phi` — M0 stays
frozen forever (plan.md §0).

## One round

```
1. propose   M_phi (Qwen3.5-9B ⊕ LoRA phi) + fixed H1 prompt
             --K samples--> K=8 HarnessSpec YAMLs
             → fail-closed validation (must differ from current best H2;
               duplicates/invalid kept as records with fixed reward -1)
             → materialize each valid spec into a FULL NexAU package:
               candNN/{agent.yaml, prompt.md, tools/, skills/, middlewares/}
2. rollouts  frozen M0 + each candidate H2 → 8 tasks × ≤20 evals
             (one process per candidate; replicas sharded over 4 GPUs)
3. collect   per-task reward = clip((score - baseline)/|baseline|, ±1)
             candidate reward = mean over tasks
             GRPO advantage = (R_k - mean)/(std+eps) over the 8-candidate group
             → grpo_batch.jsonl (+ round_summary.json)
4. train     src/training: convert → Weave slime offline-GRPO → merged M_phi
5. iterate   best candidate = next round's BASE_HARNESS; merged ckpt = next
             round's proposer
```

## The genome (HarnessSpec v0.1)

M_phi does not write arbitrary code (plan.md §5 MVP): it emits a typed YAML
spec — `system_prompt`, `skill_description`, `skill_body`,
`tool_descriptions.{edit_solution,evaluate_solution,finish}`,
`sampling.{temperature,top_p,top_k,max_tokens}`, `agent.max_iterations`,
`middleware.{budget_reminder_from_left,long_tool_output_max_chars}`.
Missing fields inherit the base harness; unknown fields fail closed; the
evaluation budget is NOT in the spec (enforced externally, plan.md §8.4).
`materialize.py` compiles a spec deterministically into the full package
(tool/middleware *code* is the fixed executor contract, shared; candidate
`middlewares/` carries the imported per-candidate copy).

## Files

| File | Role |
|---|---|
| **`harness/`** | **H1 — the FIXED proposer harness, a full NexAU package**: `agent.yaml` + `system.md` + `tools/{validate_spec,submit_spec}` + `skills/harness-design/` + `middlewares/submit_reminder.py`. The proposer drafts a spec, `validate_spec`s it (free), then `submit_spec`s (stop tool). Never mutated; hashed for provenance. |
| `harness_spec.py` | spec schema, fail-closed validation, canonical hash, base-spec extraction, diff-vs-base |
| `h1.py` | round-context builder (user message = base spec + per-task baseline) + H1 package hash |
| `propose_session.py` | ProposeSession state + contextvar bridge behind H1's tools |
| `propose.py` | run the H1 agent K times (threaded across replicas) → CandidateRecords (+ full trajectories for GRPO) |
| `materialize.py` | effective spec → full candidate package (matches `src/inner/harness_candidate/candNN` scaffold) |
| `rewards.py` | per-task normalized rewards vs `results/baseline_h2_20ev.json`, GRPO group advantages |
| `outer_round.py` | CLI: `propose` / `collect` |

Both loops' harnesses are declarative NexAU packages: H1 = `src/outer/harness/`
(fixed), H2 = `src/inner/harness/` (round-1 base) and `round00r/candNN/`
(generated candidates). GRPO trains on the proposer's full H1 trajectories
(draft→validate→submit tool calls), which is exactly the multi-turn format
Weave's slime stack masks and trains on.

Round artifacts land in `$RUN_ROOT/self_adapt_harness/outer/round00r/`:
`round.json, prompt.json, responses.json, candNN/…, rollouts/candNN/…,
grpo_batch.jsonl, round_summary.json`.

## Run

```bash
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
mkdir -p "$LOG_ROOT/slurm"
ROUND_ID=1 sbatch scripts/outer_round.sbatch      # ~2.5-4h on one 4-GPU node
# then: src/training/README.md  (GRPO on phi via Weave's stack, merge, round 2)
```

Default rollout task set (8, diverse + CPU-cheap + non-saturated):
circle_packing, hadamard, erdos, prism, txn_scheduling, eplb,
convolve2d_full_fill, psd_cone_projection.

## Round-1 note

In round 1 phi = 0, so M_phi ≡ M0 weights and one served checkpoint plays both
roles. From round 2 (trained phi) the worker must serve the merged M_phi for
`propose` and the frozen base for the inner loop — flagged TODO(round2) in
`scripts/_outer_round_worker.sh`.
