---
name: discovery-optimization
description: "Systematic step-function perturbation. Mutate heights, widths, and asymmetries of existing patterns with probe-guided ranking."
---

# Systematic Step-Function Perturbation Protocol

## Core Principle
The 12 step patterns in the seed cover diverse architectures. Instead of inventing new families, systematically PERTURB these proven patterns.

## Perturbation Menu (choose 1-2 per variant)

1. HEIGHT ADJUSTMENT
   - High peak patterns (1.50, 1.60, 1.90, 2.30, 2.80, 2.50): try ±0.10 to ±0.25
   - Medium peaks (1.40, 1.20, 1.00, 0.90): try ±0.05 to ±0.15
   - Rationale: Optimal peak heights balance L2 norm vs sup norm

2. WIDTH ADJUSTMENT
   - Narrow peaks (<0.25 width): widen by +10% to +20%
   - Wide peaks (>0.50 width): narrow by -10% to -15%
   - Rationale: Optimal support width for convolution energy concentration

3. ASYMMETRY MODULATION
   - Symmetric patterns: add slight asymmetry (shift left/right bounds by ±8%)
   - Asymmetric patterns: try reverse asymmetry or increase by ±10%
   - Rationale: Asymmetry may improve L2/sup ratio

4. LEVEL SPLIT/MERGE
   - 2-level patterns: try splitting into 3 with intermediate height
   - 4-5 level patterns: try merging adjacent levels
   - Rationale: Optimal number of levels for this inequality

5. POSITION SHIFT
   - Centered patterns: shift all levels ±10% from center
   - Offset patterns: shift toward center or further out
   - Rationale: Optimal support location in domain

## Execution Flow

Iteration 1-5 (Exploration):
- Read current best: which pattern? what heights? where are bounds?
- Generate 4 variants: one from each of 4 different perturbation types
- Probe all 4 (4 probes)
- Evaluate top 2 (2 evals)
- Keep best, abandon rest

Iteration 6-15 (Refinement):
- Focus on best perturbation type from Phase 1
- Generate 3 variants with SMALLER perturbations (±5% instead of ±10%)
- Probe all 3 (3 probes)
- Evaluate top 1 (1 eval)
- Switch to different perturbation type if no improvement

Iteration 16-30 (Final Push):
- Try extreme perturbations: ±25% height, ±20% width
- Or combine 2 perturbation types (e.g., height + asymmetry)
- Probe all, evaluate top 1-2

## Key Rules
- NEVER change more than 2 parameters per variant
- Probe ALL variants before any full evaluation
- If probe score <1.0: skip full eval, try different perturbation
- After 3 iterations with same perturbation type: switch type
- Always document: "Pattern X, perturbation: height +0.15, width -10%" in scratch
