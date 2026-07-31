# Artifact 2 — Proposer (M_φ) input → output

The trained proposer M_φ runs the H1 agent once and emits ONE harness spec for
this task instance. Full emitted spec: `proposer_output_spec.yaml`.

## INPUT to M_φ (what it conditions on)

- **Task description**: pack 26 ±-radius circles in a unit square, maximize Σr.
- **Seed program** (the current EVOLVE-BLOCK M0 will edit).
- **Scores** it is told:
  ```
  seed program alone:    0.364237
  current harness best:  0.560823   ← the harness it is mutating stalls here
  budget: 20 evals
  ```
- **The current harness spec** (h2spec/1.0) it is mutating — a generic
  "iteratively improve the program to maximize performance" harness.
- Task: "analyze why the current harness reaches only 0.56 here; design ONE
  tailored spec; validate_spec then submit_spec."

So M_φ sees a concrete failure signal (0.56 ≪ target) and is asked to diagnose
and redesign — not to guess blindly.

## OUTPUT from M_φ (the spec it submitted)

M_φ produced a **partial spec that touches every generative axis**
(`changed_fields`):

```
system_prompt, skill_description, skill_body, tool_descriptions,
sampling, agent, middleware, new_tools, new_skills, new_middlewares
```

Concretely it wrote:
- `new_tools: [analyze_geometry]` — a tool that reads the packing and names the
  lattice (see `evolved_new_tool.py`).
- `new_skills: [circle-packing-strategies]` — the n=26 construction playbook.
- `new_middlewares: [probe_reminder]` — front-load cheap probes.
- raised `sampling.temperature` to 1.2 and `agent.max_iterations` to 60.
- rewrote the system prompt to "use a lattice, replace don't patch".

This is the diagnosis→redesign the input asked for: the proposer decided the
generic harness stalled because M0 had no geometric target and no cheap way to
rank variants, and injected exactly those capabilities. The spec then passes the
SAH validator + safety gates before it is materialized into `evolved_agent.yaml`.
