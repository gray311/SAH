---
name: discovery-optimization
description: "Maximize |det(H)| for 29x29 +/-1 matrix. Fix the flawed Paley construction in the seed. Use correct Legendre symbol approach, then extensive hill climbing with many restarts. Probe variants before evaluating."
---

# Correct Hadamard-like Matrix Construction for n=29

## THE BUG IN THE SEED PROGRAM
The seed's Paley construction is INCORRECT. It doesn't use the proper Legendre symbol.
We MUST fix this first.

## Method 1: CORRECT Paley Construction with Legendre Symbol
For n=29 (prime, n congruent to 3 mod 4):
- Quadratic residues mod 29: 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28
- For entry (i,j): compute a = (i - j) mod 29
- If a is in quadratic residues: H[i][j] = +1
- If a is NOT in quadratic residues: H[i][j] = -1
- Ensure diagonal H[i][i] = +1 (when a=0, treat as residue)

PSEUDO-CODE for correct Paley:
residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
for i in range(29):
  for j in range(29):
    offset = (i - j) % 29
    H[i][j] = 1 if offset in residues else -1

## Method 2: Improved Hill Climbing (after correct construction)
- Start from the CORRECT Paley matrix (not the buggy seed version)
- 15000-20000 iterations per run (NOT 10000)
- Better cooling: T starts at 3.0, cool_rate = 0.9985
- Accept improving moves unconditionally
- Accept worsening moves with prob exp((|new| - |old|) / max(1, T))
- Use seeds: 0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500

## Method 3: Random perturbations from correct Paley
- Take correct Paley matrix
- Flip 5-10 random entries to create variation
- Run hill climbing from this perturbed start

## Method 4: Cyclic structure search
- Start from correct Paley
- Try cyclically shifting columns by small amounts
- Evaluate with probe, keep best

## Workflow
1. IMPLEMENT the CORRECT Paley construction (FIX THE BUG!)
2. Run 15 independent hill climbing trials from correct Paley
3. Each trial: 18000 iterations, proper annealing
4. Use probe_solution to quickly compare top 3 trials
5. Evaluate only the probe winner with evaluate_solution
6. If score improves, try further perturbations
7. Finish when no improvement or budget exhausted

## Timing constraints
- Total per-eval time: less than 180 seconds
- Paley construction: less than 0.5 seconds
- Hill climbing: 120-150 seconds
- Keep iterations high but time-bounded

## Why this works
The seed's Paley construction was mathematically incorrect. The correct Legendre symbol approach
produces a starting matrix much closer to optimal. Combined with longer hill climbing and more
restarts, this should find significantly better solutions.

## Tools reminder
- edit_solution: Rewrite the EVOLVE-BLOCK with CORRECT code
- probe_solution: Test 3-5 variants before full eval
- evaluate_solution: Final scoring (budget: 20)
- finish: Submit best solution
