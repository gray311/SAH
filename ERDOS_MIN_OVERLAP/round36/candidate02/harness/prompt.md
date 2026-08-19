Erdos C5 Problem: Find step function h: [0,2]->[0,1] with integral=1 that minimizes max_k integral h(x)(1-h(x+k))dx.

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving combined_score > 1.0.

STRATEGY:

1. GENERATE diverse step function templates with different structures:
   - Single threshold (bipartite)
   - Multiple narrow peaks (multi-modal)
   - Symmetric patterns
   - Asymmetric patterns
   - Piecewise linear approximations

2. For EACH template, run full optimization with:
   - Different initial latent shapes
   - Variations in num_intervals (256, 512, 1024)
   - Different penalty_strength (40, 60, 80, 100)
   - Different num_steps (60000, 100000, 150000)

3. Call evaluate_solution on the BEST 2-3 templates from each mutation strategy
   - Prefer templates with fewer regions (less flexible but more stable)
   - Track which structure type produced improvements

4. If no improvement after exhausting templates, try extreme structures:
   - Almost all zeros with one narrow peak
   - Alternating narrow peaks
   - Concentrated near boundaries

KEY: The secret is STRUCTURE, not fine-tuning. Better initial step function shapes matter more than hyperparameters.
