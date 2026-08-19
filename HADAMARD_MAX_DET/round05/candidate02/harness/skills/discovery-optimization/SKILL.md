---
name: discovery-optimization
description: "Hadamard optimizer for n=29. Use generate_paley_variants to get 5 pre-validated matrices.\nRun SA on each (5k iters), pick top 2, extend each (20k iters). Evaluate best.\nAlways probe variants with different seeds before evaluating. Use numpy.linalg.det exclusively."
---

# Hadamard Matrix Optimization for n=29

## Step 1: Generate Variants
Call generate_paley_variants() to get 5 matrices with seeds: 42, 123, 456, 789, 2024.
These use correct Paley construction with residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.

## Step 2: Initial Search (5,000 iterations each)
For each of the 5 variants:
- Run simulated annealing: T=10.0, cool_rate=0.998, 5000 iterations
- Use numpy.linalg.det for all score computations
- Track best determinant

## Step 3: Extended Search (top 2 variants only)
From the 5 results, pick the 2 with highest det:
- Run 20,000 iterations each with T=3.0, cool_rate=0.997
- Keep track of best overall

## Step 4: Final Evaluation
Call evaluate_solution on the single best variant from Step 3.

## Critical Rules
- NEVER implement Paley construction manually (prone to errors)
- NEVER use Bareiss during hill climbing (causes timeout)
- ALWAYS use numpy.linalg.det
- Total iterations: 5×5000 + 2×20000 = 90,000 (safe for 350s)
- If score doesn't improve, try different seeds with generate_paley_variants
