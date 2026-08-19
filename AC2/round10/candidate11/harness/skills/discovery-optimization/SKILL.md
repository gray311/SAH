---
name: discovery-optimization
description: "Discover new step function STRUCTURES to beat 1.03492. Try: pyramid variants, bimodal/tri-modal patterns, asymmetric structures, smoothed transitions, multi-scale grids. Use probes to test 10+ structural variants before full evaluation."
---

# Second Autocorrelation Inequality - Structural Discovery Strategy

## Current State Analysis
Best score: 1.03492 using multi-level step functions with heights ~1.4-2.3

## Why Parameter Tweaking Fails
The seed patterns (pyramid, multi-level, asymmetric) are already optimized.
Small ±5-10% changes to heights/widths won't escape local optima.

## New Approach: STRUCTURAL DIVERSIFICATION

### Pattern Class 1: Extended Pyramids
- 5-level or 7-level pyramids with different slope ratios
- Example: heights [0.5, 1.0, 1.8, 2.2, 1.5, 0.8, 0.3] over [0.0, 0.14, 0.28, 0.43, 0.57, 0.71, 0.86]

### Pattern Class 2: Bimodal/Dual-Peak
- Two distinct peaks separated by valley
- Heights: [0.8, 0.6, 0.4, 2.2, 2.0, 2.3, 0.4, 0.6, 0.8]
- Peak separation: 0.3-0.4 of domain

### Pattern Class 3: Asymmetric Multi-peak
- Three peaks with unequal heights and spacings
- Pattern: low-higher-highest-lower-high (LHHLH)
- Heights: [0.6, 1.2, 2.0, 1.0, 0.7]

### Pattern Class 4: Smoothed Step Edges
- Keep step function shape but add transition zones
- Instead of f.at[start:end].set(h), use gradual ramps

### Pattern Class 5: Multi-Stage Hybrid
- Combine features from different seed patterns
- Take outer structure from pattern 6 + inner peak from pattern 11

### Pattern Class 6: Plateau Variants
- Flat top regions instead of peaks
- Heights: [0.5, 0.8, 1.0, 1.8, 1.8, 1.0, 0.8, 0.5]

## Execution Workflow

### Phase 1: Structural Exploration (Iterate 1-8)
1. Generate 3-5 completely different structural patterns
2. Use probe_solution to score each (test 3 variants per pattern class)
3. Track best structural class by probe score

### Phase 2: Coarse Refinement (Iterate 9-12)
1. Take top 2 structural classes
2. Test with num_intervals = 200, 250, 300 (coarse grid search)
3. Identify best interval count

### Phase 3: Fine-Tuning (Iterate 13-20)
1. Refine top 1 structure to 400-450 intervals
2. Test 4-5 structural variations (shifted boundaries, alternate heights)
3. Call evaluate_solution on top 2 candidates

### Phase 4: Evaluation & Iteration
1. If eval improves structural class, continue refining
2. If eval drops, try next structural class in priority order
3. Never exhaust budget on one failing structural direction

## Key Principles
- STRUCTURE > PARAMETERS: Focus on pattern class exploration
- BREADTH FIRST: Test many structural variants before deep optimization
- MULTI-SCALE: Start coarse, refine only top candidates
- AGGRESSIVE PERSISTENCE: Don't abandon structural directions after 1 failure

## When to Stop
- After evaluating 3+ structural classes
- If no improvement after 15 evals and 2+ classes exhausted
- When budget < 5 evals remaining, make final aggressive structural change
