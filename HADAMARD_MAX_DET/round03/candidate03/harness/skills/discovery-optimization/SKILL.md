---
name: discovery-optimization
description: "Optimize 29x29 \u00b11 matrix for max |det(H)|. n=29\u22613(mod 4) allows Paley construction.\nCore issue: Single-phase SA gets stuck in local optima.\nSolution: Multi-phase strategy: (1) Paley+SA with 3 cooling schedules, (2) Local refinement of best, (3) Random seeds. Use numpy det always. 7 seeds, ~200k flips, probe before eval."
---

# 29x29 Hadamard-like Matrix Optimization

## Mathematical Context
n=29 ≡ 3 (mod 4). Paley construction creates near-optimal Hadamard-like matrices.
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
Paley rule: H[i][j] = 1 if (i-j) mod 29 in residues, else -1.

## Why Seed Fails
Single-phase simulated annealing from Paley matrix gets trapped in local optima.
The seed only tries 5 seeds with similar cooling schedules.

## Multi-Phase Search Strategy

### Phase 1: Diverse Starting Points + Multiple Cooling Schedules
Run SA from 3 different starting configurations:
- Start A: Paley matrix with T=10.0, cool_rate=0.999, 40000 iterations
- Start B: Paley matrix with T=5.0, cool_rate=0.997, 40000 iterations  
- Start C: Paley matrix with T=3.0, cool_rate=0.996, 40000 iterations
- Start D: Random ±1 matrix with T=8.0, cool_rate=0.998, 20000 iterations
- Start E: Random ±1 matrix with T=5.0, cool_rate=0.996, 20000 iterations
- Start F: Best from Phase 1, perturbed 50 random entries, T=15, cool=0.9995, 15000 iters
- Start G: Best from Phase 1, perturbed 100 random entries, T=20, cool=0.999, 10000 iters

### Phase 2: Intensive Local Refinement
Take the top 3 candidates from Phase 1. For each:
- Run focused SA: 2000 iterations, T=100.0 (very slow cooling), cool_rate=0.9999
- Then: 100 random single-flip explorations
- Keep best across all 3 refinements

### Phase 3: Cross-Matrix Recombination (Optional, if time permits)
- Take rows from top 3 candidates, randomly swap between them
- Run brief SA (1000 iters, T=50, cool=0.9995) on recombined matrices

## Implementation Requirements
1. Use numpy.linalg.det for ALL determinant calculations during search
2. Implement exactly 7+ starting seeds with the parameters above
3. Track best determinant across ALL phases
4. Wrap in try-except with timeout guard (max 180s per evaluation)
5. Return only the BEST matrix found, not all candidates

## Probe Strategy
Before evaluate_solution:
- Probe variant 1: T=10.0, cool=0.999, 40000 iters from Paley
- Probe variant 2: Random start, T=8.0, cool=0.998, 20000 iters
- Evaluate the winner of these probes

## Common Errors to Avoid
- ❌ Using Bareiss during search (causes timeout)
- ❌ Only 1-2 cooling schedules
- ❌ Only Paley start (needs random starts too)
- ❌ Not refining top candidates further
- ❌ Running too few iterations (<30000 per seed)
- ❌ Forgetting to track global best across all phases
