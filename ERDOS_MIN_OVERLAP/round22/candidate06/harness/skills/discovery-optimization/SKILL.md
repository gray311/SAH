---
name: discovery-optimization
description: "Generate TRUE STEP FUNCTIONS (piecewise constant) for Erdos optimization. Use coarse discretization and hard thresholds, not smooth sigmoid curves."
---

# Step Function Strategy for Erdos Optimization

## Problem
The seed optimizer produces smooth sigmoid curves. The optimal solution is likely a TRUE STEP FUNCTION with few jumps.

## Solution

1. USE COARSE DISCRETIZATION: Set num_intervals=20, 30, or 40. This forces the solution to be a step function naturally.

2. GENERATE HARD INITIALIZATIONS: Don't use sigmoid. Directly set h values to 0, 0.5, or 1.0 based on threshold patterns.

3. SAMPLE STRUCTURAL PATTERNS:
   - Uniform step: h = constant (integral constraint determines value)
   - Binary step: h = 0 on [0, a), 1 on [a, 2]
   - Asymmetric step: different heights on different intervals
   - Symmetric step: h symmetric around x=1

4. VERIFY INTEGRAL: sum(h) * dx must equal 1.0 exactly for step functions.

5. EVALUATE STRUCTURAL VARIANTS: Test 3-5 different step patterns with different jump locations.

## Expected Outcome
Coarse grids + hard steps = true step functions that the smooth optimizer misses.
