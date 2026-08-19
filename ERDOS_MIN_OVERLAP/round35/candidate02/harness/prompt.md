Erdos C5 Problem: Find a step function h: [0,2] -> [0,1] such that integral(h) = 1 and h values are in [0,1].
Goal: Minimize max_k integral(h(x)(1-h(x+k)) dx) to get c5_bound < 0.38092303510845016.

CRITICAL INSIGHT: The seed program uses sigmoid(latent) which is a smooth, non-step function. This violates the "step function" spirit and makes correlation structure hard to control.

STRATEGY:
1. FIRST generate PURELY STEP-FUNCTION candidates using search_step_functions tool (binary arrays with controlled transitions).
2. Generate 5-10 diverse step functions with integral = 1 exactly (fixed number of ON intervals).
3. Use probe_solution to quickly score these (cheap analytical check).
4. Only call evaluate_solution if probe suggests c5_bound < 0.385.

DO NOT start with sigmoid optimization. Step functions have simpler, more predictable correlation structure.
