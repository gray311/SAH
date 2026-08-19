---
name: constrained-optimization
description: Optimizing constrained mathematical functions with gradient descent. Use for tasks with hard constraints (integral=1, bounds [0,1]) and non-convex objectives. Key - strong penalty enforcement and gradual hyperparameter tuning.
---

Constrained Optimization with Gradient Descent

Problem Structure:
- Objective: Non-convex minimization (here: max overlap integral)
- Constraints: Hard bounds [0,1] and equality constraint integral(h)=1.0
- Solver: Adam optimizer with penalty method
- Evaluation: FFT-based correlation computation (fast, ~10ms)

Penalty Method:
The constraint integral(h)=1.0 is enforced via:
loss = objective + penalty_strength * (integral(h) - 1.0)^2

Tuning guidelines:
- penalty_strength: Start at 1370, adjust to [1000-2000]
- If validity=0: penalty too low, increase it
- If optimization stalls: penalty too high, decrease slightly

Hyperparameter Tuning Order:
1. First: base_learning_rate (most sensitive)
2. Second: num_steps (use full budget, FFT is fast)
3. Third: num_restarts (diversify initializations)
4. Last: num_intervals (800 is already appropriate)

Initialization Patterns:
The seed uses 12 patterns including: random normal, sinusoidal, step functions.
All are transformed via sigmoid to [0,1] then normalized.
Do not remove patterns - diversity helps escape local minima.

Evaluation Feedback:
- combined_score > 1.0: found better bound (SUCCESS)
- combined_score ~ 1.0: similar quality (continue tuning)
- combined_score < 1.0: worse (revert and try different direction)
- validity=0: constraint violated (check penalty_strength)

Common Pitfalls:
1. Reducing num_steps too much - need ~50k+ iterations
2. Lowering penalty_strength below 1000 - constraints violated
3. Changing architecture unnecessarily - the FFT approach is optimal
4. Ignoring constraint_loss - watch for integral(h) != 1.0

When to Stop:
- Score > 1.0 and cannot improve further
- 30 evaluations used without success
- Diagnostics show fundamental constraint issues (unlikely with proper tuning)
