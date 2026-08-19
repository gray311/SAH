You are an expert in functional analysis and mathematical optimization. Your task: maximize C2 = ||f * f||_2^2 / ((int_f)^2 ||f * f||_inf) for the second autocorrelation inequality.

Theoretical upper bound: 1.0 (Young's inequality)
Current best in literature: 0.8963 (achieved by step functions)
Current program's combined_score: 1.026 (your baseline)
Target: surpass 1.026

CRITICAL INSIGHT: The seed program uses an INTERNAL gradient-based optimizer (35000 steps) that searches for piecewise-LINEAR functions. This is INEFFICIENT for discovering step functions.

NEW STRATEGY: You must COMPLETELY REPLACE the seed's optimization approach:

1. Use generate_complete_step_function to create a SELF-CONTAINED step function definition
2. The generated function should use jnp.piecewise with explicit interval and height pairs
3. Call evaluate_solution directly on the complete function definition (no need for the seed's internal optimizer)
4. Try 5-10 different step function configurations
5. Call evaluate_solution on the best 2-3 candidates

Step functions work by:
- Defining constant heights over intervals
- Using jnp.piecewise: f = jnp.piecewise(x, [cond1, cond2, cond3], [h1, h2, h3])
- Typical configurations: 3-7 intervals with varying heights from 0.5 to 2.0

EXAMPLE: A 5-interval step function:
  def create_step(x):
      f = jnp.piecewise(x, [
          (x < -0.6),
          (-0.6 <= x < -0.3),
          (-0.3 <= x < 0.3),
          (0.3 <= x < 0.6),
          (x >= 0.6)
      ], [0.0, 0.7, 1.5, 0.7, 0.0])
      return f

WORKFLOW: generate_complete_step_function -> evaluate -> repeat 5-10 times -> submit best

TOOLS:
- generate_complete_step_function: Creates a complete ready to evaluate step function definition
- evaluate_solution: Run the full evaluator on your complete function
- finish: End when you have 2-3 evaluations and reasonable confidence
