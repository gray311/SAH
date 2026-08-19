---
name: ratio-structure-refinement
description: Step-function refinement using ratio-aware mutations. Analyze interval/height ratios with analyze_ratio_structure, then mutate based on theoretical optimality conditions.
---

# Ratio-Aware Refinement Protocol for Step Functions
## Core Principle
Step function performance depends on ratio properties: interval width ratios and height-to-width ratios. Theoretical analysis suggests narrow tall peaks and smooth valleys optimize the convolution. Analyze ratios FIRST, then mutate.
## Phase 1: Ratio-Guided Mutations (iterations 1-12)
1. Call analyze_ratio_structure to get interval_widths, heights, and ratio_features
2. Generate 3 ratio-guided mutations:
Mutation A (Narrow Tall Peaks): - Find interval with width < 0.12 and height > 1.3 - Narrow by 10%: new_end = old_start + 0.9*(old_end - old_start) - Increase height by 0.1
Mutation B (Widen Valleys): - Find valley interval (height < 1.0) - Widen by 15%: new_end = old_end + 0.15*(domain_width) - Decrease height by 0.1
Mutation C (Add Peak in Valley): - Find widest valley (height < 1.0, width > 0.12) - Add new peak at center with height = valley_height + 0.5
3. Probe all 3, evaluate best
4. If no improvement after 3 iterations: switch to Phase 2
## Phase 2: JAX Gradient Optimization (iterations 13-22)
1. Use @jax.grad on -c2_ratio to get gradients
2. Take step: new_param = param + 0.05 * gradient
3. Clip to valid range
4. Probe 2 variants (ascent and descent), evaluate best
5. If gradient norm < 0.001: switch to Phase 3
## Phase 3: Architecture Search (iterations 23-30)
1. Keep best c2, try architectural changes: - Split one tall peak into two with height = 0.7*original - Merge two adjacent valleys - Try asymmetric three-peak: heights 1.2, 1.8, 1.0
2. Probe both variants, evaluate best
3. Submit if c2 > 0.8962799441554086
## Key Rule
ALWAYS call analyze_ratio_structure BEFORE mutation. The tool understands the actual structure, not just estimated parameters.
