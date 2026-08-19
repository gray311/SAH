---
name: combinatorial-step-search
description: Search for optimal step functions by directly constructing piecewise-constant functions with controlled breakpoints and levels. Avoid gradient-based smooth curve optimization.
---

# Combinatorial Step Function Search

## Core Principle
Optimal Erdős step functions are piecewise-constant, NOT smooth sigmoid curves.
The seed optimizer's gradient descent on sigmoid-transformed vectors finds local minima
that are good but not optimal for this problem.

## Search Strategy

### Step 1: Choose Structural Parameters
- Number of steps: 4, 6, 8, 10, 12, 16
- Breakpoint spacing: uniform, golden-ratio, Fibonacci, rational grids
- Level assignments: binary (0,1), ternary (0,0.5,1), quaternary (0,0.25,0.75,1)

### Step 2: Generate Candidate
1. Define breakpoints [b_0, b_1, ..., b_N] where 0 = b_0 < b_1 < ... < b_N = 2
2. Assign levels l_0, l_1, ..., l_{N-1} in [0, 1]
3. Scale: multiply all levels by c = 1 / (sum(l_i) * (b_{i+1}-b_i))
4. This guarantees integral(h) = 1

### Step 3: Analytical Screening
Call generate_step_candidates for precomputed c5_bound
Filter: c5_bound < 0.36 (conservative) or < 0.37 (generous)

### Step 4: Full Evaluation
Call evaluate_solution ONLY on candidates passing the filter
Typical budget: 2-4 evals per batch

### Step 5: Iterate
If no improvement:
- Try different N values
- Try different breakpoint grids (rational with denom 3,4,6,8,12)
- Try different level assignments

## Why This Works
- Direct combinatorial search explores a fundamentally different space
- Precomputed analytical scores enable rapid screening
- Piecewise-constant representation matches the problem structure
