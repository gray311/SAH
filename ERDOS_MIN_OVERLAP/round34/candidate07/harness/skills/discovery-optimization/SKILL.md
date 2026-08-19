---
name: discovery-optimization
description: "Greedy hyperparameter search editing num_intervals penalty_strength learning_rate num_steps num_restarts and initialization patterns"
---

# Greedy Hyperparameter Search for Erdos C5

## Core Strategy
Edit the EVOLVE-BLOCK's Hyperparameters and initialization patterns directly.

## Step 1: Parameter Exploration
Try these hyperparameter combinations:

### num_intervals (resolution):
- 400, 600, 1000, 1600, 2000, 4000
- Higher = finer discretization but slower
- Start with 600-1000

### penalty_strength (integral constraint enforcement):
- 10, 20, 30, 40, 50, 80, 100, 150
- Higher = stronger constraint but may hurt optimization
- Try 30-50 as starting point

### base_learning_rate:
- 0.001, 0.002, 0.005, 0.01
- Lower = more stable, higher = faster but unstable
- Try 0.002-0.005

### num_steps:
- 60000, 90000, 150000, 200000
- More steps = better optimization but costs budget
- Try 90000-150000

### num_restarts:
- 5, 10, 15
- More restarts = better global search
- Try 5-10

## Step 2: Initialization Pattern Variations
Modify _get_best_initialization() to try:

### Bipartite:
h = sigmoid(latent) where latent = a*x + b
- Try different slopes and offsets
- Ensure integral(h) approx 1

### Multi-modal (3-4 peaks):
h = sum of 3-4 narrow Gaussian-like peaks
- Peak locations: [0.3, 1.0, 1.7], [0.2, 0.8, 1.2, 1.8]
- Width: 0.05-0.1
- Heights: scale to integral = 1

### Uniform-ish:
h = sigmoid((x - c) / s) - shifted sigmoid
- Try different centers c in [0.2, 0.5, 0.7, 1.0, 1.3, 1.6]
- Try different scales s

## Step 3: Greedy Search Loop
1. Start from seed
2. Pick ONE parameter to edit (e.g., num_intervals = 600)
3. Call probe_solution to estimate c5_bound
4. If c5_bound < 0.375, call evaluate_solution
5. If improved, use that as new seed and repeat
6. If no improvement after 2-3 edits, try a different parameter

## Key Rules
- Edit ONE hyperparameter at a time
- Use probe_solution to screen
- Evaluate only promising candidates
- Keep edits simple and concrete
