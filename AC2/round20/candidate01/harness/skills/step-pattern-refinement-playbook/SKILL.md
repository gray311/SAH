---
name: step-pattern-refinement-playbook
description: Refine step patterns with small perturbations while preserving multi-level structure.
---

# Step-Pattern Refinement Playbook for C2 Maximization

## Core Principle
The current best (0.8963) is achieved by MULTI-LEVEL STEP FUNCTIONS. Do NOT 
change to smooth families (Gaussian, B-spline, etc.). Instead, PERTURB the 
existing step patterns with small, careful adjustments.

## Perturbation Guidelines

### Height Perturbations (CRITICAL)
- Change heights by +/- 0.1 to 0.3 (e.g., 1.60 -> 1.65 or 1.55)
- NEVER change by more than 20% of the original height
- Preserve the relative ordering of heights (don't invert the pattern)
- Example: [0.80, 1.60, 2.00, 1.40, 0.90] -> [0.85, 1.65, 1.95, 1.45, 0.90]

### Position Perturbations
- Shift segment boundaries by +/- 3% to 5% of total width
- Keep segments roughly the same size (don't collapse to single steps)
- Maintain the overall "balance" of the pattern

### Structure Preservation
- Keep the SAME number of levels (don't collapse to fewer steps)
- Preserve the multi-level character (don't create a simple step)
- Ensure all heights remain positive (> 0.1)

## Why Small Perturbations Work
The optimization space for step functions is CONTINUOUS. Small perturbations 
can fine-tune the L2/inf ratio without losing the structural advantages of 
multi-level steps. The seed's patterns are already sophisticated; we just need 
to find the optimal height/width configuration.

## Search Strategy
1. Analyze current pattern structure (call analyze_step_structure)
2. Generate 3-5 perturbed variants (call generate_step_variants)
3. Probe ALL variants (use your 30 probes wisely)
4. Evaluate top 2 by probe score
5. If no improvement after 5 iterations: try hybrid patterns

## Red Flags
- If you're generating Gaussians, splines, or oscillatory functions: STOP
- If you're changing heights by more than 20%: STOP
- If you're collapsing multi-level patterns to single steps: STOP
- Always stay in the step-function landscape
