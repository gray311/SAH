---
name: discovery-optimization
description: "Spectral-aware search for Erdos C5. Start diverse, use FFT correlation insights, probe before full eval."
---

# Spectral-Aware Erdos C5 Search

## Phase 1: Diverse Initialization

1. Generate 5-10 diverse initial step functions:
   - Uniform: h(x) ≈ 0.5 everywhere
   - Bimodal: Two peaks (e.g., h=0.8 on [0,0.5] and [1.5,2], h=0.2 elsewhere)
   - Trimodal: Three peaks at 0.33, 1.0, 1.67
   - Golomb-like: Peaks at 0.0, 0.4, 0.8, 1.2, 1.6
   - Step function: Threshold at x=0.5 (h=1.0 for x<0.5, h=0.0 otherwise, adjusted for integral)

2. For each initialization:
   - Apply sigmoid to latent to ensure [0,1] range
   - Apply L2 projection: h = h / integral(h) * 1.0 to enforce integral=1
   - Keep top 3 by probe score

## Phase 2: Spectral-Aware Mutations

The objective: max_k integral h(x)(1-h(x+k))dx = max_k correlation[k] * dx

FFT insight: correlation[k] comes from the k-th frequency component.

Mutation templates:

### Template A: Peak Shifting
- Identify a peak at position p
- Shift it by delta (±0.1 to ±0.3)
- Re-normalize for integral
- Expected effect: Changes correlation at shifts related to delta

### Template B: Peak Splitting
- Take a broad peak and split into two narrower peaks
- Example: [0.2, 0.8] → two peaks at 0.3 and 0.5 with lower height
- Expected effect: Reduces correlation at certain lags

### Template C: Peak Merging
- Merge two nearby peaks into one broader peak
- Example: peaks at 0.2 and 0.4 → one peak at 0.3
- Expected effect: Smooths the function, may reduce high-frequency correlations

### Template D: Plateau Adjustment
- Raise/lower a plateau region
- Example: h=0.6 on [0.2, 0.6] → h=0.7 on [0.2, 0.6]
- Adjust other regions to maintain integral=1
- Expected effect: Changes correlation at all shifts (global change)

### Template E: Localized Perturbation
- Add small noise (±0.05 to ±0.15) in region of high overlap
- Find k where correlation[k] is large, find x where h(x)(1-h(x+k)) is large
- Perturb h(x) in that region
- Re-normalize for integral

## Phase 3: Probe-Driven Search

1. After each mutation, call probe_solution immediately
2. Keep mutations with c5_bound < 0.382 (probe threshold)
3. Evaluate only the best 1-2 probe candidates
4. If no improvement in 10 iterations, reset to a new diverse initialization

## Phase 4: Iterative Refinement

1. Start with larger edits (±0.1 to ±0.2)
2. As search progresses, use smaller edits (±0.02 to ±0.08)
3. Always maintain integral=1 and h in [0,1]
4. Track best solution across all iterations

## Key Rules
- DIVERSITY FIRST: Always try diverse initializations
- SPECTRAL AWARENESS: Think about how mutations affect FFT correlation
- PROBE BEFORE EVAL: Never spend full eval budget on unproven candidates
- INTEGRAL CONSTRAINT: Always re-normalize after edits
- ITERATIVE: Start coarse, refine fine
