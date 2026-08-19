---
name: discovery-optimization
description: "Hyperparameter and algorithm search for continuous optimization tasks with integral constraints. Uses probe-based ranking to efficiently explore hyperparameter space within strict eval budget."
---

# Hyperparameter Search for Optimization Tasks

## Problem Type
You are solving a continuous optimization problem where the goal is to find parameters of a step function h(x) that minimizes an integral objective. The evaluator rewards combined_score = baseline / found_value. Need combined_score > 1.0 to improve.

## Critical Constraints
- **Integral constraint**: ∫ h(x) dx = 1.0 exactly. If validity=0, this constraint is violated.
- **Eval budget**: Only 30 full evaluations allowed. Every eval must count.
- **Time limit**: Each evaluation has a hard timeout. Keep internal search bounded.

## Strategy: Probe-First Evaluation

### Step 1: Edit with One Change
Make exactly one meaningful change to the EVOLVE-BLOCK:
- Change ONE hyperparameter at a time (e.g., penalty_strength: 1370 → 2000)
- OR change optimizer (Adam → AdamW, add learning rate schedule)
- OR change initialization pattern
- OR change num_intervals (affects discretization granularity)

**DO NOT** make cosmetic changes. Every edit must be substantive.

### Step 2: Probe (Mandatory)
**Before every full evaluation, call probe_solution.**
- Probe uses ~2000-row subsample: ~10s runtime, no eval budget cost
- Check if probe indicates improvement over best_so_far
- If probe score is worse or no improvement, skip full evaluation and try a different variant

### Step 3: Evaluate (Only if Promising)
Call evaluate_solution ONLY if:
- Probe score shows clear improvement trend
- You have probes left and want to confirm with full eval
- You've exhausted probe-based ranking and need to commit

## Hyperparameter Space to Explore

### Learning Rate Strategies
1. **Constant**: base_learning_rate = [0.001, 0.005, 0.01, 0.05]
2. **Linear decay**: Decrease LR over num_steps
3. **Cosine decay**: Smooth LR decrease
4. **Warmup**: Start low, ramp up

### Optimizers
- optax.adam (default)
- optax.adamw (better weight decay)
- optax.rmsprop (good for non-stationary objectives)
- optax.lamb (adaptive with layer-wise scaling)

### Penalty Strength
Try: [500, 1000, 1370, 2000, 5000, 10000]
- Too low: constraints violated, invalidity=0
- Too high: optimization stalls, stuck in poor local minima
- Optimal: depends on initialization quality

### Discretization
Try num_intervals: [400, 800, 1600, 3200]
- More intervals = finer function representation = better potential
- But also more optimization steps needed

### Initialization Patterns
The seed uses 12 random patterns. Consider:
- Structured patterns (step functions, sinusoidal)
- Multi-level search (coarse → fine)
- Gradient-based warm starts

## Iteration Budget
- max_iterations = 8 (not 36!)
- Each iteration: 1 edit, 1-2 probes, possibly 1 eval
- Total evals per harness run: 30
- With 8 iterations, you can test 3-4 full variants

## Common Mistakes to Avoid
1. **Changing multiple things at once**: Can't tell which change caused improvement/regression
2. **Not using probes**: Wasting evals on variants you can already tell are bad
3. **Ignoring validity=0**: If constraint violated, the score is meaningless
4. **Too many iterations**: 36 iterations with 30 evals = bad signal-to-noise

## Output Format
Your edits must preserve the fixed entry function and imports. Only modify the EVOLVE-BLOCK region between markers.

**SUCCESS CRITERIA**: combined_score > 1.0 means you found h where c5_bound < 0.38092303510845016.
