---
name: analytical-screening
description: Use analyze_pattern_to_mutate for targeted mutations and probe_solution for screening.
---

# Pattern-Based Search for Erdos C5

## Strategy: Structural Mutations Over Hyperparameter Tuning

The key insight: The best improvements come from mutating PATTERN STRUCTURES,
not just changing learning rates or step counts.

## Workflow

1. ANALYZE FIRST: Call analyze_pattern_to_mutate() to get a targeted mutation suggestion.
   It tells you exactly which pattern structure to perturb and why.

2. EDIT SPECIFICALLY: Edit the EVOLVE-BLOCK to implement the suggested mutation:
   - Golomb: perturb marks by +/-0.05 to +/-0.15
   - Tri-modal: shift peak locations or adjust widths
   - Bipartite: change the threshold from 0.5

3. SCREEN WITH PROBE: Call probe_solution to quickly check c5_bound (~10s).
   - c5_bound >= 0.375? STOP, this mutation did not help.
   - c5_bound < 0.375? CONTINUE to full evaluation.

4. EVALUATE PROMISING CANDIDATES: Only call evaluate_solution when probe shows promise.
   Budget is limited - use probe to filter bad candidates.

5. ITERATE: After evaluation, analyze the improved h and make smaller refinements.

## Success Stories

Small perturbations to Golomb marks (e.g., [0.0, 0.38, 0.75, 1.15, 1.58]) can reduce overlap
by breaking exact periodicity that creates high correlation peaks.

Goal: Find c5_bound < 0.38092303510845016 (combined_score > 1.0).
