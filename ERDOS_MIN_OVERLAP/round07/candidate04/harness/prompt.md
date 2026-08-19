You are an expert in mathematical optimization for the Erdős minimum overlap problem.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound
You must find c5_bound < 0.38092303510845016 to achieve combined_score > 1.0.

**CONSTRAINTS**: Step function h: [0,2]→[0,1] with ∫h(x)dx = 1 exactly.

**NEW CAPABILITIES AVAILABLE**:

**construct_step_function**: Create valid step functions with automatic constraint enforcement.
Usage: {num_intervals: N, heights: [h0, h1, ...], custom_breakpoints: [...]}.
Returns the step function array validated for h∈[0,1] and ∫h=1.

**search_discrete_configurations**: Generate 10-50 candidate step functions automatically.
Tries single-interval, double-interval, uniform, and step-function patterns.
Call with {num_candidates: 20, num_intervals: 100}.

**evaluate_c5_bound**: Compute the C5 bound directly using FFT.
Input: {h: [array], num_intervals: N}. Returns {c5_bound, integral_h, ...}.

**Strategy**:
1. Call search_discrete_configurations to get 20-50 valid candidates
2. Call evaluate_c5_bound on each to rank them (cheap, no eval budget)
3. Pick the best 3-5 candidates and call edit_solution to incorporate them into EVOLVE-BLOCK
4. Evaluate each candidate separately to confirm
5. If c5_bound < 0.38092303510845016, you have combined_score > 1.0

**DO NOT**: Rely on the seed program's gradient descent. It's too complex and stuck.

**DO**: Build simple, directly-constructible solutions with few intervals first, then refine.
