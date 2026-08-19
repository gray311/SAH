You are an expert in harmonic analysis and combinatorial construction. Your task is to find a step function h: [0,2]→[0,1] with integral=1 that minimizes max_k integral of h(x)(1-h(x+k)) dx.

THE OBJECTIVE: Maximize combined_score = 0.38092303510845016 / c5_bound (need >1.0 for a new record).

KEY INSIGHT: This is a COMBINATORIAL CONSTRUCTION problem. Gradient descent from random initializations gets trapped in local optima. You MUST try structured step function PATTERNS.

STRATEGIC APPROACH:
1. MANUAL CONSTRUCTION FIRST: Before using optimizers, try explicit step functions with 2-4 breakpoints
2. SYSTEMATIC PATTERNS: Try single-step, double-step, symmetric wave, periodic patterns, concentrated mass
3. REFINE THEN OPTIMIZE: Once you have a promising manual construction, use fine-grained optimization
4. USE THE PROBE TOOL: Rank your candidate constructions with probe_solution before full evaluation

CONSTRAINTS: h in [0,1], integral over [0,2] must equal exactly 1. Use these to design your step functions.

BUDGET: ~30 evaluations. Spend on testing different CONSTRUCTION TYPES, not just tuning hyperparameters.

REWRITE STRATEGY: For each construction type, write COMPLETELY NEW code in the EVOLVE-BLOCK that builds that specific class of solutions. Don't patch the seed's optimizer.
