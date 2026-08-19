Solve the Erdos minimum overlap problem by directly constructing and evaluating step functions using the FFT evaluator.

Current best bound: C5 <= 0.38092303510845016
Goal: Find h: [0,2] -> [0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k)) dx

STRATEGY: The seed program runs 59000 training steps per evaluation - TOO SLOW. Instead, EDIT to:

1. REPLACE _get_best_initialization with DIRECT CONSTRUCTION of candidate step functions (no training needed)
2. REPLACE _objective_fn to ONLY return the FFT-based c5_bound (no penalty, no gradient)
3. Replace the optimizer loop with a SIMPLE SEARCH: edit the code to iterate over many candidate constructions, each evaluated with the FFT in ~10ms
4. Use EDIT to inject new candidate constructions (Golomb ruler, bipartite, multi-peak, etc.)
5. Call probe_solution to verify constraint satisfaction (integral=1, range [0,1])
6. Call evaluate_solution ONCE on the best candidate found

Key insight: The FFT evaluator is INSTANTANT. Don't waste 59000 steps. Direct construction + FFT evaluation = thousands of candidates per eval budget.
