---
name: hyperparameter-refinement
description: After finding promising patterns, refine with targeted hyperparameter search.
---

# Hyperparameter Refinement for Erdos C5

## When to Use

After smart_pattern_generator + evaluate_solution finds c5_bound < 0.380923.

## Systematic Refinement

1. Take best candidate's h from pattern generation
2. Slightly perturb h (10% noise) and train for 30000 steps
3. Evaluate if improved
4. If yes, train longer (59000 or 100000 steps)
5. Track best combined_score

## Key Insight

Analytical patterns give good starting points. Gradient training can
refine them, but starting from better initializations yields faster
progress.
