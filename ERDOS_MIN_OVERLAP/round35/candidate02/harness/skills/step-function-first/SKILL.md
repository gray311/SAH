---
name: step-function-first
description: Generate pure step functions (binary arrays) with exact integral constraint before attempting sigmoid optimization.
---

# Step-Function-First Strategy for Erdos C5

## Why this works:
The seed program uses sigmoid(latent) which creates smooth transitions. 
Step functions have sharp, predictable correlation peaks that are easier to manipulate.

## Step-by-step:
1. CALL search_step_functions ONCE at the start
   - Generate 5-10 diverse binary candidates with integral = 1
   - Use strategy="uniform_k_widths" for balanced candidates
2. CALL probe_solution on each candidate
   - Quickly filter to find those with c5_bound < 0.385
3. SELECT the best 1-2 candidates from probe results
4. CALL evaluate_solution on the best candidates
   - Full evaluation only on promising step functions
5. IF combined_score > 1.0, finish immediately
6. ONLY if all step functions fail, consider sigmoid approaches

## Key rules:
- STEP FUNCTIONS FIRST: Binary arrays are easier to reason about
- EXACT INTEGRAL: search_step_functions guarantees integral(h) = 1
- PROBE THEN EVAL: Use cheap probe to filter before expensive full eval
- FINISH EARLY: Don't waste evaluations on sigmoid if step functions work
