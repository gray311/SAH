---
name: function-diversity-protocol
description: Escape step-function local optimum by generating diverse mathematical function families.
---

# Function Diversity Protocol for C2 Maximization

## Why Step Functions Fail
The seed's 11 step patterns ALL achieve the same combined_score of 1.042. 
They're trapped in the SAME local optimum. Small mutations will NEVER escape.
You MUST generate fundamentally different function forms.

## Four Proven Function Families

### Family A: Gaussian Mixtures
- **Formula**: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))
- **Why it works**: Smooth convolution, analytically tractable
- **Parameters**: n_gaussians in [2,4], mu in [-2,2], sigma in [0.3,1.5]
- **When to use**: First choice - smooth functions often beat sharp steps

### Family B: Oscillatory Decay
- **Formula**: f(x) = (1 + alpha*cos(beta*x)) * exp(-gamma*|x|)
- **Why it works**: Built-in multi-peak structure from cosine modulation
- **Parameters**: alpha in [0.2,0.6], beta in [3,8], gamma in [0.5,1.2]
- **When to use**: When you want controlled oscillations with natural decay

### Family C: Symmetric Piecewise-Linear
- **Why it works**: Combines step-function discreteness with smooth transitions
- **Parameters**: 5-7 vertices, heights [h1,h2,h3,h2,h1]
- **When to use**: When Gaussian is too smooth, need more structure

### Family D: Multi-Level Asymmetric Steps
- **Why it works**: Improves on seed's symmetric patterns with asymmetry
- **When to use**: If smooth functions don't work, try refined steps

## Execution Protocol

### Iterations 1-15: Broad Exploration
1. Call propose_function_family to get parameters for a NEW family
2. EDIT the EVOLVE-BLOCK using those parameters
3. Call probe_solution to check if promising
4. If probe looks reasonable, call evaluate_solution
5. Track which families produced better results

### Iterations 16-30: Focused Refinement
1. Pick the BEST performing family from Phase 1
2. VARY its parameters systematically
3. Call probe on 3 variants, evaluate the best
4. If no improvement after 5 iterations: switch to different family

## Critical Rules
- NEVER mutate step functions after iteration 5 - they're stuck
- ALWAYS call propose_function_family when starting fresh
- ALWAYS probe before evaluate - save your 30 evals
- If stuck at iteration 12: try a family you haven't explored yet
