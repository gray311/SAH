---
name: discovery-optimization
description: "Paley-based Hadamard optimizer for n=29. Build matrix from quadratic residues, then anneal 100k iterations at T=5.0, cool=0.997. Try 4 seeds per eval from [42,123,456,789,2024,2025,2026,2027]. Use numpy.linalg.det only."
---

# Paley Hadamard Optimizer for n=29

## Step 1: Build Paley Base Matrix
Quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
For each position (i,j): diff = (i-j) mod 29
  If diff in residues: H[i,j] = 1
  Else: H[i,j] = -1

## Step 2: Simulated Annealing Hill Climb
For each seed in your 4 chosen seeds:
  - Copy Paley base to current matrix
  - Initialize best = current, best_det = det(current)
  - Set T = 5.0
  - For 100,000 iterations:
      * Pick random (i,j), flip H[i,j]
      * Compute new_det = numpy.linalg.det(H)
      * delta = new_det - current_det
      * If delta > 0: accept, current_det = new_det
      * Else if T > 1e-10 and random() < exp(delta/T): accept, current_det = new_det
      * Else: undo flip
      * T *= 0.997
      * If new_det > best_det: best = current, best_det = new_det
  - Return best matrix for this seed

Return the best matrix across all 4 seeds.

## CRITICAL RULES
- Use numpy.linalg.det for ALL determinant computations
- Never use Bareiss during search (causes timeout)
- Run exactly 100,000 iterations per seed
- Use exactly 4 seeds per evaluation
- Total runtime must be < 350 seconds
tool_descriptions:
  edit_solution: |
    Replace EVOLVE-BLOCK with complete working code implementing:
    1. Paley construction from residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
    2. Simulated annealing: 100k iterations, T=5.0, cool=0.997
    3. Try 4 seeds from [42,123,456,789,2024,2025,2026,2027]
    4. Use numpy.linalg.det for ALL determinants
    Return the matrix with highest determinant.
  evaluate_solution: |
    Run your code and return combined_score. Budget: 20 evals total.
  probe_solution: |
    Cheap approximate score on subsampled data. Use to test different seed choices before evaluate.
  finish: |
    End session when you've used all 20 evals or found the best solution.
sampling:
  temperature: 0.8
  top_p: 0.95
  top_k: 30
  max_tokens: 12288
agent:
  max_iterations: 40
middleware:
  budget_reminder_from_left: 0
  long_tool_output_max_chars: 10000
