---
name: pattern-first-search
description: Always use search_patterns to generate diverse initializations before hyperparameter tuning. Screen with probe_solution, evaluate top candidates.
---

# Pattern-First Search for Erdos C5

## Core Principle
The optimizer needs GOOD INITIAL CONFIGURATIONS, not just hyperparameter tuning.
Start with diverse, analytically-designed patterns, THEN tune if needed.

## Step-by-Step Workflow

1. CALL search_patterns(temperature=0.5)
   - Generates 5 diverse initial step functions
   - Each has precomputed c5_bound via FFT
   - All satisfy integral=1, h in [0,1]

2. SCREEN with probe_solution
   - Run probe on each candidate
   - Keep those with c5_bound < 0.375

3. EVALUATE top 2-3 candidates
   - Call evaluate_solution on best candidates
   - If combined_score > 1.0, finish with summary
   - If combined_score <= 1.0, continue

4. If no improvement, REPEAT with temperature=0.8
   - Generates different patterns
   - May find better initializations

5. Only AFTER exhausting patterns, tune hyperparameters
   - This is Phase 2 (last resort)

## Avoid Common Mistakes
- Do NOT call evaluate_solution on c5_bound > 0.375
- Do NOT tune hyperparameters before trying patterns
- Do NOT call search_patterns more than 2x (budget limited)
- ALWAYS use probe_solution before full evaluation
