You are optimizing a JAX/NumPy program to solve the Erdos minimum overlap problem:
Find h: [0,2]->[0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k)) dx.

Current best: C5 <= 0.38092303510845016. Beat this with combined_score > 1.0.

CRITICAL STRATEGY FOR THIS TASK:
The seed program has only 12 fixed initialization patterns and 59000 optimization steps.
It gets stuck in local optima. To break through:

1. IN EVERY evaluation, implement a multi-restart loop inside _optimize_single_run:
   - For EACH of 5 different initializations (try them all):
     a) Use a DIFFERENT structured init pattern (bimodal, triangular, periodic, Golomb, sine-wave)
     b) Run 3000 steps with aggressive LR=0.05, penalty=5000
     c) Run 10000 steps with moderate LR=0.01, penalty=20000
     d) Use probe_solution (CHEAP) to get c5_bound
     e) Pick the 2 best by probe and evaluate them fully
   - The best of all 5 restarts is your final answer

2. VARY num_intervals: Try [400, 800, 1200, 1600] across different restarts.
   Higher resolution can find finer structures.

3. USE probe_solution FREQUENTLY: Rank all 5 restarts by probe before spending eval budget.

4. The seed program's 12 patterns are ALL variants of the same basic ideas (bimodal, triangular, periodic).
   Your multi-restart must actually TRY THEM DIFFERENTLY with different hyperparams.

Write code that implements this EXACT multi-research loop. Call probe_solution 5 times, evaluate 2 times max.
