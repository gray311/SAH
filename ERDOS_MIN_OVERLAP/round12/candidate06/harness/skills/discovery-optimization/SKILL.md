---
name: discovery-optimization
description: "Resolution-first optimization with strict probe-based constraint filtering. Prioritize higher num_intervals (1600-6400) and use probe to screen invalid programs before full evaluation. Only evaluate variants with |integral(h)-1|<0.05."
---

# Erdos Minimum Overlap - Resolution-First Protocol

## Problem Understanding
We need to find a step function h: [0,2] to [0,1] with integral(h)=1 that minimizes C5 = max_k integral h(x)(1-h(x+k)) dx.
Current seed uses num_intervals=800 and achieves C5 approx 0.380923.
To beat this, explore higher resolutions, better optimizer settings, and more diverse initializations.

## Why Probe-Based Constraint Filtering is Critical
The seed optimizer may produce h where integral(h) does not equal 1. Evaluating such programs is WASTEFUL.
probe_solution returns approximate integral(h) and c5_bound - use it to FILTER and RANK.

## Step-by-Step Search Protocol

### Phase 1: Baseline (1 eval)
Evaluate the unmodified seed program. Record baseline_score approx 0.999855.

### Phase 2: Resolution Sweep (Primary - 15 evals)
For each resolution in 1600, 3200, 4000, 6400:
1. EDIT: num_intervals = resolution
2. PROBE: Get integral(h) and c5_approx
3. FILTER: If |integral - 1| >= 0.05, DISCARD
4. If multiple resolutions pass filter, CALL evaluate_solution on top 1-2
6. If no improvement, move to Phase 3

### Phase 3: Learning Rate Fine-tuning (6 evals)
For the best resolution: try LR values 0.001, 0.003, 0.007, 0.01
- EDIT base_learning_rate, PROBE for constraint
- Evaluate only if valid

### Phase 4: Penalty Strength Tuning (3 evals)
Try: 30, 100, 200, 500
- Use probe to filter

### Phase 5: If Stuck, Expand Initialization (5 evals)
Add ONE new pattern to _get_best_initialization():
- Four-peak Gaussian: centers at 0.25, 0.5, 0.75, 1.0, width=0.12

## Key Success Factors
- ALWAYS probe before evaluating
- Focus on resolution as primary search dimension
- Keep only the BEST result

## Expected Budget Usage (30 evals total)
- 1: baseline evaluation
- 8-12: probe calls for filtering and ranking
- 5-10: full evaluations on promising variants
