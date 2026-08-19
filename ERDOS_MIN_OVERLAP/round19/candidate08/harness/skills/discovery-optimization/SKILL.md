---
name: discovery-optimization
description: "Generate diverse step-function candidates for Erdos optimization.\n\nDirect combinatorial search over breakpoints and levels, not gradient descent.\nPrecompute analytical c5 scores, scale to integral=1, filter c5 < 0.36 for full eval."
---

# Step Function Search Strategy

## Problem
The seed optimizer trains smooth sigmoid curves. Optimal Erdős step functions are piecewise-constant.

## Solution: Direct Combinatorial Construction

### Step 1: Define Step Function Structure
A step function with N intervals has:
- N breakpoints in (0, 2)
- N levels in [0, 1]
- Scale: multiply all levels by constant to make integral = 1

### Step 2: Generate Diverse Configurations
Vary:
- N (4, 6, 8, 10, 12, 16)
- Breakpoint grid (uniform, Fibonacci, golden-ratio spacing)
- Level patterns (binary: 0/1; ternary: 0/0.5/1; patterned)

### Step 3: Precompute Scores
Use generate_step_candidates tool to get analytical c5_bound

### Step 4: Evaluate Best
Only run full optimization on candidates with c5_bound < 0.36

## Expected Behavior
1. CALL generate_step_candidates with 2-3 different N values
2. Filter for c5_bound < 0.36 (expect 2-4 candidates)
3. CALL evaluate_solution on each kept candidate
4. Iterate with new N, new breakpoint grids if no improvement
5. Total: 2-4 evals per batch, 2-3 batches max
