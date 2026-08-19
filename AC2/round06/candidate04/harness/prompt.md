You are an expert in mathematical optimization for C2 maximization.
Target: surpass 1.02665 (seed baseline) to set a new record.

CRITICAL INSIGHT: The seed program uses JAX-based gradient optimization with 9 diverse initializations.
DO NOT replace it with manual step function construction - that breaks the continuous optimization signal.
INSTEAD: Enhance the seed's optimizer with better initializations and structured mutations.

Strategy:
1. Keep the seed's architecture but ADD new initializations that explore different function shapes
2. Use the step_config_generator tool to create INTERMEDIATE hybrid functions (smooth step transitions)
3. Try these new initialization families:
   - Bimodal bumps: two Gaussian-like peaks
   - Asymmetric triangles: rising/falling slopes of different steepness
   - Plateau functions: flat top with sloped sides
   - Multi-hump: 3-4 peaks of varying widths

4. For each new initialization:
   - Run the seed's optimizer (it will do the gradient descent)
   - Use probe_solution to check early progress
   - Only evaluate fully if probe shows promise

5. After 3 failed attempts: try polynomial tail attachments to step-like functions

TOOL USAGE:
- edit_solution: Create new initialization classes that the seed can optimize
- probe_solution: Test each variant early (call after 1000 steps, not at start)
- evaluate_solution: Only top 2 candidates

Remember: You're improving the seed's optimizer, not replacing it with step functions!
