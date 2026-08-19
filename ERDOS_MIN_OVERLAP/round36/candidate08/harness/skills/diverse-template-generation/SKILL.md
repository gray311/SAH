---
name: diverse-template-generation
description: Generate diverse initial hypotheses with varied structure and discretization. Probe them cheaply before full evaluation.
---

# Diverse Template Generation for Erdos C5

## Strategy: Explore Structural Diversity FIRST

The seed uses num_intervals=800 with 14 patterns. Instead:
1. Generate 5-7 structurally DIFFERENT hypotheses using generate_step_function_template
   - Vary template_type: bipartite, multimodal_3peaks, golomb_ruler, sinusoidal_threshold
   - Vary num_intervals: 400, 800, 1600, 3200 (discretization matters!)
2. Probe ALL hypotheses with probe_solution (cheap, ~10s each)
3. Evaluate only the best 3 (lowest c5_bound from probing)
4. If no improvement, try structure_inspired_mutations on the best hypothesis

## Why this works

The current harness modifies the seed's 14 patterns but all share num_intervals=800.
The optimal step function might need more intervals (3200) or a completely different structure (bipartite).
By exploring structural diversity FIRST, we avoid local optima in the seed's pattern space.

## Workflow

1. Call generate_step_function_template 5-7 times with diverse (template_type, num_intervals) pairs.
2. Call probe_solution on each candidate.
3. Call evaluate_solution on the best 3 candidates (c5_bound < 0.385).
4. If combined_score > 1.0, finish.
5. If stuck, try mutations on the best hypothesis.

## Key Rules

- ALWAYS explore structural diversity (different templates, different num_intervals) BEFORE hyperparameter tuning.
- Use probe_solution to screen many hypotheses cheaply (budget: 30 probes).
- NEVER evaluate more than 2 hypotheses without probing first.
- VARY num_intervals (400, 800, 1600, 3200) as part of template diversity.
