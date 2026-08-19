---
name: mutate-then-evaluate
description: Generate patterns, mutate the best one to create refined variants, screen with probe, evaluate the best. Do not skip mutation phase.
---

# Mutate-Then-Evaluate for Erdos C5

## Core Principle
The seed optimizer gets stuck. We need to MUTATE the best pattern to escape local optima.

## Step-by-Step Workflow

1. CALL search_patterns(temperature=0.5)
   - Generates 5 diverse initial patterns
   - Each has precomputed c5_bound via FFT

2. IDENTIFY the best pattern (lowest c5_bound)
   - Compare all 5 candidates
   - Select the one with minimum c5_bound

3. CALL mutate_best_pattern on the best pattern
   - Creates 3 refined variants
   - Each variant has precomputed c5_bound via FFT
   - Mutations: width adjustment, center shift, amplitude change

4. SCREEN all 3 mutated variants with probe_solution
   - Probe is cheap (separate budget)
   - Keep variants with c5_bound < 0.375

5. CALL evaluate_solution on the BEST 1-2 mutated variants
   - Only evaluate if c5_bound < 0.375 (combined_score > 1.01)
   - Full optimization takes ~59000 steps

6. If no improvement, REPEAT with search_patterns(temperature=0.8)

7. Only after exhausting pattern-based search, tune hyperparameters

## Avoid Common Mistakes
- Do NOT skip the mutation phase
- Do NOT call evaluate_solution on c5_bound > 0.375
- Do NOT tune hyperparameters before trying mutations
- ALWAYS use probe_solution before full evaluation
