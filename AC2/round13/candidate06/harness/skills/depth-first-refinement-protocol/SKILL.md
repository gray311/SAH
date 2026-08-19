---
name: depth-first-refinement-protocol
description: Depth-first refinement within step-function class. Explore 20+ iterations per pattern before switching, using probes to filter variants and small systematic mutations.
---

# Depth-First Step-Function Refinement Protocol

## Core Principle

The step-function record (0.8962799441554086) is a LOCAL optimum in FUNCTION ARCHITECTURE SPACE.
Smooth functions are LIKELY suboptimal. Focus DEPTH-FIRST refinement within step functions.

## Rule 1: Depth Over Breadth

- Spend 20+ iterations refining ONE pattern before switching
- Don't try 5 different patterns in 10 iterations
- Incremental improvements compound: 5 variants x 0.0001 = 0.0005 improvement possible

## Rule 2: Small Systematic Mutations

- Heights: perturb by ±0.02 to ±0.08 (NOT ±0.15 or more)
- Widths: adjust interval boundaries by ±2% to ±5%
- Asymmetry: perturb symmetric patterns by 0.01-0.03
- Large mutations break the current optimum; small ones climb the hill

## Rule 3: Probe-Filter-Evaluate Loop

1. Generate 5-8 variants with small mutations
2. PROBE ALL variants (use your 30-probe budget!)
3. EVALUATE only top 2-3 by probe score
4. If all probes < current best: regenerate with different mutation types

## Rule 4: Mutation Pipeline Order

When refining a pattern, follow this order:
1. Height perturbation (±0.03-0.08 on peaks, ±0.02 on others)
2. Width adjustment (±3-5% on interval boundaries)
3. Level addition/removal (for 4+ level patterns)
4. Symmetry breaking (make symmetric pattern asymmetric)
5. Center shift (move entire pattern by 1-2% of domain)

Try mutation type 1 for 5 iterations. If no improvement, try type 2 for 5 iterations, etc.

## Rule 5: Pattern Switching (Last Resort)

Only after 8+ iterations without improvement on current pattern:
- Switch to a DIFFERENT seed pattern (1-3 at most before 20 iterations)
- Prefer patterns with different characteristics (more levels, different positions)
- Don't spend 15+ iterations on patterns that aren't promising

## Rule 6: Documentation for Success

Track per pattern:
- Iteration when improvement occurred
- Which mutation type helped (height/width/asymmetric)
- Best score achieved
- Total iterations spent

## What to AVOID

- SMOOTH functions (Gaussian, spline, oscillatory) - they spread energy
- Radical mutations (±0.15+, 10%+ width changes) - break the optimum
- Trying many patterns quickly - don't explore broadly
- Using evaluate_solution for variants you haven't probed

## Success Pattern

Expected trajectory: Pattern A (3 iterations) -> Pattern B (8 iterations) -> Pattern C (15 iterations)
-> Final: A single well-refined step pattern beats the record.
