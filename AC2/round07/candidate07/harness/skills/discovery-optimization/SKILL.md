---
name: discovery-optimization
description: "Step function optimization. Use generate_complete_step_function to create complete step function definitions with jnp.piecewise. Evaluate directly without the seed's internal optimizer. Try 5-10 configurations, evaluate top 2-3. Target >1.026."
---

# Step Function Optimization for C2 Maximization

The seed uses a 35000-step gradient optimizer for piecewise-LINEAR functions. This is too slow and does not naturally discover step functions.

Step functions are piecewise-CONSTANT (flat, not sloped). Create them directly with jnp.piecewise.

Method:
1. Use generate_complete_step_function to get a COMPLETE function definition
2. The output should be ready to paste into your solution (or use directly)
3. Call evaluate_solution on the complete definition
4. Try 5-10 different configurations (vary intervals and heights)
5. Evaluate the 2-3 best ones
6. finish

Step Function Design Principles:
- Heights typically range from 0.5 to 2.0
- 3-7 intervals work well
- Symmetric functions (3-5 intervals centered at 0) are promising
- Asymmetric functions with varying heights can also work
- Avoid too many intervals (slower convolution)

Example Configurations to Try:
1. Simple 3-interval symmetric: [0.0, 1.2, 0.0]
2. 5-interval symmetric plateau: [0.0, 0.7, 1.5, 0.7, 0.0]
3. Multi-peaked asymmetric: varying heights from 0.5 to 2.0
4. Pyramid shapes: low-high-low pattern

Probe/Eval Strategy:
- NO need for probe_solution - evaluate directly on complete step functions
- Try 5-10 different step functions
- Evaluate the 2-3 that look most promising (based on configuration complexity)
- finish when you have 2-3 evaluations

Remember: step functions beat linear functions for this problem. Use generate_complete_step_function to create TRUE constant step functions.
