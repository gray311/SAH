Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly (critical!). h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: This is a PATTERN DISCOVERY problem, not hyperparameter tuning. The seed optimizer trains for 59000 steps - the bottleneck is finding the RIGHT initial pattern.

STRATEGY:

1. GENERATE INTEGRAL-CONSTRAINED PATTERNS: Call generate_ready_candidates(temperature=0.5) to get 3 integral-constrained initializations (Golomb, Bipartite, Tri-modal).

2. SCREEN WITH PROBE: For each candidate, call probe_solution to get approximate c5_bound. Only keep those with c5_bound < 0.375.

3. FULL EVALUATION: Call evaluate_solution on candidates with c5_bound < 0.370.

4. IF STUCK, VARY PATTERN PARAMETERS:
   - Golomb: Try marks = [0.0, 0.33, 0.66, 1.33, 1.66] (denser) or [0.0, 0.5, 1.0, 1.5] (sparser)
   - Tri-modal: Try peaks = [0.25, 1.0, 1.75] or add 4th peak at [0.2, 0.7, 1.0, 1.7]
   - Bipartite: Try split at 0.4, 0.6, or 0.7

5. USE probe_solution AGGRESSIVELY: Budget 30 probes. Screen 10-20 pattern variants before any full eval. Only spend 1 eval on the BEST probe candidate.

6. STOP if combined_score > 1.0 or if you exhaust probes with no < 0.375 candidate.

REMEMBER: The optimizer is well-tuned (lr=0.006, steps=59000, penalty=60). DON'T waste time retuning hyperparameters. Focus on finding better PATTERNS.
