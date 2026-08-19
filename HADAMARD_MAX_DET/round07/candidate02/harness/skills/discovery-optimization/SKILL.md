---
name: discovery-optimization
description: "Hadamard n=29 optimizer. Key: diversify starting matrices (perturbed Paley + random) across multiple SA chains per eval. Use probe before evaluate."
---

# Hadamard n=29 - Diverse Search Strategy

## Problem
n=29 ≡ 3 mod 4. True Hadamard doesn't exist, find best ±1 matrix.

## Why SA from single seed fails
- Paley construction is mathematically "good" but creates a narrow basin of attraction
- SA with fixed parameters gets trapped in local optimum (seed score 0.545)
- Parameter sweeps don't help because the BASE construction limits escape

## Solution: Diversified Multi-Chain Search

### Per Evaluation, Run 6 Parallel SA Chains:

#### Chain 1-3: Perturbed Paley (most promising)
- Start with correct Paley matrix from residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- Randomly FLIP 5, 10, and 15 entries respectively
- This explores "nearby" solutions while keeping structural advantages

#### Chain 4: Moderate Random
- Initialize with random ±1 matrix
- Run SA with T=5.0, 2000 iterations, cool=0.995

#### Chain 5: Aggressive Random  
- Initialize with random ±1 matrix
- Run SA with T=15.0, 2000 iterations, cool=0.998 (higher T for escape)

#### Chain 6: Original Paley (baseline)
- Run from exact Paley with T=3.0, 2000 iterations, cool=0.997

### Parameters for Each Chain:
- Iterations per chain: 2000 (total 12000 across 6 chains)
- Temperature: 3.0, 5.0, 15.0 (different for different chains)
- Cooling: 0.995, 0.997, 0.998
- Random seed: Use different seeds for each chain

### Determinant Strategy
- ALWAYS use numpy.linalg.det for search
- Run all 6 chains in parallel (total ~12s, well under 350s)
- Track best matrix across ALL 6 chains
- Return that best matrix

### Workflow
1. Call edit_solution with code implementing 6 parallel chains
2. Call probe_solution to quickly test if this strategy beats seed
3. If probe shows improvement, call evaluate_solution for full run
4. If no improvement, try: more perturbations, different T values, more chains
5. Continue until budget (20 evals) or clear plateau

## Critical Rules
- PALEY RESIDUES MUST BE EXACT: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- Run at least 6 parallel SA chains per evaluation
- Include perturbed versions of Paley (flip 5, 10, 15 entries)
- Include at least 2 random initializations
- Use numpy.linalg.det for ALL search iterations
- Total iterations ≤ 15000 per eval (easily under time budget)
- Track and return the BEST matrix across all 6 chains

## Expected Outcome
By exploring 6 different regions of matrix space per evaluation, you're far more likely to escape the seed's local optimum than sweeping parameters on a single chain.
