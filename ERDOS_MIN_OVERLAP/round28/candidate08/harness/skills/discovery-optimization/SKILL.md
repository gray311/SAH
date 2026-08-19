---
name: discovery-optimization
description: "Systematic hyperparameter tuning for Erdos C5 optimizer. The seed optimizer trains latent vectors via gradient descent. We must find hyperparameters (learning_rate, penalty_strength, num_steps, num_intervals, num_restarts) that produce c5_bound < 0.380923. Use short training runs (5000 steps) for screening, full runs for confirmation. Always vary one parameter at a time. Use probe_solution before evaluate_solution."
---

# Hyperparameter Tuning for Erdos C5

## Understanding the Seed Optimizer

The seed optimizer:
1. Takes a latent vector (via one of 15 patterns in _get_best_initialization)
2. Applies sigmoid to get h in [0,1]
3. Trains for num_steps using gradient descent
4. Minimizes max_k integral h(x)(1-h(x+k))dx while enforcing integral(h)=1

## Strategy: Systematic Hyperparameter Search

### Step 1: Establish Baseline
Run the seed configuration:
- num_intervals=800
- base_learning_rate=0.006
- num_steps=59000
- penalty_strength=60.0
- num_restarts=3

### Step 2: Quick Screening with Short Runs
Before full 59000-step training, test short runs:
- Set num_steps=5000, num_restarts=1
- Use probe_solution to check c5_bound
- Target: c5_bound < 0.382 (allow margin)

### Step 3: Parameter-by-Parameter Tuning

**base_learning_rate:**
- 0.001: Very conservative, stable but slow
- 0.005: Seed default, balanced
- 0.01: Aggressive, may overshoot
- 0.02: Very aggressive, unstable

**penalty_strength:**
- 20: Weak constraint (integral may violate)
- 40: Moderate
- 60: Seed default
- 80-120: Strong constraint (enforces integral=1)

**num_steps:**
- 5000: Quick screening
- 10000: Short training
- 30000: Medium training
- 59000: Seed default (full training)
- 80000-120000: Extended training

**num_intervals (grid resolution):**
- 400: Coarse, faster but may miss structure
- 800: Seed default
- 1600: Finer
- 3200: Very fine, slower

**num_restarts:**
- 1: Single initialization (fast)
- 3: Seed default
- 5-10: More diversity

### Step 4: Pattern-Based Initializations (modify latent)

If hyperparameter tuning stalls, try different latent patterns in _get_best_initialization:

**Pattern 12 (Golomb ruler):**
marks = [0.0, 0.4, 0.8, 1.2, 1.6]  # 5 equally spaced marks

**Pattern 13 (Bipartite):**
x < 0.5: high (3.0), x >= 0.5: low (-3.0)

**Pattern 14 (Tri-modal):**
peaks at [0.4, 1.0, 1.6] with width ~0.24

**Pattern 5:**
x < 0.5: high (3.5), x >= 0.5: low (-3.5)

## Workflow

1. Run seed config (59000 steps, 3 restarts) - full evaluation
2. If no improvement, try short runs (5000 steps, 1 restart) with hyperparameter variations
3. Use probe_solution to screen short-run candidates
4. Evaluate promising candidates fully
5. If still stuck, try pattern modifications
6. Vary ONE parameter at a time to understand effects

## Key Tips

- Use probe_solution extensively to avoid wasting eval budget
- Start with short training runs for rapid exploration
- Only run full 59000-step training on promising candidates
- Track which parameters helped/hurt
