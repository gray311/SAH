You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx
for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016

CRITICAL INSIGHT: The goal is a TRUE STEP FUNCTION, not a smooth function.
The seed program's multi-restart optimizer produces smooth h(x) via sigmoid(latent),
which gives poor results. You must DIRECTLY CONSTRUCT step functions.

Strategy: Generate h(x) as a piecewise-constant function with k jumps at positions [t_1, t_2, ..., t_{k-1}]
where 0 < t_1 < t_2 < ... < t_{k-1} < 2.

Steps:
1. Call evaluate_solution on seed to establish baseline
2. EDIT to create k-piece step functions:
   - Vary number of pieces: k = 2, 3, 4, 5, 6, 8, 10, 12, 16
   - For each k, generate random jump positions and compute level heights to satisfy integral(h)=1
   - Level heights are chosen from {0, 1} for binary, or fractions for multi-level
3. For each candidate, use probe_solution to check integral constraint quickly
4. Call evaluate_solution on candidates that pass probe
5. Track best combined_score, continue generating new step configurations
6. If stuck at smooth init, completely replace _get_best_initialization with piecewise step generator
7. Keep iterating until combined_score > 1.0 or budget exhausted

Focus: DIRECT STEP FUNCTION CONSTRUCTION, not hyperparameter tuning of smooth functions.
