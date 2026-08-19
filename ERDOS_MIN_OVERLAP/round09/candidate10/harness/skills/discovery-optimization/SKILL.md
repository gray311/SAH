---
name: discovery-optimization
description: "Erdos minimum overlap optimization using systematic multi-restart search around principled constructions.\nThe key is running multiple perturbed restarts per construction and using probe-based ranking."
---

# Multi-Restart Search Strategy for Erdos Problem

## Why Multi-Restart Works
The landscape has deep local optima. The seed program runs ONE optimization per initialization,
but you need 3-5 restarts PER construction with varied perturbations.

## Method

### Step 1: Generate Constructions
Call analyze_constructions() to get 7 diverse initializations.

### Step 2: For Each Construction
For each construction returned:
1. Create perturbations (3-5 total) with Gaussian noise (std=0.1, 0.3, 0.5)
2. For each perturbation, run optimizer with varied hyperparams:
   - Restart A: lr=0.01, penalty=1500, steps=20000
   - Restart B: lr=0.005, penalty=1000, steps=30000
   - Restart C: lr=0.001, penalty=3000, steps=40000
3. Use probe_solution to get c5_bound (cheap, separate budget)
4. Track the variant with best probe score

### Step 3: Final Evaluation
- Evaluate only the top 1-2 candidates
- Stop if combined_score > 1.0 (c5_bound < 0.380923)

## Critical Tips
- Save best program between restarts (use ctx.scratch_write)
- Use constraint penalty: (integral(h) - 1)^2 * 1000-2000
- jit all computation for speed
- Probe budget (~30) is unlimited; eval budget (30) is precious
