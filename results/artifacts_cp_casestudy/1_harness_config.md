# Artifact 1 — Harness config: baseline vs evolved

Full files: `baseline_agent.yaml` (the fixed seed harness, `src/inner/harness/`)
and `evolved_agent.yaml` (round300/cand06). Diff summary:

| field | baseline | evolved (cand06) |
|---|---|---|
| tools | edit_solution, evaluate_solution, probe_solution, finish | **+ analyze_geometry** (generated) |
| skills | discovery-optimization | **+ circle-packing-strategies** (generated) |
| middlewares | budget_reminder, stall_restart, long_tool_output, round_reminder | **+ probe_reminder** (generated, before_model hook) |
| sampling.temperature | 0.7 | **1.2** |
| agent.max_iterations | 36 | **60** |
| system_prompt | generic "improve the EVOLVE-BLOCK" | packing-specific: "use a lattice, replace not patch" |

So the candidate differs from the seed harness on **all four generative axes**
(tool code, skill text, middleware code, prompt) plus two sampling knobs — not
just hyperparameters. See the generated code:

- `evolved_new_tool.py` — `analyze_geometry(ctx, args)`: reads `ctx.get_program()`,
  detects hexagonal/ring/spiral cues, returns lattice-spacing suggestions.
- `evolved_new_skill.md` — the n=26 packing playbook.
- `evolved_new_middleware.py` — `probe_reminder`: on `before_model`, if evals_left
  ≤ 5 injects "call probe_solution to rank variants first".

All three passed the static AST gate + frozen-M0 reviewer + runtime-isolation
self-test before materialization (§4.2 of IMPROVEMENTS.md).
