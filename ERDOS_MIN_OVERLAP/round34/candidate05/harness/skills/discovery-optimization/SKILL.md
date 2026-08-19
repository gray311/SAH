---
name: discovery-optimization
description: "Generate 5-7 diverse step-function initializations from parameterized families (bipartite, multi-peak, Golomb, anti-periodic, piecewise), screen with probe, mutate top candidates structurally, evaluate only best."
---

# Diverse Initialization Strategy for Erdos C5

## Why Seed Failed
The seed uses 15+ random patterns but they rarely satisfy integral(h)=1. Random sigmoid latent doesn't naturally integrate to 1. Result: optimizer searches in invalid region.

## Phase 1: Generate Diverse INITIALizations (NOT random!)
Generate these 5-7 explicit families:

### 1. Bipartite (Single threshold)
h = 1 on [0, a], h = 0 on (a, 2]
- Constraint: 1*a = 1 => a = 1.0
- h = [1.0]*800 for first half, [0.0]*800 for second half (approximate)

### 2. Dual-peak (Two narrow Gaussians)
h = sigmoid( (x - c1) / w1 ) + sigmoid( (x - c2) / w2 )
- Choose c1=0.2, c2=1.8, w1=0.08, w2=0.08
- Scale so integral=1 (multiply by normalization factor)

### 3. Four-peak Golomb-like
centers = [0.25, 0.75, 1.25, 1.75], width=0.06
- h = sum of 4 narrow sigmoids, scale for integral=1

### 4. Anti-periodic (high in 3 bands)
h = 1 on [0.1,0.3] U [0.8,1.0] U [1.5,1.7]
- Total width = 0.6, need integral=1, so h=1.667 in these bands? No, cap at 1.
- Alternative: h=0.5 on [0,0.4] U [1.6,2], h=1 on [0.4,1.6] (integral=0.8+1.2=2.0, scale by 0.5)

### 5. Piecewise-constant
divide [0,2] into 3 parts: [0,0.2], [0.2,1.8], [1.8,2]
h = [1.0, 0.5, 0.0] => integral = 0.2 + 1.8*0.5 + 0 = 1.1, scale by 0.909

### 6. High-low-high
divide into 3: [0,0.25], [0.25,1.75], [1.75,2]
h = [1.0, 0.0, 1.0] => integral = 0.5, need to scale up
- Alternative: h=1 on [0,0.2] and [1.8,2], h=0.5 on [0.2,1.8]
- Integral = 0.2 + 1.6*0.5 + 0.2 = 1.2, scale by 0.833

### 7. Tri-modal with gaps
centers = [0.35, 0.95, 1.65], width=0.07
- Sum of 3 narrow sigmoids, scale for integral=1

## Phase 2: Screen with probe
For each of 5-7 initializations:
1. Call probe_solution to get approximate c5_bound
2. Keep only those with c5_bound < 0.381
3. Discard others (they're worse than seed)

## Phase 3: Mutate top candidates
For each kept candidate (rank by c5_bound, lowest first):
- Try mutation: narrow high regions by 15-20% (reduce sigma by that factor)
- Try mutation: shift centers by ±0.12 to break symmetry
- Try mutation: add small bump in low region (width 0.05, height 0.2-0.3, re-normalize)

## Phase 4: Re-probe and evaluate
1. Re-call probe_solution on all mutated variants
2. Pick top 1-2 by c5_bound
3. Call evaluate_solution on those
4. If any combined_score > 1.0, call finish

## Key Rules
- DIVERSITY > Randomness. Use explicit, parameterized families.
- ENFORCE integral=1 during generation (the optimizer can't fix invalid h).
- PROBE BEFORE EVALUATE. Don't waste eval budget.
- MUTATE STRUCTURALLY. Don't just tune hyperparameters.
- STOP EARLY if combined_score > 1.0.
