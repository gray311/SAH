---
name: diversity-construction-strategy
description: Specialized skill for testing multiple base constructions (Paley+perturbation, random, etc.) in parallel per evaluation. Use to escape local optima in Hadamard optimization.
---

# Diversity Construction Strategy for Hadamard Optimization

## Why Multiple Constructions?
The seed achieves 0.545692. Current harness best is 0.561608 - barely better.
This indicates the SA search on a SINGLE deterministic base (Paley) is stuck.
SOLUTION: Test MULTIPLE different base constructions per evaluation.

## Base Construction Strategies

### Strategy 1: Paley + Random Perturbation
Start with Paley construction, then randomly flip 5-15% of elements
Then run SA from this perturbed base

### Strategy 2: Pure Random Initialization
Start with a random ±1 matrix, then run SA from scratch

### Strategy 3: Paley + Targeted Perturbation
Start with Paley, identify elements with lowest contribution to determinant
Flip those elements to explore different search landscapes

## Parallel Evaluation Workflow

### Per Evaluation (20 total):
1. Choose: perturbation_fraction (0.05, 0.10, 0.15)
2. Choose: perturbation_seed (0, 100, 200, 300, 400)
3. Choose: seed_range (0-500, 500-1000, 1000-1500, 4000-4500, 8000-8500)
4. Choose: SA params (iterations, T, cool_rate)

### Run 5 strategies in parallel:
- Strategy A: Paley + perturbation_fraction A
- Strategy B: Paley + perturbation_fraction B
- Strategy C: Random initialization
- Strategy D: Paley + perturbation_fraction C
- Strategy E: Random initialization with different seed

### Use PROBE to test 2-3 strategies quickly (500 iterations each)
### Use FULL evaluation on the BEST strategy
### Track which base construction works best

## Critical Rules
- NEVER use only ONE construction strategy per evaluation
- ALWAYS test at least 3 different base constructions
- VARY perturbation_seed between evaluations (don't reuse 4000-4499)
- Use numpy.linalg.det for all determinant calculations (fast)
- If all strategies fail, try RANDOM initialization exclusively
- Remember: 20 evals is enough to thoroughly explore construction diversity
