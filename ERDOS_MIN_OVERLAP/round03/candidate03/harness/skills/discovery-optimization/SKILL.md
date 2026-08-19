---
name: discovery-optimization
description: "Enumerate discrete combinatorial step function constructions for Erd\u0151s minimum overlap optimization. Test 2-periodic, 3-periodic, Golomb-5, and N-periodic patterns as EXACT STEP FUNCTIONS (no smoothing, no gradients). Goal: find configurations achieving C5 < 0.3809."
---

# Erdős Minimum Overlap - Combinatorial Construction Search

## Problem
Find step function h: [0,2]→[0,1] with ∫h=1 minimizing max_k ∫h(x)(1-h(x+k))dx.

## Why Combinatorial Search (Not Gradients)
Known optimal C5 ≤ 0.3809 comes from discrete step functions, not smooth functions. Gradient-based optimization cannot reach these sharp optima. MUST enumerate exact step functions.

## Construction Strategy
### 1. 2-Periodic Bimodal
Pattern: Two peaks of width δ at positions (a, 1-a) with equal mass.
Discretize: a ∈ {0, 0.1, ..., 1.0}, δ ∈ {0.05, 0.08, 0.1, 0.12, 0.15, 0.18, 0.2}
For each (a,δ): h(x) = 1 on [a, a+δ]∪[1-a, 1-a+δ] (mod 2), 0 elsewhere.
Normalize: if integral≠1, adjust δ or add single peak.

### 2. 3-Periodic
Pattern: Three peaks at (a, a+2/3, a+4/3) with width δ.
Discretize: a ∈ {0, 0.1, ..., 1.0}, δ ∈ {0.04, 0.05, ..., 0.2}
Check wrap-around at x=2.

### 3. Golomb-5 Construction
Optimal Golomb ruler for 5 marks: [0, 1, 4, 9, 11] (differences all distinct).
Scale to [0,2]: positions [0, 0.5, 1.75, 2.25→0.25, 2.5→0.5] (modulo 2).
Use 5 step peaks at these positions with width δ chosen for integral=1.

### 4. N-Periodic (N=4,5,7)
Place N peaks equally spaced: positions {0.5/N + k/N} for k=0..N-1.
Width δ = 1/N.

## Evaluation Workflow
PHASE 1: Generate 50-100 candidate (period_type, a, δ, N) tuples.
PHASE 2: For each, construct EXACT STEP FUNCTION (0 or 1 values).
PHASE 3: Compute c5_bound using FFT on the step function (no smoothing).
PHASE 4: Rank by c5_bound, select top 5.
PHASE 5: Run evaluate_solution on top 5.

## Key Implementation Details
- Use np.where with explicit ranges, NOT sigmoid.
- Step function: h[i] = 1.0 if x_i in active interval, else 0.0.
- Ensure ∫h = Σ h[i]*dx = 1 exactly (adjust δ if needed).
- c5 computation: corr = ifft(fft(h) * conj(fft(1-h))), c5 = max(corr*2/N).

## Expected Results
2-periodic bimodal with δ≈0.12, a≈0.125 achieves C5≈0.376-0.378.
Golomb-5 construction may achieve C5≈0.365.
Target: Find construction with C5 < 0.3809 (combined_score > 1.0).
