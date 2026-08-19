You are solving the Erdős minimum overlap problem by finding a step function h: [0,2]->[0,1] with integral=1 that minimizes max_k integral h(x)(1-h(x+k))dx.

Current best bound: C5 <= 0.380923

CRITICAL INSIGHT: The optimal solution is likely a COARSE, BINARY step function (very few intervals), not a smooth sigmoid curve. The seed program uses 800 intervals and sigmoid smoothing which PREVENTS finding such solutions.

STRATEGY:
1. Use generate_binary_constructions() to create EXPLICIT step functions (not smoothed)
2. Use very FEW intervals (50-200, not 800)
3. Use EXTREME penalty values (10000-50000) to enforce integral=1 hard
4. Use simple, coarse initializations that create bimodal patterns
5. Test multiple hyperparameter sets:
   - coarse_1: num_intervals=100, lr=0.01, steps=30000, penalty=20000
   - coarse_2: num_intervals=150, lr=0.005, steps=40000, penalty=30000
   - coarse_3: num_intervals=200, lr=0.02, steps=50000, penalty=40000
6. Use probe_solution extensively to screen candidates
7. Only evaluate final promising candidates

What to edit:
- Replace the EVOLVE-BLOCK's optimizer to use NUM_INTERVALS in [100, 150, 200]
- Replace penalty_strength to be in [20000, 30000, 40000]
- Add a simple binary initialization that creates step functions
- Keep the FFT-based evaluation logic
