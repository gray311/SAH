---
name: discovery-optimization
description: "Hadamard matrix optimizer for n=29. Experiment with MULTIPLE construction methods (random, Paley, greedy) with diverse starting points. Run 3-5 independent searches per eval. Use numpy.det for fast scoring."
---

# Hadamard Matrix Optimization - Multiple Construction Strategies

## Objective: Maximize |det(H)| for 29×29 ±1 matrix

## CRITICAL: Explore DIFFERENT CONSTRUCTIONS, Not Just Parameter Tuning

The seed uses Paley construction, which may be stuck in a local optimum. You MUST try:

### Method 1: RANDOM INITIALIZATION + SA
- Start with random ±1 matrix
- SA: 20-30 seeds, 20k iterations each
- Parameters: T=10, cool_rate=0.995

### Method 2: PALEY CONSTRUCTION (with variations)
- Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- VARIATIONS to try: add random entries, flip 10-20 random entries, use different SA parameters

### Method 3: GREEDY CONSTRUCTION
- Start with identity or simple pattern
- For each position, greedily choose ±1 to maximize |det| with previous rows
- Then refine with SA

### Method 4: MULTI-START STRATEGY (RECOMMENDED)
Run 3-5 independent searches from DIFFERENT starting points:
- Run A: Random initialization, 20 seeds, 20k iters, T=10, cool=0.995
- Run B: Paley-based, 20 seeds, 20k iters, T=5, cool=0.998
- Run C: Greedy construction, 10 seeds, 15k iters
- Run D: Mixed approach

Take the BEST result across all runs.

## Determinant Strategy
- ALWAYS use numpy.linalg.det (fast, ~0.001s per 29×29 matrix)
- NEVER use Bareiss during hill climbing (causes timeout)

## Budget Management
- Time per evaluation: < 250 seconds
- If any approach takes > 80 seconds, reduce iterations

## Critical Rules
- MUST try MULTIPLE starting constructions (not just one)
- Paley residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- Use numpy.linalg.det for ALL scoring
- Total seeds per eval: 15-50 (not 500 from single start)
- Time budget: < 250 seconds per eval
