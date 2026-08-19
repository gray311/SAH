Erdos C5 minimization: Find step function h: [0,2]->[0,1] with integral(h)=1 minimizing max_k integral h(x)(1-h(x+k))dx.

Target: c5_bound < 0.38092303510845016 (combined_score > 1.0).

PROVEN FAILURE: All 8 previous harness attempts reached exactly 0.999945 (seed score).

ROOT CAUSE: The harness wastes iterations on random hyperparameter tweaking. The seed optimizer's 15 patterns are designed to create diverse initializations. Instead of small hyperparameter changes, we need to FORCE exploration of different function shapes.

NEW STRATEGY: Use existing generate_ready_candidates tool for instant candidate generation

1. ITERATION 1: Call generate_ready_candidates(temperature=0.5)
   - Returns 3 candidates with precomputed c5_bound (no training needed)
   - Candidates are integral-constrained and ready to evaluate
   - Look for c5_bound < 0.375 candidates

2. ITERATION 2-4: Call evaluate_solution on top 2 candidates
   - If any achieve combined_score > 1.0, submit immediately
   - Typical target: c5_bound ~ 0.370 gives combined_score ~ 1.02

3. IF NO SUCCESS from candidates:
   - Fall back to pattern testing via edit_solution
   - Focus on Pattern 12 (Golomb) and Pattern 14 (Tri-modal)
   - Use probe_solution first to screen before full evaluation
 
4. USE TOOL STRATEGY:
   - generate_ready_candidates: BEST FIRST CHOICE - instant feedback
   - probe_solution: SECOND CHOICE - fast approximate evaluation
   - evaluate_solution: LAST RESORT - expensive, use only on promising candidates
   - edit_solution: For structural changes when tools don't help
 
5. STOP CRITERIA:
   - Submit immediately when combined_score > 1.0
   - After 10 iterations with no improvement, restart with temperature=1.2
