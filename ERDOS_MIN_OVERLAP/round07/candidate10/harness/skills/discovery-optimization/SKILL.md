---
name: discovery-optimization
description: "Erd\u0151s C\u2085 bound optimization harness. The seed's gradient-based approach is stuck at 0.999641. Use the construct_candidate tool to build diverse step function candidates through combinatorial search rather than relying on Adam optimization alone. Target combined_score > 1.0."
---

# Erdős C₅ Minimum Overlap Problem

## Problem Statement

Find a step function h: [0,2] → [0,1] that minimizes:
max_k ∫₀² h(x)(1-h(x+k)) dx

Subject to: h∈[0,1], ∫₀² h(x)dx = 1

Current best: C₅ ≤ 0.38092303510845016

## Why Gradient Descent Gets Stuck

The objective landscape has many local optima. Adam optimization from random or simple patterns consistently converges to near-0.999641. The problem rewards clever piecewise constructions.

## Strategic Approach: Combinatorial Construction

**Do not rely solely on the seed's multi-restart Adam approach.** Instead:

### 1. Use construct_candidate for Diverse Generations

The `construct_candidate` tool builds step functions through:
- uniform: n equal-width intervals with constant height
- symmetric: patterns centered at x=1 (mirrored)
- concentrated: mass concentrated near endpoints [0,a]∪[2-a,2]
- multi_step: k-piece function with strategic breakpoints

Call this 3-4 times with different parameters to get diversity.

### 2. Evaluate, Don't Overfit

Each evaluation is precious (~30 total). After constructing 3-5 candidates:
- Evaluate the best ones
- If any score > 1.0, STOP and submit
- Otherwise, construct 2-3 new variations around the best structure

### 3. Refinement Strategy

If a constructed candidate is promising but not optimal:
- Use edit_solution to make targeted changes
- Adjust only 1-2 parameters
- Avoid long gradient descent runs

### 4. Template Constructions to Try

**Type A: Uniform Split**
- Divide [0,2] into n equal intervals
- Set h(x) = 2/n for half intervals, 0 for others

**Type B: Concentrated Mass**
- h(x) = c on [0,a] and [2-a,2]
- Choose c = 1/(2a) to satisfy ∫h = 1

**Type C: Symmetric Patterns**
- Create patterns centered at x=1, mirrored

**Type D: Multi-Step Functions**
- k-piece step functions with strategic breakpoints

## Execution Flow

1. Call construct_candidate(n_intervals=100, style="uniform") → evaluate
2. Call construct_candidate(n_intervals=100, style="symmetric") → evaluate
3. Call construct_candidate(n_intervals=200, style="concentrated") → evaluate  
4. Call construct_candidate(n_intervals=50, style="multi_step", steps=4) → evaluate
5. Pick best score, construct variations around it
6. If no improvement after 10 evals, try n_intervals=400, 800 on best style

## Critical Reminders

- **∫h must equal exactly 1** - construct_candidate handles this
- **h must be in [0,1]** - don't violate this
- **Coarse discretization often finds better global optima**
- **Stop when combined_score > 1.0**
