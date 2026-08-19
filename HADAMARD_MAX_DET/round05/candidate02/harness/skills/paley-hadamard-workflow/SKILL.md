---
name: paley-hadamard-workflow
description: Workflow for n=29 Hadamard optimization. Use generate_paley_variants for correct Paley construction, then hill climb with numpy det. 5 base variants, 5k initial, 20k extension on top 2.
---

# Paley Hadamard Optimization Workflow for n=29

## Overview
n=29 ≡ 3 mod 4, so we use Paley construction with quadratic residues.
The generate_paley_variants tool guarantees correct implementation.

## Workflow Steps

### Step 1: Generate Base Variants
Call generate_paley_variants() once. This returns 5 matrices using seeds [42, 123, 456, 789, 2024].
Each uses the correct Paley construction:
- H[i][j] = 1 if (i-j) mod 29 ∈ {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- H[i][j] = -1 otherwise

### Step 2: Initial Hill Climbing
For each of the 5 matrices:
- Run simulated annealing: 5,000 iterations
- Parameters: T=10.0, cool_rate=0.998
- Use numpy.linalg.det for all score computations
- Track the best determinant found

### Step 3: Extended Hill Climbing
Pick the 2 best variants from Step 2:
- Run 20,000 iterations each
- Parameters: T=3.0, cool_rate=0.997
- Continue using numpy.linalg.det
- Keep the absolute best result

### Step 4: Final Evaluation
Call evaluate_solution on the single best variant.

## Critical Rules
- DO NOT implement Paley manually - use generate_paley_variants
- DO NOT use Bareiss during search (causes timeout)
- ALWAYS use numpy.linalg.det
- Total iterations: 5×5000 + 2×20000 = 90,000 (safe for 350s budget)

## Budget Management
- Time per evaluation: < 180 seconds
- numpy det on 29×29: ~0.001s
- 90,000 iterations: ~90 seconds (safe margin)
