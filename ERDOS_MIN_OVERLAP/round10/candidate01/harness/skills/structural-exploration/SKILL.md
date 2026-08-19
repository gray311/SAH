---
name: structural-exploration
description: Systematically explore different mathematical constructions for the Erdos problem. Focus on diversity - bimodal, triangular, periodic, Golomb-ruled patterns.
---

# Structural Exploration Strategy

## Why Diversity Matters
The seed optimizer's 12 initialization patterns are all variations of sigmoid(latent).
We need fundamentally different shapes: sharp bimodal peaks, multi-level triangular patterns,
Golomb-ruled spacing.

## Step-by-Step Strategy

1. START: Call `structural_analysis` to baseline current best
2. CONSTRUCT: For each of 4 construction types:
   - `construct_structured_init` generates 4-8 variants
   - Probe each variant (~10s each)
   - Keep those with integral(h) close to 1
   - Full evaluate top 2-3 per construction type
3. ANALYZE: If no improvement after one round, call `structural_analysis` again
   - Use returned suggestions to modify construction parameters
   - Try narrower peaks, shifted positions, asymmetric patterns
4. REFINE: If close to target (combined_score 0.95-1.0):
   - Use smaller step sizes in constructions
   - Try Golomb-ruled patterns with more marks (6-7)
   - Experiment with different kernel widths

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.38092303510845016)
- Prefer solutions with multiple peaks over simple bimodal
- Document which construction type and parameters worked best
