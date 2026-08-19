You are an expert in harmonic analysis and the Erdős minimum overlap problem.

Target: Find h: [0,2]->[0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k))dx.

Current best: C5 ≤ 0.38092303510845016. Beat this to get combined_score > 1.0.

SEARCH STRATEGY (CRITICAL):

1. Call analyze_constructions() FIRST to get multiple construction types with varied parameters

2. For EACH construction, run 3-5 restarts with different perturbations before calling evaluate_solution

3. Use probe_solution to rapidly rank variants within the local search

4. Only call evaluate_solution on your absolute best candidate from step 2

Key insight: The seed program's single-run-from-bad-init approach fails because the landscape has deep local optima. You need multiple restarts PER construction.

What to edit:
- Implement analyze_constructions() tool call at start
- Add a multi-restart loop: for each construction, run 3-5 perturbations
- Use probe_solution after each restart to rank locally
- Evaluate only the top candidate with evaluate_solution
- Ensure constraint satisfaction via penalty term
