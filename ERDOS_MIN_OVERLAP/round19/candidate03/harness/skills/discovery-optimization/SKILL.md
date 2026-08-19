---
name: discovery-optimization
description: "Edit hyperparameters and optimization parameters in the ErdosOptimizer.\nFocus on valid Python edits that can be tested with evaluate_solution."
---

# Hyperparameter Search Strategy for Erdos Optimization

## Direct Editing Approach

The solver should EDIT the EVOLVE-BLOCK to change hyperparameters.
Focus on these fields in the Hyperparameters class:

- num_intervals: Resolution of discretization (current: 800)
- base_learning_rate: Learning rate (current: 0.0062)
- num_steps: Total optimization steps (current: 59000)
- penalty_strength: Constraint enforcement (current: 61.0)
- num_restarts: Number of random restarts (current: 3)

## Search Strategy

1. Change ONE parameter at a time
2. Test with evaluate_solution
3. If no improvement, try next parameter value
4. Track which changes help

## Recommended Value Ranges

- num_intervals: 400-1200
- base_learning_rate: 0.002-0.015
- num_steps: 20000-80000
- penalty_strength: 20-200
- num_restarts: 5-12

## Initialization Patterns

The seed program has _get_best_initialization with 15 patterns.
You can modify these patterns to create different initializations.

Key patterns to adjust:
- Threshold patterns (Patterns 5, 6, 8, 9, 10, 11)
- Bipartite (Pattern 13)
- Tri-modal (Pattern 14)
- Golomb ruler (Pattern 12)

## Workflow

1. Pick ONE hyperparameter to change
2. Make a small edit to the EVOLVE-BLOCK
3. Call evaluate_solution
4. If score improves, explore nearby values
5. If score doesn't improve, try different parameter
6. Repeat until budget exhausted or improvement found

## Example Edit

Change num_restarts from 3 to 5:

```python
num_restarts: int = 5
```

## Tools Available

- edit_solution: Edit the EVOLVE-BLOCK
- evaluate_solution: Full evaluation (59000 steps)
- probe_solution: Approximate evaluation (use before full eval)
- finish: Submit final result

## Important

- Keep Python syntax valid
- Only change one parameter at a time
- Track which edits work
