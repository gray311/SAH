---
name: discovery-optimization
description: "Constrained numerical optimization for continuous functions. Focus on hyperparameter tuning,\ninitialization diversity, and optimizer modifications while PRESERVING sigmoid enforcement\nand penalty-based constraint satisfaction. Small, targeted edits only."
---

# Constrained Optimization Harness

## Core Principle
This task finds a step function h: [0, 2] → [0, 1] minimizing overlap integrals.
The seed uses sigmoid(latent) for bounds and penalty terms for ∫h=1.0.
**NEVER break these** - they're non-negotiable for validity.

## Editing Guidelines
1. **Hyperparameter tuning**: Adjust base_learning_rate (try 0.001-0.01), num_steps (30000-80000),
   penalty_strength (500-2000), num_intervals (200-1000)

2. **Initialization variants**: Try different _get_best_initialization patterns or add new ones
   (triangular waves, piecewise constant, multi-frequency sinusoidal)

3. **Optimizer changes**: Try optax.adamw, optaxrmsprop, or lr schedules instead of fixed adam

4. **Restart strategy**: Modify num_restarts or seed cycling logic

5. **DO NOT touch**: sigmoid activation, penalty structure, FFT computation, integral formula

## Process
1. Read current EVOLVE-BLOCK carefully - identify which params to tune
2. Choose ONE change: a specific hyperparameter value or small structural tweak
3. Use SEARCH/REPLACE to modify only that part
4. Evaluate and score. If validity=0, the edit broke constraints - revert and try different param
5. If score < best_so_far, abandon this direction - try another parameter space
6. Track which params work: combine successful ideas

## Common Pitfalls
- Replacing sigmoid with tanh/softmax (breaks [0,1] constraint)
- Removing penalty_strength=XXX (integral constraint violated)
- Changing h = sigmoid(...) to direct assignment (values can be <0 or >1)
- Rewriting _compute_c5_bound incorrectly (invalidates the scoring)

## Scoring
- combined_score > 1.0 means beating the record (0.3809...)
- closer to 1.0 from below means worse
- seed = 0.999641 is already very good - beat it, don't just match
