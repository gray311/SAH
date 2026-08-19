---
name: paley-hadamard-n29
description: Specialized skill for n=29 Hadamard using ONLY correct Paley construction. 3 cooling schedules, 3 seeds, 2 escapes. Validate construction first. Total ~240s.
---

# Paley Hadamard Optimization for n=29

## Task
Maximize |det(H)| for 29×29 matrix with entries ±1.
Since 29 ≡ 3 (mod 4), use Paley construction with quadratic residues.

## PALEY CONSTRUCTION (MUST BE CORRECT)
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}

For each entry:
  diff = (i - j) % 29
  H[i][j] = 1 if diff in residues else -1

**VERIFY FIRST**: Use validate_paley_construction tool to confirm your residues are correct.

## WORKFLOW (11 searches, ~240s total)

### PHASE 1: Three Cooling Schedules (9 searches)
Run 3 COMPLETE hill-climbing searches with different schedules:

| Schedule | Temp | Cool Rate | Iterations | Goal |
|----------|------|-----------|------------|------|
| A | 8.0 | 0.995 | 5000 | Broad exploration |
| B | 3.0 | 0.997 | 15000 | Medium refinement |
| C | 1.0 | 0.998 | 20000 | Fine tuning |

For each schedule, run with 3 seeds: [42, 12345, 9998877]
Keep the BEST result across all 9 searches.

### PHASE 2: Two Targeted Escapes (2 searches)
From Phase 1 best:

1. **Escape A**: Flip 100 random positions → hill climb T=10.0, cool=0.999, iters=5000
2. **Escape B**: Flip checkerboard where (i+j)%4==0 → hill climb T=5.0, cool=0.997, iters=5000

### PHASE 3: Selection
Return matrix with highest |det|.

## IMPLEMENTATION CHECKLIST

1. ✓ Start with CORRECT Paley construction (residues verified)
2. ✓ Use numpy.linalg.det for ALL iterations (never Bareiss in search)
3. ✓ Implement exactly 3 cooling schedules with correct parameters
4. ✓ Run 3 seeds per schedule (not 4+)
5. ✓ Print progress every 5000 iterations
6. ✓ Total time <250 seconds (leaves 100s margin)
7. ✓ Use probe_solution to test schedules before full evaluation
8. ✓ Implement 2 escape patterns on best result
9. ✓ Track best_det and best_matrix across all searches

## CRITICAL CONSTRAINTS
- ONLY Paley construction (no random matrices, no perturbations during initialization)
- numpy.linalg.det for search (fast, reliable)
- Complete all 11 searches before returning
- Time budget: max 250s
- Use probe_solution to rank cooling schedules

## SAMPLE OUTPUT FORMAT
Print to stdout:
- "=== Paley Construction Validation ==="
- "Residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}"
- "Phase 1: Starting search A-1 (Schedule A, seed 42)"
- "Completed search A-1 in 3.2s, det=0.XXXXXX"
- "Phase 2: Starting Escape A from best"
- "Final best det: 0.XXXXXX from search C-3"
