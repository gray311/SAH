You are an expert in mathematical optimization for the Erdős minimum overlap constant C5.

THE OBJECTIVE: Maximize combined_score = 0.38092303510845016 / c5_bound
where c5_bound = max_k integral from 0 to 2 of h(x)(1-h(x+k)) dx

CONSTRAINTS: h:[0,2]->[0,1], integral from 0 to 2 of h(x) dx = 1

WHY WE'RE STUCK: The seed program uses 800 continuous parameters with Adam optimization,
which gets trapped in local optima. The optimal solution is likely a piecewise constant
function with FEW breakpoints, not 800 independent parameters.

NEW STRATEGY: Use the construct_candidates tool to generate explicit piecewise constant
functions with explicit breakpoints. Optimize only the breakpoint positions and heights,
not 800 latent values.

EXECUTION: 
1. Call construct_candidates to generate 5-10 diverse piecewise constant candidates
2. Evaluate each (use evaluate_solution - this evaluator is fast)
3. Combine the best patterns with refined discretization (500-1000 intervals)
4. Use the piecewise structure to guide the optimizer
5. Target combined_score > 1.0

AGENCY: COMPLETELY REWRITE the EVOLVE-BLOCK to use piecewise construction. Do not try
to fix the seed's gradient descent on 800 parameters. Build a new approach from scratch.
