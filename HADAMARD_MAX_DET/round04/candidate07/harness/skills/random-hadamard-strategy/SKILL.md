---
name: random-hadamard-strategy
description: Use random initialization instead of Paley. 100k iterations with temp=20.0, cool=0.9995. numpy det only.
---

# Random Hadamard Strategy for n=29

## KEY INSIGHT: Random beats Paley for this task
The seed's Paley construction produces a local optimum (det ≈ 319.83). Random initialization explores different regions of the ±1 matrix space.

## IMPLEMENTATION
1. **Random Initialization**: Create 29x29 matrix with random ±1 entries
   ```python
   matrix = [[random.randint(0,2)*2-1 for j in range(29)] for i in range(29)]
   ```

2. **Aggressive Simulated Annealing**:
   - Initial temperature: 20.0 (high for exploration)
   - Cooling rate: 0.9995 (slow cooling)
   - Iterations: 100,000
   - Random single-flip mutation per iteration
   - Accept improvements, sometimes accept worse with prob exp(delta/T)

3. **Determinant Calculation**:
   - Use numpy.linalg.det (fast, ~0.001s per 29x29)
   - Track the matrix with highest |det|

4. **Time Budget**:
   - 100k iters × 0.001s/det ≈ 100s
   - Python overhead ≈ 50s
   - Total ≈ 150s (< 350s limit)

## Why This Works
- Random init: Different starting point than Paley
- High temp: Escape local optima
- Slow cooling: Fine-grained search
- Many iterations: Thorough exploration

## Common Mistakes to Avoid
- ❌ Using Paley construction (same as seed)
- ❌ Using Bareiss determinant (too slow)
- ❌ Too few iterations (< 50k)
- ❌ Too low initial temp (< 10.0)
- ❌ Too fast cooling (cool_rate > 0.999)
- ❌ Not tracking best matrix during search

## Expected Outcome
Should find matrices with |det| > 319.83, giving score > 0.531724.
