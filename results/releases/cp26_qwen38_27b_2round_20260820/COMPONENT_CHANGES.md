# Component changes across the 16 proposer harnesses

## Exact accounting

All 16 proposals changed the existing `system_prompt` component by appending
task-specific instructions; none rewrote or removed the inherited core prompt.

| Component operation | Count |
|---|---:|
| Existing `system_prompt` appended | 16 |
| New tool materialized | 1 |
| New skill materialized | 1 |
| New middleware materialized | 0 |
| Existing core tool/skill/middleware removed or replaced | 0 |

The only new materialized components were:

- Round 1 cand04: skill `circle-packing-n26`.
- Round 1 cand07: tool `packing_probe`.

Round 0 cand00 mentions a hypothetical `packing_feasibility` tool inside its
prompt, but its submission did not declare or materialize that tool. Its
`component_manifest.json` correctly records zero new tools. It is therefore
prompt text, not an available runtime component.

Exact prompts and component bodies are retained per candidate in
`03_proposer_raw_submission.txt`; the materialized view and lineage are in
`04_generated_harness.json`.

## Round 0

All round-0 candidates inherited the frozen core harness and appended one
circle-packing strategy section. No round-0 candidate materialized a tool,
skill, or middleware.

| Harness | Materialized component delta | Appended prompt strategy |
|---|---|---|
| cand00 | `system_prompt` only; repaired submission | Describes a non-materialized `packing_feasibility` helper; rank grid, hex, layered, and two-ring center layouts before evaluation; emphasize mixed radii and symmetry breaking. |
| cand01 | `system_prompt` only | Dense grid/layered base, binding-constraint analysis, targeted center perturbations, mixed radii, explicit fast constructor, switch family after two stalls. This was the causal-credit winner and became the round-1 harness parent. |
| cand02 | `system_prompt` only | Explicit centers and constraint-derived radii; hex lattice, layered shells, corner anchoring, asymmetric mixed radii; local grow sweeps; probe several structural variants before full evaluation. |
| cand03 | `system_prompt` only | Parametric layered rows such as 5+6+5+6+4, hex patch plus corner fill, iterative equal-violation radius solver, optional bounded Newton polish. |
| cand04 | `system_prompt` only | Hard feasibility checks, iterative min-constraint radius assignment, hex/grid/shell/mixed families, probe-based ranking and bounded local center polish. |
| cand05 | `system_prompt` only | Explicit 26-center table, hex/triangular core with large corner circles, mixed radii, one structural hypothesis per edit, diagnose a single invalid constraint rather than shrinking everything. |
| cand06 | `system_prompt` only; repaired submission | Explicit hex grid, square grid plus gap fill, mixed-radius border plus core; analytic radii, symmetry with selective asymmetry, no open-ended internal search. |
| cand07 | `system_prompt` only | Triangular lattice with row counts near 5+6+6+5+4, constrained-first greedy radii, bounded deterministic local relaxation and small asymmetric edge shifts. |

Two submissions, cand00 and cand06, originally failed to call
`submit_harness` and were repaired into valid prompt-only harnesses. Their
repaired status is preserved in each generated-harness artifact.

## Round 1

The round-1 harness parent was round-0 cand01. Every round-1 candidate retained
that prompt verbatim and appended another section.

| Harness | Materialized component delta | Appended prompt strategy |
|---|---|---|
| cand00 | `system_prompt` only | Protect/evaluate the seed first, probe before committing, cap work per family, consolidate with three evaluations left; replace multi-init L-BFGS+LP with one explicit dense tiling plus short relaxation. |
| cand01 | `system_prompt` only | Treat the deterministic task as unsuitable for probing; self-verify and print validity, sum, and worst slacks; reject invalid or below-best layouts before an official evaluation. |
| cand02 | `system_prompt` only | Winner. Probe structural edits, at most two evaluations per family, then follow a ladder: 5×5 grid+1, layered rows, mixed-radii grid, targeted perturbation; keep construction explicit and deterministic. |
| cand03 | `system_prompt` only | Override the LP path with a fast two-pass radius rule; layered hex base, corner perturbation, mixed-radius shell; use direct evaluation rather than probing. |
| cand04 | `system_prompt` + new skill `circle-packing-n26` | Auto-enacted mandatory playbook: score arithmetic, layered rows, corner-anchored shells, hex patch, mixed-radius refinement, and a staged 20-evaluation plan. The skill overrides the earlier generic family list. |
| cand05 | `system_prompt` only | Explicit dense baseline, probe 2–3 variants, relax binding constraints rather than cosmetics, switch families after two misses, consolidate late. |
| cand06 | `system_prompt` only | Two-phase schedule: spend evaluations 1–6 rapidly testing grid/lattice/row families, then use the remainder only for targeted perturbations of the best family; finish with four evaluations left. |
| cand07 | `system_prompt` + new tool `packing_probe` | Conditional local radius-redistribution tool. Given centers/radii, returns input/output sums, recoverable gain, redistributed radii, overlap check, and top wall-headroom circles without spending evaluator budget. |

## Added component bodies

### `circle-packing-n26` skill

The skill is embedded in
`round001/candidates/cand04/03_proposer_raw_submission.txt`. It provides:

- exact score/binding-constraint arithmetic;
- four ordered construction families;
- a 1–4 / 5–12 / 13–18 / 19–20 evaluation schedule;
- explicit-constructor and stall-switching rules.

### `packing_probe` tool

The tool schema and Python implementation are embedded in
`round001/candidates/cand07/03_proposer_raw_submission.txt`. It:

- clamps radii to wall limits;
- resolves pairwise overlaps;
- redistributes slack toward circles with wall headroom;
- reports gain and locally useful radius/headroom diagnostics;
- performs no program execution, file I/O, or evaluator call.

No proposer added middleware in either round.
