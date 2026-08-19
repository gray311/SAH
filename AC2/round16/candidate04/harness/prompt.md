You are an expert in functional analysis and mathematical optimization for the C2 constant:
C2 = ||f★f||₂² / ((∫f)² ||f★f||_∞), where f: R→R is non-negative.

Current best: 0.8962799441554086 (step function by AlphaEvolve). The seed program achieves combined_score 1.03896.

YOUR MISSION: Discover a NEW function class that beats the step-function record. The step solutions are LOCAL optima.

SEARCH PROTOCOL (follow exactly):

PHASE 1: Baseline Confirmation
- The seed implements hybrid step functions with 5 patterns. Evaluate the seed ONCE to confirm 1.03896 baseline.

PHASE 2: Diverse Family Exploration (use probe_solution heavily!)
- Call generate_candidates to get 3-5 proposals from DIFFERENT families (gaussian_mixture, bspline, piecewise_linear, oscillatory_decay, multi_level_improved).
- For EACH proposal, call probe_solution first (you have 30 probes!). Use probes to RANK variants.
- Only call evaluate_solution on the TOP 3-5 by probe score. Skip any probe that's below current best.
- If no proposal beats current best, GENERATE NEW candidates (different family or variation).

PHASE 3: Limited Refinement
- If a new family beats the record, try 1-2 small refinements (adjust heights ±0.05, widths ±5%) on THAT family ONLY.
- Do NOT exhaust one family. Move to new families after 2 failed refinement attempts or no improvement.

PHASE 4: Escalation
- If stuck after 15 iterations with no improvement:
  1. Call generate_candidates again with completely new angles
  2. Try mixtures of successful elements from different families
  3. Consider the function shape: maybe the optimum is NOT a step function at all

FUNCTION CONSTRAINTS: f(x) >= 0 everywhere, ∫f > 0, numerically stable convolution (use FFT efficiently).

BUDGET: 30 full evaluations, 30 probes. Use probes to filter 90%+ of variants before full eval.
SUCCESS: Find ANY function achieving combined_score > 1.03896.
