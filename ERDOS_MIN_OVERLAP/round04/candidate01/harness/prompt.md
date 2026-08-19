You are an expert in harmonic analysis and the Erdős minimum overlap problem.

Your goal: beat the current best bound C5 <= 0.38092303510845016 by finding a step function h: [0,2]->[0,1]

with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k))dx.

Key insight: The constraint integral(h)=1 is CRITICAL. Start with INITIALLY VALID functions (integral=1) to avoid wasting optimization steps on constraint satisfaction.

The landscape is non-convex, but known constructions (periodic step functions, bimodal distributions) provide good starting points.

Strategy:

1. Use generate_constrained_init() to generate an h VALUE (not latent) with integral(h)=1 EXACTLY satisfied

2. Use penalty_annealing_workflow: start with low penalty strength, gradually increase

3. Call evaluate_solution on promising candidates to verify constraint satisfaction

4. Use probe_solution only after verifying the solution is valid (integral close to 1)

What to edit:

- Replace latent-based initialization with direct h values that satisfy integral=1

- Implement penalty annealing: start penalty=100, end penalty=5000 over the optimization run

- Add constraint checking before each evaluation

Target: combined_score > 1.0 (c5_bound < 0.380923)
