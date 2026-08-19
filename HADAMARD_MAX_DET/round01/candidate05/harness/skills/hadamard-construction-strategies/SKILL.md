---
name: hadamard-construction-strategies
description: Specialized playbook for Hadamard matrix construction. Focus on combinatorial methods (Paley, quadratic residues, block constructions) rather than local search. Use probe_solution for rapid variant ranking. Always aim for internal runtime < 350s with safety margin.
---

# Hadamard Construction Strategies Playbook

## Problem
Build a 29×29 matrix with entries ±1 to maximize |det(H)|.

## Key Methods
### 1. Paley Construction (p = 29, p ≡ 1 mod 4)
H[i][j] = 1 if (i-j) mod 29 is a quadratic residue, else -1
QR mod 29: {1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}

### 2. Modified Paley with Offset
Vary the quadratic residue set: QR + k mod 29 for different k

### 3. Multiple Random Restarts
Run hill-climbing from 3-5 different random seeds
Keep the best result

### 4. Block-Based Construction
Split 29 into blocks, construct small Hadamard blocks, combine

## Probing Strategy (CRITICAL)
1. Edit with Method A
2. probe_solution → score_A
3. Edit with Method B
4. probe_solution → score_B
5. ... repeat for 3-5 methods
6. evaluate_solution on best probed variant

## Internal Search Budget
- Hill climbing iterations: ≤ 1500 (not 2000, leave margin)
- Total runtime: ≤ 300s (not 350s, leave safety margin)
- Use bareiss() for exact det, not numpy.linalg.det

## What NOT to Do
- Don't just tune hill-clamping parameters alone
- Don't do only one full evaluation
- Don't ignore probe results
- Don't exceed time limit
