# Qwen-235B × Circle Packing: tool-mediated transfer

## Matched result

| Field | Initial harness | Evolved harness |
|---|---:|---:|
| Model | Qwen-235B | Qwen-235B |
| Seed | 540001 | 540001 |
| OpenEvolve iterations | 48 | 48 |
| Best iteration | 1 | 1 |
| Sum of radii | 1.791181513 | 2.501998960 |
| Combined score | 0.679765280 | 0.949525222 |
| Normalized score | 68.0023% | 94.9886% |
| Validity | 1.0 | 1.0 |

The evolved harness increases the sum of radii by `0.710817447` (39.7%
relative to the initial-arm best) and the matched normalized score by **26.9862
percentage points**.

## What transferred

1. `hex-pack-complete-guide` supplies staggered-row geometry, cumulative
   indexing, and a probe-before-evaluate workflow.
2. `hexagonal_construction` validates the requested row counts and directly
   stages a complete solver that searches staggered layouts, solves radii with
   linear programming, and refines circle centers.
3. `indexing_reminder` repeatedly guards against the common
   `row_idx * num_rows` indexing error.
4. `probe_solution` validates the staged geometry before the only formal
   evaluator call in the winning proposal.

Proposal `3bc2d83ddd4a419989d932a886a7f359` calls
`hexagonal_construction` once, obtains a valid probe score of
`0.949525222`, applies one full rewrite, and receives the same frozen
evaluator score. The skill is present before the first edit, and the indexing
middleware fires on all five model turns.

Across all 48 evolved proposals:

- skill delivery before first edit: 48/48;
- `hexagonal_construction`: 50 attempts, 50 completions, 0 errors;
- `indexing_reminder`: 246 fires;
- `complete_tool_reminder`: 0 fires;
- probes: 50; formal evaluator calls: 48.

The matched initial arm has 48 proposals, 186 LLM calls, 44 evaluator calls,
and no generated skill, custom tool, generated middleware, or probe use.

## Interpretation boundary

This is deliberately labeled **tool-mediated transfer**. The generated tool
stages the complete solver and includes a known validity-safe 2.502-family
anchor, so this case should not be presented as Qwen independently deriving
the geometry. It demonstrates that an executable, inspectable harness artifact
learned elsewhere transfers to a larger frozen model and is correctly invoked,
validated, and incorporated.

`complete_tool_reminder` did not fire and is not credited as an active
contributor. Numeric attribution among the other components requires an
ablation.

## Files

- `results/`: immutable cell-level result JSON for both arms.
- `programs/`: exact initial- and evolved-arm best programs.
- `evidence/winning_audit.json`: compact structured audit.
- `evidence/winning_trajectory.json`: full model/tool trajectory.
- `evidence/component_frequency.json`: run-level component totals.
- `evolved_harness/`: exact runtime prompt, spec, skill, tool, middleware,
  component manifest, and compatibility-repair provenance.
