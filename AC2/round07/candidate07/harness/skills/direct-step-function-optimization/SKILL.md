---
name: direct-step-function-optimization
description: Playbook for discovering step functions by direct generation and evaluation. Bypass the seed's slow optimizer.
---

# Direct Step Function Optimization

The seed's 35000-step gradient optimizer is designed for piecewise-LINEAR functions.
Step functions are piecewise-CONSTANT and can be discovered much more efficiently
by direct generation.

Method:
1. Use generate_complete_step_function to create a complete step function definition
2. The output contains ready-to-use jnp.piecewise code
3. Evaluate directly without running the seed's internal optimizer
4. Try 5-10 different configurations (vary num_intervals, symmetry, heights)
5. Evaluate the 2-3 best candidates
6. finish

Configuration Space to Explore:
- Symmetric 3-interval: [low, high, low]
- Symmetric 5-interval: [low, med, high, med, low]
- Symmetric 7-interval: more gradual peaks
- Asymmetric multi-peak: varying heights across the domain

Height Guidelines:
- Peak heights: 1.2 to 1.8 (higher than baseline)
- Base heights: 0.5 to 0.9 (lower than peak)
- Try combinations that create contrast

Evaluation Strategy:
- NO gradient optimizer needed - the step function is complete
- Try 5-10 different step function definitions
- Evaluate each directly with evaluate_solution
- submit_spec with the best result

Remember: step functions beat linear functions for this problem. Generate complete step functions directly!
