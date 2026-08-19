Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. Generate multiple diverse step function candidates with SHARP, DISTINCT PEAKS at carefully chosen locations.
   Examples of promising structures:
   - Two narrow peaks separated by exactly 1.0 (anti-aligned at shift k=1)
   - Three peaks at positions 0.25, 1.0, 1.75 (period-1.75 spacing)
   - Four peaks at 0.125, 0.875, 1.375, 2.0 (quarter-period spacing)
   - Peaks at fractional positions that are NOT integer fractions of 2.0 (irrational-like spacing)

2. For each candidate, ensure:
   - The function is a STEP FUNCTION (piecewise constant)
   - Values are exactly 0 or 1 (or very close, then sigmoid-smoothed)
   - Integral over [0,2] equals 1 (total width of "1" regions = 1.0)

3. When editing, create COMPLETE step functions from scratch, not incremental tweaks.
   Use the stage_edit tool to replace the entire h array with new sharp peaks.

4. Use probe_solution to quickly screen which peak configurations look promising.
   Look for candidates with c5_bound < 0.375 before full evaluation.

5. Only call evaluate_solution on candidates that are structurally different from the seed.

KEY INSIGHT: The seed program's slow gradient-based optimization is too weak.
Instead of optimizing existing patterns, GENERATE NEW step function PATTERNS with
deliberately separated peaks that avoid overlap at critical shifts.
