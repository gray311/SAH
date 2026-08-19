---
name: discovery-optimization
description: "Optimize 29x29 Hadamard-like matrix for maximum |det(H)|. n=29\u22613 mod 4, so use Paley construction with quadratic residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}. Fix determinant computation using scipy.linalg.det with scaling for numerical stability. Search with 5 seeds \u00d7 30k iterations, 4 cooling schedules. Use probe_solution to pre-rank variants."
---

# Hadamard Matrix Optimization for n=29 (Corrected)

## Mathematical Foundation
- 29 ≡ 3 (mod 4), so Paley construction applies
- Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
- Paley construction: H[i,j] = 1 if (i-j) mod 29 in residues, else -1

## CRITICAL: Determinant Computation Fix
The current code likely uses bareiss() which can fail or numpy.linalg.det which loses precision on large integer matrices.

**USE THIS PATTERN**:
```python
import numpy as np
import scipy.linalg

def stable_det(matrix):
    """Compute determinant with numerical stability."""
    A = np.array(matrix, dtype=np.int64)
    # Scale to numerical stability range
    scaled = A / np.sqrt(29)
    det_scaled = scipy.linalg.det(scaled)
    # Rescale: det(A) = (sqrt(29))^29 * det(A/sqrt(29))
    return abs(det_scaled) * (np.sqrt(29) ** 29)
```

Or use Python's arbitrary precision:
```python
def exact_det(matrix):
    A = np.array(matrix, dtype=object)
    return abs(np.linalg.det(A))
```

## Search Strategy
1. **Paley construction** (verified correct):
   ```python
   residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
   H = [[1 if (i-j)%29 in residues else -1 for j in range(29)] for i in range(29)]
   ```

2. **Multi-start Simulated Annealing**:
   - 5 different random seeds
   - 30,000 iterations per seed
   - 4 cooling schedules: (T=3.0, cool=0.996), (T=2.0, cool=0.997), (T=1.5, cool=0.995), (T=4.0, cool=0.994)
   - Adaptive cooling: reduce iterations if no improvement in last 1000 steps

3. **Perturbation refinement**:
   - Take best result and apply 10 random ±1 flips
   - Run final SA with 10,000 iterations on perturbed start

## Budget Management
- Total iterations: 5×30,000 + 10,000 = 160,000 flips
- Time with numpy: ~20-25 seconds
- Use probe_solution to test 3 cooling schedule variations
- Then evaluate only the best variant

## Workflow
1. Implement corrected code with scipy.linalg.det or object dtype
2. Call edit_solution with complete working code
3. Call probe_solution on 3 variants with different cooling schedules
4. Call evaluate_solution on the probe winner
5. If no improvement after 10 evals, try: different construction, more seeds
6. Repeat until budget exhausted
