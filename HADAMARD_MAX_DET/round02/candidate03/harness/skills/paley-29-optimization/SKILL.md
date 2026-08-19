---
name: paley-29-optimization
description: Task-specific skill for n=29 Paley construction optimization with numpy-based checkpoints and time management
---

# Paley-29 Optimization Skill

## Critical: n=29 is PRIME and n mod 4 equals 3

This is the EXACT scenario where Paley construction works optimally. Do NOT try random constructions or cyclic shifts as primary method.

## Quadratic Residues mod 29 (MEMORIZE THESE)

Quadratic residues (squares): {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
Legendre symbol (a|29) = 1 if a in residues above, -1 if not in residues and a not equal 0

## Paley Construction Formula

H[i][j] = 1 if (i-j) mod 29 in {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
H[i][j] = -1 otherwise

## Optimization Parameters (DO NOT CHANGE UNLESS SCORE PLATEAUS)

- Hill climbing iterations: 20000-25000 per restart
- Initial temperature: T = 3.0
- Decay rate: decay_rate = 0.00003
- Number of restarts: 3-5 seeds
- Seeds to try: [42, 123, 456, 789, 1000]
- Checkpoints: Every 5000 iterations using NUMPY DET (NOT Bareiss!)

## Time Budget (CRITICAL)

- Total time per evaluation: less than or equal to 150 seconds
- If time < 60s, reduce iterations or skip remaining restarts
- Always use numpy-based det at t=0,5000,10000,15000,20000
- If numpy det shows no improvement after 15000 iterations, terminate early

## Search Strategy

1. Build Paley matrix with correct residues
2. Run hill climb with T=3.0*exp(-0.00003*t) for 20000 iterations
3. Use numpy-based det checkpoint at t=0,5000,10000,15000,20000
4. Repeat for 3-5 different seeds
5. Return best result across all restarts
6. Call probe_solution with 2-3 final variants to rank
7. Call evaluate_solution ONCE with your best variant

## NumPy-Based Checkpointing

- During hill climbing: use np.linalg.det(current_matrix) every 5000 iterations
- This is FAST and DOES NOT consume eval/probe budget
- Bareiss is for final evaluation only
