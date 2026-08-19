You are solving the Erdos minimum overlap problem: find a step function h: [0,2] -> [0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k)) dx.

Current best bound: C5 <= 0.380923
Your seed program uses gradient descent with multi-restart, but it is STUCK AT THE SEED SCORE. This means the gradient approach is trapped in local minima.

NEW STRATEGY: Do NOT just tune hyperparameters. Instead, DIRECTLY CONSTRUCT candidate step functions using piecewise-constant patterns. The optimal solution is likely a specific arrangement of plateaus at discrete values.

PHASE 1: Constructive Search (Use all 30 evals)
1. Build explicit step functions with SPECIFIC plateau configurations:
   - Single plateau at value 0.5: h(x) = 0.5 for all x (gives integral=1, check c5)
   - Two plateaus: h(x) = a for x in [0, L], h(x) = b for x in [L, 2] where a*L + b*(2-L) = 1
   - Three plateaus: h(x) = a, b, c on intervals [0,p1], [p1,p2], [p2,2] with weighted sum = 1
   - Staircase patterns: h(x) = [1,0,1,0,...] alternating (binomial pattern)
   - Concentrated mass: h(x) = 1 on small interval, 0 elsewhere (spike pattern)
   - Spread patterns: h(x) = 0.3 on wide intervals, 0.7 on narrow intervals
2. For each construction, call probe_solution to quickly screen
3. Call evaluate_solution on the best 3-4 candidates
4. If no improvement, try DIFFERENT construction types (not just parameter tweaks)

PHASE 2: Hybrid Approaches
If constructive search fails, then try:
- Use constructive patterns as INITIALIZATIONS for gradient descent (not just random seeds)
- Try DIRECT search over plateau configurations (enumerate small discretizations)

PHASE 3: If still stuck
- Modify _get_best_initialization to ADD constructive patterns (plateau-only, step-only)
- Consider that the seed best might not be globally optimal

FOCUS: BUILD SOLUTIONS DIRECTLY, DO NOT JUST OPTIMIZE RANDOM SEEDS.
