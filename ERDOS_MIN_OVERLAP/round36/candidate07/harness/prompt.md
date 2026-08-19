Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

SEARCH STRATEGY (CRITICAL):
The seed program uses 800 intervals and sigmoid parameterization with 13+ pattern initializations.
Current harness fails because it relies on correlation_analyzer which CANNOT parse the seed's h array format.
The seed stores h as: h = array((v0, v1, ..., v799)) with ~500-600 digits total.

FIX: Use EDIT_DIRECT to manually craft a new h array with the SPECIFIED NUMBER of intervals, ensuring:
  - sum(h) * (2.0 / N) = 1 (integral constraint)
  - All values in [0, 1]
  - Use sparse peaks (narrow Gaussians or boxcars) to create low-overlap structures

NEW WORKFLOW:
1. Decide on a SPARSE PEAK COUNT (start with 3-4 peaks)
2. Use EDIT_DIRECT to manually write a new h array with:
   - Exactly N intervals (match seed or try smaller N=200, 400, 800)
   - Peaks at strategic positions (e.g., 0.0, 0.66, 1.33) to minimize self-overlap at shifts k=1,2,...
   - Smooth transitions between peaks (sinusoidal ramps or sigmoid blends)
3. CALL evaluate_solution immediately on the crafted h
4. If score <= 1.0, try DIFFERENT peak counts and positions

KEY INSIGHT: The seed's 13+ patterns are too broad and overlapping. Sparse, well-separated peaks may achieve lower C5.
Try: 3 peaks at 0.0, 0.66, 1.33 (Golomb-like) OR 2 peaks at 0.0, 1.33 OR 4 peaks at 0.0, 0.5, 1.0, 1.5

Stop patterns: Reduce from 13 to 3-5 distinct peak configurations.
Focus on structural simplicity over hyperparameter tuning.
