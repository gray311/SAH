---
name: discovery-optimization
description: "Optimize a JAX-based function minimizer for the Erd\u0151s minimum overlap problem. Use quick_eval to test configs cheaply, then evaluate promising candidates. Preserve constraint satisfaction (integral=1.0) while reducing the C5 bound."
---

# Erdős C5 Optimization Strategy

**Objective**: Minimize C5 = max_k ∫h(x)(1-h(x+k))dx by optimizing step function h.
**Score**: combined_score = 0.380923 / C5 (maximize this, target > 1.0).

## Structure
- Hyperparameters control: num_intervals (discretization), base_learning_rate, num_steps, penalty_strength, num_restarts
- _get_best_initialization tries 12 pattern variants with sigmoid activation
- _objective_fn = overlap_objective + penalty_strength * (integral-1.0)^2
- Constraints: h in [0,1], ∫h = 1.0

## Strategy
1. **Preserve the seed structure** - the 12-pattern initialization works, improve it:
   - Add more pattern diversity (piecewise, multiresolution, learned features)
   - Adjust scaling factors (try latents with different std devs)
   - Add temperature/scale annealing

2. **Hyperparameter search** (use quick_eval first, then eval):
   - Learning rate: 0.001, 0.005, 0.01, 0.02
   - Penalty: 500, 1000, 2000, 5000 (too high over-constrains, too low ignores constraint)
   - Steps: 50000, 100000, 200000 (trade-off: more steps = better, but timeout risk)
   - Intervals: 800, 1200, 2000 (higher = better resolution but slower)
   - Restarts: 3, 5, 10 (more restarts = better coverage)

3. **Optimizer experiments**:
   - Try optax.adamw (weight decay regularization)
   - Try optax.rmsprop (better for oscillatory objectives)
   - Try optax.adagrad (larger early steps)
   - Try schedule: decay learning rate by 0.95 per 10k steps

4. **Pattern improvements**:
   - Add triangular/sawtooth patterns
   - Add multi-scale sin/cos combinations
   - Add block patterns with varying widths
   - Add learned parameterization (a few weights to train patterns)

5. **Quick_eval vs Eval**:
   - quick_eval: Run 100 iterations with num_intervals=200, check if integral≈1 and obj improves
   - evaluate_solution: Only if quick_eval shows obj improvement AND constraint satisfied within 5%
   - Always start with quick_eval to avoid wasting evaluations on invalid configs

## Common pitfalls
- Breaking the optimization loop (missing return, wrong variable)
- Syntax errors in JAX code (jax vs np conflicts)
- Forgetting to apply gradient through constraint properly
- Making num_intervals too large causing timeout
- Penalty too high making convergence impossible

## Tool sequence example
1. quick_eval with: lr=0.01, penalty=5000, steps=10000 (quick feasibility check)
2. If feasible, evaluate_solution with: lr=0.01, penalty=5000, steps=100000 (full run)
3. If score improves, try edit to increase steps or adjust hyperparams
4. Try different optimizer variant
5. finish when 2 consecutive quick_evals show no improvement or evals exhausted
