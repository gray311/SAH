# SAH — Self-Adapt Harness

Train a **harness-proposer** LoRA (`M_phi`) with RL so it writes better *discovery
harnesses* (`H2`) for a **permanently frozen executor** `M0` (Qwen3.5-9B). No weights
of `M0` are ever updated — all learning lives in the proposer.

```
inner loop:   M0  +  H2         ->  solution + reward   (executor is frozen)
outer loop:   M_phi + H1(tau)   ->  K candidate H2       (this is what we RL-train)
```

For task instance `tau`, `M_phi` running the fixed proposer harness `H1` emits `K=8`
task-conditioned candidate harnesses `H2`. Each `H2` drives `M0` through one inner
rollout on `tau` (≤20 evaluations), yielding one reward. The `K` rewards form **one
instance-wise GRPO group**; the policy gradient trains `M_phi` on the *outer* (H2-
generation) trajectories. One task per step, online. See [`plan.md`](plan.md) for the
full spec.

## Layout

| path | what |
|------|------|
| `src/inner/` | inner loop: EFT task registry, program-edit (EVOLVE-BLOCK / SEARCH-REPLACE), subprocess-isolated evaluator, `run_baseline` CLI, the initial `H2` NexAU package (`harness/`) and candidate scaffold (`harness_candidate/`) |
| `src/outer/` | outer loop: `HarnessSpec` typed genome + fail-closed validation, the fixed `H1` proposer NexAU package (`harness/`), `propose`/`materialize`/`rewards`/`outer_round` (per-task GRPO group) |
| `src/training/` | `grpo_batch -> Weave slime replay` conversion + LoRA training driver |
| `src/protocols/` | optional protocol adapters; Adaptive v1 is isolated here and imports only when selected |
| `scripts/` | Slurm sbatch + in-container workers for one outer step (propose → rollouts → collect → train → merge) |
| `results/` | `maintable.md` (vs official Qwen3.5-9B / Finch-9B), campaign targets, baselines |

**Harness rule:** every harness — the initial `H2`, every candidate `H2`, and
each protocol's proposer `H1` — is a declarative **NexAU package**
(`agent.yaml` plus its referenced prompt/tool/skill/middleware assets), never a
bare `.py` script. Packages may intentionally declare empty tool, skill, and
middleware lists.

## Dependencies (external, not vendored)

- **[NexAU](https://github.com/gray311/NexAU)** — agent framework (`Agent`, `AgentConfig.from_yaml`)
- **Weave_v2** — slime offline GRPO / LoRA training stack (reused for the outer update)
- **[evolution-fine-tuning](https://github.com/Open-Galapagos/evolution-fine-tuning)** — the EFT benchmark (22 tasks); eval data is prepared into `$DATASET_ROOT/self_adapt_harness/` (not committed)
- `M0` = Qwen3.5-9B; served with vLLM (`--enforce-eager --language-model-only --enable-auto-tool-choice --tool-call-parser qwen3_xml`)

Cluster paths are read from `$CODE_ROOT / $DATASET_ROOT / $MODEL_ROOT / $RUN_ROOT`
(see `config/workspace_env.sh` on the cluster); scripts assume a GB200 (aarch64) +
Slurm + pyxis/enroot environment.

## Training modes

The current SAH path remains the default. Both modes now use declarative NexAU
packages for the outer H1 proposer and every inner H2 executor. The optional
`adaptive_v1` protocol reuses SAH's native `h2spec/1.0` materializer, frozen
inner executor, rollout service, and proposer trainer; it changes only the H1
proposal policy/context, matched-repeat controller, dual-frontier selection,
and plateau-gated update cadence. Its Adaptive-only entry point defaults to
`max_eval=30`; the original SAH defaults are unchanged:

```bash
bash scripts/unified_campaign.sh sah <existing fresh_campaign args...>
bash scripts/unified_campaign.sh adaptive_v1 <task> <rounds> <round_base> [workspace]
```

See [`docs/ADAPTIVE_V1_UNIFICATION.md`](docs/ADAPTIVE_V1_UNIFICATION.md) for
the exact shared boundary, Agent topology, state/recovery semantics, and local
tests.

## Status

Instance-wise online GRPO campaign, iterating task-by-task until each beats Finch-9B.
Trained-`M_phi` steps have produced harnesses that beat Finch back-to-back
(Hadamard 0.509 > 0.481, Transaction 3788 > 3636). See `results/maintable.md` and
`results/finch_targets.json`.
