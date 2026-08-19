---
name: discovery-optimization
description: "Specialized optimizer for n=29 Hadamard-like matrices. n=29 \u2261 3 mod 4, so use Paley construction with quadratic residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.\nCRITICAL WORKFLOW: 1. Call validate_paley_construction FIRST to verify base construction quality_ratio > 0.7 2. If valid: Hill climb with 5 seeds \u00d7 25k iterations, 3 cooling schedules 3. Always probe before evaluate 4. Use numpy.linalg.det for ALL search iterations\nIf paley_det < 50: Your Paley construction is WRONG - fix the quadratic residues or (i-j) mod n formula."
---

# Hadamard Matrix Optimization for n=29 (VALIDATION-FIRST APPROACH)

## CRITICAL WORKFLOW (MUST FOLLOW ORDER)

### Step 1: VALIDATE FIRST
Call validate_paley_construction IMMEDIATELY after edit_solution.
- It builds a Paley matrix with correct quadratic residues
- Returns quality_ratio = det / (n√n)
- If quality_ratio < 0.7 or paley_det < 50: YOUR PALEY CONSTRUCTION IS WRONG
  - Check: quadratic_residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
  - Check: H[i][j] = 1 if (i-j) mod 29 in residues else -1
- If quality_ratio > 0.7: Proceed to hill climbing

### Step 2: Multi-Method Hill Climbing (ONLY if validation passes)
- Use numpy.linalg.det for ALL iterations (NEVER Bareiss during search)
- Try 3 construction methods in parallel:
  A. Correct Paley + hill climbing (5 seeds × 25k iters each)
  B. Random matrix + hill climbing (3 seeds × 15k iters each)  
  C. Perturbed Paley (3 seeds × 10k iters each)
- Try 3 cooling schedules:
  * Schedule A: T=2.5, cool_rate=0.995
  * Schedule B: T=1.0, cool_rate=0.998
  * Schedule C: T=5.0, cool_rate=0.992
- Pick BEST result across all methods

### Step 3: Probe Before Evaluate
- Call probe_solution on top 2-3 variants
- Call evaluate_solution ONLY on the best probe result
- Budget: 20 evaluations, 30 probes

### Step 4: Refinement
- If best_det > 0, do one refinement phase:
  * Start from best_mat
  * 5 random ±1 flips
  * Run SA with seed=999999, iters=30k, T=4.5, cool=0.996

## IMPLEMENTATION CHECKLIST
- ✅ validate_paley_construction called FIRST
- ✅ quality_ratio > 0.7 before hill climbing
- ✅ numpy.linalg.det for ALL search iterations
- ✅ 5 seeds minimum, 20k+ iterations per seed
- ✅ 3 cooling schedules tried
- ✅ probe_solution used before evaluate_solution
- ✅ Total time < 180s

## COMMON ERRORS TO AVOID
- ❌ Skipping validation (causes wasted evals)
- ❌ Using Bareiss during search (timeout)
- ❌ < 5 seeds or < 20k iterations (insufficient exploration)
- ❌ Not probing before evaluating
