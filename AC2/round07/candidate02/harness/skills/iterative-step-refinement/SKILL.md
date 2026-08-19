---
name: iterative-step-refinement
description: Playbook for iterative step function refinement using analyze_step_config to guide systematic improvements.
---

# Iterative Step Function Refinement Playbook

## Core Principle

Don't randomly search. Use analyze_step_config to understand the current best, then make **targeted, systematic improvements**.

## The Refinement Loop

1. **ANALYZE**: Call analyze_step_config
   - Extract: peak_height, plateau_width, outer_wings
   - Note: improvement_suggestions list

2. **PICK ONE SUGGESTION**: Choose from suggestions
   - "INCREASE_PEAK_HEIGHT": Edit to raise plateau height
   - "WIDEN_PLATEAU": Extend plateau boundaries
   - "NARROW_PLATEAU": Shrink central region
   - "ADD_WINGS": Add outer asymmetric steps
   - "TRY_ASYM_2PEAK": Switch to 2-peak configuration

3. **EDIT**: Use edit_solution with the chosen modification
   - Make ONLY the suggested change (minimal perturbation)
   - Don't redesign the whole function

4. **PROBE**: Call probe_solution on the modified function
   - Check if the single change helped

5. **REPEAT**: If improved, call analyze_step_config again
   - Apply next suggestion or refine current change further
   - Continue 2-3 cycles before full evaluation

6. **EVALUATE**: After 2-3 refinement cycles, evaluate the best variant
   - Then call analyze_step_config on the NEW best to continue

## Example Session

- Iteration 1: analyze → "INCREASE_PEAK_HEIGHT: from 1.4 to 1.7" → edit → probe (+0.001)
- Iteration 2: analyze → "WIDEN_PLATEAU: extend width by 0.1" → edit → probe (+0.002)
- Iteration 3: analyze → "NARROW_PLATEAU: shrink to width 0.5, height 1.8" → edit → probe (+0.003)
- Iteration 4: analyze → "ADD_EXTREME_WINGS: add outer steps" → edit → probe (+0.001)
- Iteration 5: evaluate top variant
- Iteration 6: analyze NEW best → continue refinement from new baseline

## Why This Works

- **Focused search**: Each edit makes one targeted improvement
- **Low risk**: Small changes don't destroy good structure
- **Progressive**: Builds up improvements incrementally
- **Guided by analysis**: Know what to try next
