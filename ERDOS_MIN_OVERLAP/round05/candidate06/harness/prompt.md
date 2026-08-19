You are optimizing a hyperparameter-heavy continuous optimization problem: finding a step function h that minimizes max_k ∫ h(x)(1-h(x+k)) dx.

TASK FRAMEWORK:
- The code has a fixed entry function (main) with Hyperparameters dataclass
- You must tune hyperparameters (num_intervals, base_learning_rate, num_steps, penalty_strength) and algorithm structure
- Budget: 30 full evaluations only. Use probes extensively!

STRATEGY (follow strictly):
1. NEVER make cosmetic changes. Every edit must meaningfully change:
   - Hyperparameter values (especially penalty_strength, base_learning_rate)
   - Optimization algorithm (optimizer type, AdamW vs Adam, learning rate schedules)
   - Initialization strategy (different random seeds or patterns)
   - Constraint handling methods

2. PROBE FIRST, EVALUATE LATER:
   - Before ANY full evaluation, call probe_solution to rank your variants
   - Probe is cheap (~10s) and doesn't consume eval budget
   - Only call evaluate_solution on the top 1-2 variants from probes

3. ITERATE SMARTLY:
   - max_iterations=8 because 30 evals ÷ 3-4 probes per variant = 8-10 meaningful test variants
   - Keep iterations tight: edit → probe → probe → evaluate (if promising)
   - If probe score doesn't improve, don't waste a full eval

4. FIX CONSTRAINT VIOLATIONS:
   - The integral of h must equal 1.0 exactly
   - If validity=0, the constraint is violated - fix the penalty or reinitialization

5. WHEN TO EDIT:
   - Try different optimizers: optax.adam, optax.adamw, optax.rmsprop, optax.lamb
   - Try learning rate schedules: linear decay, cosine decay, constant
   - Try different num_intervals: [400, 800, 1600, 3200]
   - Try different penalty_strengths: [1000, 1370, 2000, 5000]
   - Try different initialization patterns (structured vs random)

Tools:
- edit_solution: Replace only the EVOLVE-BLOCK region. Use targeted diffs or complete rewrite.
- probe_solution: Call BEFORE any full eval. Uses ~2000-row subsample. Fast, no eval budget cost.
- evaluate_solution: Only call on variants that look promising from probes. Returns combined_score > 1.0 to beat baseline.
- finish: Call when you've exhausted 30 evals or can't improve.

OUTPUT EXPECTATION: Combined_score = 0.38092303510845016 / c5_bound. Need score > 1.0 to beat baseline (C5 < 0.380923). Most promising regions: reduce penalty_strength with better optimization, increase num_intervals for finer discretization, try AdamW with learning rate scheduling.
