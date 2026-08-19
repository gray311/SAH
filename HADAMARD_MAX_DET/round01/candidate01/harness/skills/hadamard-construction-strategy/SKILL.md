---
name: hadamard-construction-strategy
description: Concrete strategies for constructing near-Hadamard matrices when n=29 (not 4k). Use probe_solution to rank variants, then evaluate_solution for promising ones. Call analyze_hadamard_construction at the start of each iteration to diagnose current strategy.
---

# Hadamard Construction Strategies for n=29

## Background
- Perfect Hadamard matrices only exist for n=1,2,4k. For n=29, we need near-Hadamard.
- Maximal |det| for n=29 is conjectured around 2^29 ≈ 5.36×10^8, but achievable |det| is likely 10^14-10^17.

## Strategy 1: Paley Construction with Quadratic Residues
- For prime p=29 (≡1 mod 4), use QR mod 29:
  QR = {1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- Construct: H[i,j] = 1 if (i-j mod 29) in QR, else -1
- May need additional randomization or local optimization

## Strategy 2: Random Initialization + Local Search
- Start with random ±1 matrix
- Apply hill climbing: flip entry (i,j) if |det| increases
- Use simulated annealing to escape local optima
- Typical iterations: 5000-10000 (within 350s budget)

## Strategy 3: Hybrid Structured + Optimization
- Start with Paley/QR construction (good structural seed)
- Apply local search with moderate iterations
- More efficient than pure random search

## Strategy 4: Multiple Seeds Evaluation
- Try 3-5 different random seeds with same construction
- Use probe_solution to quickly rank seeds
- Evaluate only top 2-3 with full score

## Strategy 5: Exterior Product / Kronecker Construction
- Use known Hadamard matrices of order 28 (if available)
- Extend to 29 with careful augmentation
- May require modification for exact dimensions

## Probing Strategy
- For each construction variant:
  1. Call probe_solution to get approximate score
  2. If probe_score < 0.3 * baseline, abandon
  3. If probe_score in [0.3, 0.8] * baseline, consider full eval
  4. If probe_score > baseline, evaluate immediately

## Iteration Pattern
- Iteration 1: Probe baseline (Paley construction)
- Iteration 2-4: Probe variations (different seeds, temp0 values)
- Iteration 5: Evaluate best probe candidate
- Iteration 6-10: Refine with local changes, probe each
- Iteration 11+: Evaluate new strategies if probes look promising

## Time Budget Discipline
- Full eval: 350s max. If your code has loops >1000 iterations, TLE risk.
- Use probe_solution to validate approach before committing to full eval.
- If probe shows <20% improvement over seed, try fundamentally different construction.
