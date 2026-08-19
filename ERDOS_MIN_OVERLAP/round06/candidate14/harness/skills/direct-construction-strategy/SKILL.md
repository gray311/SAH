---
name: direct-construction-strategy
description: Direct construction bypasses gradient optimization. Use when the seed's optimizer is stuck. Construct h piecewise, compute exact c5_bound, and submit.
---

# Direct Construction Strategy for Erdos C5

## When to Use This Skill

The seed program uses Adam optimizer achieving combined_score=0.999641. It's stuck because gradient descent cannot escape local optima.

Use this skill when:
- The harness probes show the optimizer isn't improving
- You need to try mathematically motivated candidate functions
- The goal is to find a simple, structured h that beats random initialization

## How to Use

1. Choose a strategy: single_step, double_step, three_step, symmetric, concentrated, or custom
2. Compute the function: Use construct_piecewise tool with your strategy
3. Verify constraints: Check that h in [0,1] and integral equals 1
4. Submit via edit_solution: Replace the entire EVOLVE-BLOCK
5. Evaluate: Call evaluate_solution on the new program

## Example Strategies

### Single Step
h(x) = 1 for x in [0, 1], h(x) = 0 for x in (1, 2]
Integral = 1, h in [0,1]

### Double Step
h(x) = 0.5 for x in [0, 0.5] union [1.5, 2], h(x) = 0 elsewhere
Integral = 0.5 times 1.0 = 1

### Concentrated Mass
h(x) = 1 for x in [0, 0.5], h(x) = 0 elsewhere
Integral = 1 times 0.5 = 0.5 (need to adjust)

## Key Insight

Direct construction gives you EXACT control over h's structure. The optimizer can only perturb; you CREATE. This is why direct construction can escape local optima that trap gradient-based methods.
