---
name: structured-search-playbook
description: Playbook for escaping C5 local optima via structured candidate generation.
---

# C5 Optimization: Structured Search Playbook

## Problem: Local Optima Traps

The seed's Adam optimizer with 12 initializations converges to ~0.999641 combined_score.
This is a local optimum. Gradient-based methods from similar starts cannot escape.

## Solution: Structurally Diverse Generation

### Step 1: Generate Diverse Candidates

Use struct_generate_candidates to create programs with DIFFERENT mathematical structures:

- **Pure step functions**: h=1 on [0,1], h=0 elsewhere (integral=1 by construction)
- **Sinusoidal mixtures**: sin/cos combinations with sigmoid activation
- **Piecewise constant**: 3-5 segments with optimized heights
- **Genetic algorithm**: Population-based search with crossover/mutation
- **Simulated annealing**: Metropolis-Hastings-style optimization

### Step 2: Evaluate and Select

- Evaluate each candidate with evaluate_solution
- Select the 2-3 highest-scoring candidates
- Analyze which ansatz family performed best

### Step 3: Refine the Winner

- Keep the successful ansatz structure
- Optimize hyperparameters: num_intervals, learning_rate, penalty_strength
- Add small variations or alternative initializations

### Step 4: Constraint Enforcement

Always ensure integral of h equals 1:
- Pre-normalize in the ansatz construction
- Post-normalize before evaluation

## Key Insights

- The seed's 12 patterns all use sigmoid-softmax latent - try fundamentally different structures
- Step functions (few breakpoints) may find better optima with less flexibility
- Non-gradient methods explore the space differently than Adam
- The objective landscape likely has multiple disconnected basins

## Success Criteria

- combined_score > 1.0 means c5_bound < 0.38092303510845016
- Focus on STRUCTURAL diversity, not hyperparameter tuning alone
