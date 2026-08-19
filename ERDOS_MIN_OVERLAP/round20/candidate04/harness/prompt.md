Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score (c5_bound < 0.380923).

CRITICAL: The seed optimizer already has 15 pattern variations. It STUCK at seed score.
Don't just add MORE pattern variations - they won't help.

NEW STRATEGY: Edit the optimizer's core algorithm structure, not just patterns.

1. First: Use probe_solution to test SMALL changes (one or two hyperparam changes)
   to confirm the evaluator responds to edits.

2. Then: Try completely different optimization approaches:
   - Change optimizer type (Adam -> SGD, or different learning rate schedules)
   - Change discretization (fewer intervals, different domain handling)
   - Change the C5 computation method (use convolution theorem differently)
   - Add explicit constraint enforcement during optimization

3. Don't evaluate all at once - use 1-2 evals per iteration, learn from feedback.

4. If edits fail, try a MINIMAL edit: change only num_intervals or learning_rate.

5. Track what changes work (probe) before committing to full evaluations.

Key: Structural algorithm changes, not pattern enumeration.
