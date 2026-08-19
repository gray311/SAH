Erdos minimum overlap problem: find step function h with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k))dx.
Current best bound: 0.38092303510845016. Goal: beat this.
Use PROVEN PERIODIC STEP FUNCTION construction.
Worklfow: Start with PERIODIC_STEP. Fine-tune width w in [0.3,0.5] and position a in [0.25,0.75].
Use probe_solution to test (w,a) pairs. Evaluate TOP 2 candidates.
Replace EVOLVE-BLOCK with CONSTRUCTOR_LOOP. Compute c5 via FFT directly (no optimization).
Target: combined_score > 1.0.
