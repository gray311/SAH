---
name: multi-start-hadamard
description: Specialized skill for n=29 Hadamard optimization using multi-start search. Must try at least 3 different construction methods per evaluation.
---

# Multi-Start Hadamard Optimization for n=29

## Core Principle: DIVERSITY of Starting Points

The seed uses only Paley construction with 500 seeds. This may be stuck in a local optimum.
You MUST explore MULTIPLE fundamentally different construction methods.

## Required: At Least 3 Construction Methods

For EACH evaluation, implement at least 3 different starting matrices:

### Method A: Random Initialization
Start with random ±1 matrix, then apply SA.

### Method B: Paley Construction
Use quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}

### Method C: Greedy Construction
Build matrix entry by entry to maximize orthogonality

## Recommended Workflow

1. Generate 3-5 different starting matrices using different construction methods
2. For each starting matrix, run SA with 20-30 seeds, 15-20k iterations
3. Track the BEST matrix across all runs
4. Use different SA parameters for each run:
   - Run 1 (random): T=10, cool=0.995, 20k iters
   - Run 2 (Paley): T=5, cool=0.998, 15k iters
   - Run 3 (greedy): T=15, cool=0.993, 25k iters
5. Return only the BEST result from all runs

## Determinant Strategy
- Use numpy.linalg.det for ALL scoring (fast ~0.001s)
- NEVER use Bareiss during hill climbing

## Budget Management
- Time per eval: < 250 seconds
- If one method takes > 60 seconds, reduce iterations

## Critical Checkpoints
- Implement at least 3 DIFFERENT construction methods
- Run 3-5 independent SA searches from different starts
- Return the BEST result across all searches
