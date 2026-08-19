---
name: discovery-optimization
description: "Generate diverse step function templates with varied discretization and structure (bipartite, multimodal, Golomb-like, sinusoidal), probe them cheaply, then evaluate the best."
---

# Diverse Template Generation Strategy for Erdos C5

## Phase 1: Generate 5-7 Diverse Initial Hypotheses

Use generate_step_function_template with DIFFERENT template types:

- "bipartite": Single threshold h(x) = 1 if x < 0.5 else 0.
- "multimodal_3peaks": Three narrow peaks at x=0.5, 1.0, 1.5 with widths ~0.15.
- "multimodal_5peaks": Five narrow peaks at x=0.3, 0.7, 1.0, 1.3, 1.7 with widths ~0.12.
- "golomb_ruler": Sparse peaks at [0.0, 0.4, 0.8, 1.2, 1.6] to minimize overlaps.
- "sinusoidal_threshold": Smooth transition using sigmoid(sin) to create wave-like structure.
- "piecewise_constant": Simple step function with varying intervals.

VARY num_intervals: try 400, 800, 1600, 3200. Optimal discretization might differ from seed's 800.

## Phase 2: Probe and Evaluate

1. Call probe_solution on EACH hypothesis to get approximate c5_bound.
2. Keep only those with c5_bound < 0.385.
3. Call evaluate_solution on the best 3 hypotheses (lowest c5_bound).
4. If any has combined_score > 1.0, finish.

## Phase 3: Targeted Mutations (if needed)

If no hypothesis beats the seed:
- Take the BEST single hypothesis (lowest c5_bound from Phase 2).
- Use structure_inspired_mutations with target_shifts from correlation_analyzer.
- Create 3-5 mutants per mutation type. Probe them, evaluate the best 1-2.

## Key Rules
- ALWAYS explore structural diversity FIRST (different templates, different num_intervals).
- Use probe_solution to screen many hypotheses cheaply.
- Only do hyperparameter tuning AFTER exhausting diverse structural hypotheses.
