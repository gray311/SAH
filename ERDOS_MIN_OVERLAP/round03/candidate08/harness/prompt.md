You are an expert in harmonic analysis and the Erdos minimum overlap problem.

Target: Beat C5 <= 0.38092303510845016 by finding a step function h: [0,2]->[0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k))dx.

CRITICAL INSIGHT: The optimal solution likely comes from structured combinatorial designs (Golomb rulers, specific periodic patterns). 
The seed program's optimizer is good but its initialization is limited.

STRATEGY THAT WORKS:

1. USE internal_golomb_search() FIRST - this tool searches over Golomb ruler parameterizations to find the best construction
2. For each promising Golomb construction, RUN ADAPTIVE OPTIMIZATION with staged hyperparameters
3. Run phased optimization: Phase 1 (exploration, lr=0.05, penalty=1000, 10000 steps) -> Phase 2 (refinement, lr=0.01, penalty=5000, 15000 steps) -> Phase 3 (fine-tuning, lr=0.001, penalty=20000, 5000 steps)
4. Use probe_solution to quickly rank candidates by c5_bound
5. Evaluate the top 2-3 candidates with evaluate_solution

WHAT TO EDIT IN EVOLVE-BLOCK:
- Implement internal_golomb_search() with internal parameter tuning over mark count (3-8), mark positions (local search), kernel types (Gaussian/boxcar), and widths
- Integrate the search results into your optimization workflow
- Add phased training as described above
- Use probe_solution extensively during the search to avoid wasting evaluate_solution budget

TARGET: combined_score > 1.0 (c5_bound < 0.380923)
