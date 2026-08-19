---
name: discovery-optimization
description: "Generate true step functions (constant on intervals) with 2-10 steps, screen with probe_solution, evaluate top candidates. Focus on step function diversity (single step, double step, up-down patterns) with exact integral constraint."
---

# Step-Function Search for Erdos C5

## Core Principle
The optimal C5 minimizer is likely a TRUE STEP FUNCTION (constant on intervals), not a smooth sigmoid.
The seed program's gradient optimization gets stuck because it starts from smooth initializations.

## Step-by-Step Workflow

1. CALL discrete_step_search(num_steps=5)
   - Generates step functions with 5 intervals
   - Each has precomputed c5_bound via FFT
   - Patterns include: single step up, single step down, up-down, multiple steps

2. SCREEN with probe_solution
   - Run probe on each candidate
   - Keep those with c5_bound < 0.375

3. EVALUATE top 1-2 candidates
   - Call evaluate_solution on best candidates
   - If combined_score > 1.0, finish with summary
   - If combined_score <= 1.0, continue

4. If no improvement, REPEAT with different num_steps (2, 3, 7, 10)

5. Only AFTER exhausting step functions, use gradient optimization

## Avoid Common Mistakes
- Do NOT call evaluate_solution on c5_bound > 0.375
- Do NOT use gradient optimization before trying step functions
- Do NOT call discrete_step_search more than 2x (budget limited)
- ALWAYS use probe_solution before full evaluation
