---
name: multi-chain-hadamard
description: Specialized skill for multi-chain Hadamard optimization on n=29.  Run 6 parallel SA chains per eval - 3 perturbed Paley, 2 random, 1 baseline. Use numpy.det for all calculations. Probe before evaluate.
---

# Multi-Chain Hadamard Optimization for n=29

## Core Insight
Single-seed SA gets trapped. Solution: run 6 parallel chains per evaluation
starting from diverse initial matrices.

## The 6 Chains Strategy

### Chains 1-3: Perturbed Paley (primary search)
Start from exact Paley construction, then flip:
- Chain 1: flip 5 random entries
- Chain 2: flip 10 random entries  
- Chain 3: flip 15 random entries

Paley residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = 1 if (i-j) mod 29 in residues else -1

### Chain 4: Moderate Random Start
Initialize with random ±1 matrix
Parameters: T=5.0, iterations=2000, cool_rate=0.997

### Chain 5: Aggressive Random Start
Initialize with random ±1 matrix
Parameters: T=15.0, iterations=2000, cool_rate=0.998

### Chain 6: Original Paley (baseline)
Parameters: T=3.0, iterations=2000, cool_rate=0.997

## Total Budget Analysis
- 6 chains × 2000 iterations = 12,000 total iterations
- numpy.linalg.det on 29×29: ~0.001s each
- Total time: ~12 seconds (well under 350s budget)
- Per-eval search coverage: 6 different regions of matrix space

## Determinant Strategy
- ALWAYS use numpy.linalg.det for search
- NEVER use Bareiss during hill climbing (causes timeout)
- Track best determinant across ALL 6 chains
- Return the matrix achieving the best determinant

## Workflow
1. Implement construct_paley_matrix(n, residues)
2. Implement perturbation functions (flip specified number of entries)
3. Implement random matrix initialization
4. Implement sa_run(start_matrix, T, iterations, cool_rate, seed)
5. Generate 6 starting matrices
6. Run 6 parallel SA chains
7. Collect results, return best matrix

## Critical Rules
- PALEY RESIDUES: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- EXACTLY 6 chains per evaluation
- Use numpy.linalg.det for ALL determinants
- Track global best across all chains
- Random seeds: use different seed for each chain
- Total iterations per eval ≤ 15,000
- Test with probe_solution before full evaluation

## Why This Beats Parameter Sweeping
- Parameter sweeps on single seed: explore SAME region, different depth/temperature
- Multi-chain: explore 6 DIFFERENT regions simultaneously
- Much higher chance of escaping deep local optima
- Computational cost is similar (6 chains is still fast)
