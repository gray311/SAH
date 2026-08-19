---
name: discovery-optimization
description: "Random initialization + aggressive SA for n=29. 100k iters, temp=20.0, cool=0.9995. Use numpy det. Time < 350s."
---

# Random Initialization + Aggressive Simulated Annealing for n=29

## CRITICAL CHANGE FROM SEED
The seed uses Paley construction which is deterministic and produces a local optimum. You MUST use RANDOM initialization.

## Algorithm
1. Create 29x29 matrix with random ±1 entries (use random.randint(0,2)*2-1)
2. Define det_func: return abs(np.linalg.det(matrix.astype(float)))
3. Simulated annealing loop:
   - T = 20.0 (aggressive start)
   - cool_rate = 0.9995 (slow cooling for exploration)
   - iterations = 100,000
   - Randomly flip one entry per iteration
   - Accept if better, or with prob exp(delta/T)
   - Track best matrix and its determinant
4. Return best matrix

## Why Random Initialization?
Paley construction produces a specific structure. Random initialization explores completely different regions of the solution space.

## Time Budget
- 100,000 iterations × 0.001s/det ≈ 100s
- Python overhead ≈ 50s
- Total ≈ 150s (well under 350s)

## Implementation Notes
- Import random, numpy
- Use random.seed(42) for reproducibility in the code
- Use numpy.linalg.det (fast, numerical)
- DO NOT use Bareiss (too slow)
- DO NOT use Paley construction
- Return the matrix (not the determinant)

## Expected Score Improvement
Random initialization + 100k iters should find matrices with higher determinant than the Paley seed (det ≈ 319.83, normalized score 0.531724).
