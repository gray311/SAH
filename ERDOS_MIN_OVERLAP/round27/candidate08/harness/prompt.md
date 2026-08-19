Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: To minimize overlap between h(x) and h(x+k), use NARROW, WELDSPACED pulses.
The optimal pattern uses triangular pulses with width ~0.15-0.2 centered at marks that maximize
separation. Try 4-6 marks spaced at ~0.5 intervals: [0.2, 0.7, 1.2, 1.7] or similar.

STRATEGY:
1. FIRST: Call generate_structural_variants to get pre-optimized pulse patterns (no training needed)
2. Each candidate is integral-normalized and has c5_bound computed analytically via FFT
3. FILTER: Keep only candidates with c5_bound < 0.375
4. EVALUATE: Run full 59000-step optimization ONLY on filtered candidates
5. If no improvement after 3 tries, call generate_structural_variants with different parameters

USE probe_solution for rapid screening of edited solutions. Only spend full evals on c5_bound < 0.375.

AVOID: Don't waste evaluations tuning hyperparameters of poor initializations.
The initial h function form MATTERS more than optimizer hyperparameters.
