---
name: discovery-optimization
description: "Analyze the seed optimizer and try systematic hyperparameter sweeps,\nalgorithm modifications, and entirely new optimization strategies.\nFocus on c5_bound improvement through disciplined evaluation."
---

# Systematic C5 Optimization Strategy

## Step 1: Analyze the Seed

The seed code defines ErdosOptimizer with:
- 800 intervals (dx = 2/800 = 0.0025)
- 59000 optimization steps
- Learning rate 0.0062
- Penalty strength 61.0
- 3 restarts

## Step 2: Hyperparameter Sweep

Try these sweeps ONE at a time (one eval per sweep):

LR sweep:
- Try lr = 0.001, 0.01, 0.05, 0.1 (compare to seed 0.0062)
- Edits: change Hyperparameters.base_learning_rate

Steps sweep:
- Try steps = 10000, 20000, 100000 (compare to seed 59000)
- Edits: change Hyperparameters.num_steps

Penalty sweep:
- Try penalty = 10, 30, 100, 200 (compare to seed 61.0)
- Edits: change Hyperparameters.penalty_strength

Intervals sweep:
- Try intervals = 200, 400, 1600 (compare to seed 800)
- Edits: change Hyperparameters.num_intervals

## Step 3: Algorithm Modifications

Try these ONE at a time:

- Change optimizer to Adam: Replace SGD with optax.adam(0.01)
- Add constraint enforcement: Modify loss to penalize |∫h - 1| more heavily
- Modify initialization: Use better pattern starting points
- Multi-scale optimization: Coarse-fine approach (optimize coarsely, then refine)

## Step 4: New Approaches

- Direct pattern optimization: Instead of latent→sigmoid, optimize step thresholds directly
- Multiple small restarts: num_restarts=10, steps=5000 per restart
- Spectral relaxation: Try different Fourier-based approaches

## Step 5: Evaluation

After each edit:
1. Verify the code still compiles
2. Run evaluate_solution
3. Check combined_score
4. If no improvement, try next edit

## Constraint Checking

The constraint ∫h = 1 must be satisfied. The seed code normalizes candidates,
but the optimizer itself should maintain this during training. Consider:
- Adding a regularization term for integral constraint
- Using constrained optimization methods

## Success Criteria

- combined_score > 1.0 (c5_bound < 0.380923)
- NEW BOUND is YOUR goal
- Report all promising candidates with their scores

# Worked Example

Edit 1: Change lr from 0.0062 to 0.01

def run(ctx, args):
    h = edit_solution(...)  # get new code
    score = evaluate_solution()
    if score > 1.0:
        return "IMPROVEMENT: c5_bound improved!"

Remember: Each edit should be TESTED before the next.
