# `src/` module map

Frozen-executor bilevel RL. **Inner** = `M0 + H2 -> solution + reward` (executor
weights never change). **Outer** = `M_phi + H1 -> K candidate H2` (this is what
GRPO trains). Read `../plan.md` for the full spec.

Nothing here is dead code: modules that no other `.py` imports are loaded at
runtime through NexAU `agent.yaml` bindings or through materialized candidate
packages. Grep a binding string (e.g. `inner.harness.tools.discovery:edit_solution`)
to see who pulls a module in.

## inner/ — the inner loop (M0 drives a program search under a harness)

| file | role |
|---|---|
| `eft_task.py` | task registry: `EFTTask`, `load_tasks`, `get_task`; where each task's seed program, evaluator, and spec live |
| `program_edit.py` | EVOLVE-BLOCK split/assemble, SEARCH/REPLACE diff apply, full-rewrite parse |
| `eval_runner.py` | `evaluate_program`: writes the candidate to a temp file, runs the task evaluator in a subprocess, returns `EvalOutcome` (supports `subsample=` for cheap probes) |
| `_eval_worker.py` | the subprocess entry the runner spawns — imports+calls the evaluator in isolation, never crashes the harness |
| `session.py` | `InnerSession` (current/best program, budget ledger, checkpointing) + `probe()`; the single source of run state |
| `harness_runner.py` | builds a NexAU `Agent` from an H2 package and runs the edit→evaluate loop for one task |
| `run_baseline.py` | CLI: run M0+H2 over tasks (`--harness-dir`, `--seed-programs-file` for inheritance, `--max-evals`, ...) |
| `harness_sdk.py` | **`ToolContext`** — the capability surface handed to M_phi-generated tools (get/stage_edit/probe/evaluate/read_input_df/...); evaluator, answers, network, filesystem are unreachable by construction. `MockContext` for self-tests |
| `harness/` | **the built-in H2 package** (the initial discovery harness): `agent.yaml`, `system.md`, `tools/`, `skills/`, `middleware/` |
| `harness/tools/discovery.py` | H2's fixed tools: `edit_solution`, `evaluate_solution`, `probe_solution`, `finish` |
| `harness/tools/runtime.py` | contextvar bridge: `get_session()` (owner is `session.py`) |
| `harness/tools/custom_runtime.py` | dispatcher for M_phi-generated tools — builds a fresh `ToolContext`, loads `custom_tools/<name>.py`, traps errors |
| `harness/middleware/` | `budget_reminder`, `stall_restart` (plateau intervention) |

## outer/ — the outer loop (M_phi proposes H2; GRPO trains M_phi)

| file | role |
|---|---|
| `harness/` | **the H1 harness itself**: a complete file-native system prompt plus inspect/edit/delete/validate/submit tools over one private H2 filesystem. Fixed during training |
| `proposer_io.py` | glue around that harness (NOT H1 itself): builds the round's USER message per task, `render_feedback`, `H1_PACKAGE`/`H1_VERSION`/`h1_hash`. Renamed from `h1.py` |
| `harness_spec.py` | typed semantic H2 genome — extraction, fail-closed validation, explicit generated-component deletion, parent diff, and hash |
| `h2_workspace.py` | candidate-isolated filesystem tools and validation; `agent.yaml`/files/`prompt.md` must agree before canonical compilation |
| `propose_session.py` | `ProposeSession` + contextvar; backs H1's filesystem and submit tools |
| `propose.py` | `run_once`: one H1 agent run -> `CandidateRecord`; accepted bytes are exactly the H1-validated/submitted bytes—there is no post-submit model repair |
| `static_gates.py` | fail-closed AST gate for generated tool code (single `run(ctx,args)`, import whitelist, no os/open/exec) |
| `reviewer/reviewer.py` | static-gate + self-test helper used with repair disabled by canonical `validate_harness`; optional repair API is legacy-only |
| `reviewer/selftest.py` | subprocess self-test of a tool against `MockContext` under rlimits |
| `materialize.py` | validated semantic genome -> full canonical candidate H2; verifies but never rewrites the proposer-owned executor prompt |
| `rewards.py` | task reward + GRPO advantages: gap-normalized reward, RLOO baseline, max-weighted sharpening, zero-signal/tie guards |
| `outer_round.py` | the round orchestrator CLI: `propose` (K H1 runs -> materialize) and `collect` (rollouts -> rewards -> `grpo_batch.jsonl` + `next_bases.json`). `--force-tool-frac` for structured tool exploration |

## training/

| file | role |
|---|---|
| `grpo_to_replay.py` | convert `grpo_batch.jsonl` (H1 trajectories + advantages) into the Weave/slime offline-GRPO replay format for the LoRA trainer |

## Data flow (one round)

```
proposer_io.build_user_message ─┐
                                ▼
  outer/harness (H1) × K ── validate_harness ── submit_harness ── materialize
                                                                       │
                                          round/tasks/<task>/candNN/   ▼
                                          (agent.yaml + custom_tools/)  │
  inner/harness_runner (M0 + candidate H2) ── edit→evaluate ── score ──┘
                                │
  outer_round collect ── rewards.compute_* ── grpo_batch.jsonl
                                │
  training/grpo_to_replay ── Weave slime GRPO ── new M_phi LoRA
```
