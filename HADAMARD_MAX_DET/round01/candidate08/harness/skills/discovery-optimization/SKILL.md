---
name: discovery-optimization
description: "Optimize Hadamard-like matrix construction for n=29 (max |det(H)|). Use multiple construction strategies (Paley, quadratic residues, cyclic), multiple restarts with different seeds, extended search (5000-10000 iterations), and probe_solution for quick variant ranking before full evaluation. Keep all searches within 350s budget."
---

# Hadamard-like Matrix Optimization for n=29

## Critical constraint
n=29 does not satisfy n % 4 == 0, so true Hadamard matrices don't exist. We're doing combinatorial optimization to find the BEST possible ±1 matrix.

## Strategy: Multiple diverse constructions + extensive search

### Phase 1: Test multiple construction methods

Method A: Paley construction (works for prime n where n ≡ 3 (mod 4))
- Compute Legendre symbol for each element
- Use quadratic residues as +1, non-residues as -1
- This is more principled than arbitrary quadratic residue sets

Method B: Cyclic shifts of rows/columns
- Start with any good small block
- Generate other rows by cyclic shifts
- Try different shift amounts

Method C: Random perturbations from structured seed
- Start from Paley or cyclic
- Apply bounded random flips
- Use simulated annealing

Method D: Random restarts
- Try 5-10 different starting seeds
- Run hill climbing from each
- Pick best result

### Phase 2: Extended search parameters

- Increase iterations from 2000 to 5000-10000
- Adjust temperature schedule: T = 0.8 / (1 + t * 0.0008)
- Use multiple independent runs and pick best
- Consider 2-3 different construction methods and compare

### Phase 3: Use probe_solution wisely

- Before full evaluation, create 2-3 variants
- Use probe_solution to rank them (cheap, ~10s)
- Only evaluate the top 1-2 variants with evaluate_solution
- This saves precious eval budget

### Phase 4: Guardrails

- Total search time per evaluation must be <200s (leaves margin)
- If hitting timeout, reduce iterations or number of restarts
- Always return a valid 29x29 ±1 matrix
- Determinant calculation uses Bareiss (exact integer arithmetic)

### Tools

- edit_solution: Change EVOLVE-BLOCK. Use targeted SEARCH/REPLACE for small changes.
- evaluate_solution: Full scoring. Track your best score.
- probe_solution: QUICK ranking (~10s). Does NOT use eval budget. Create variants, probe them, evaluate only the winner.
- finish: When budget exhausted or no improvement.

### Workflow template

1. Pick a construction method (start with Paley for n=29)
2. Set up extended search (10000 iterations, multiple restarts)
3. Write code with EXACT parameters
4. Call edit_solution (full block rewrite if needed, or targeted diff)
5. Call evaluate_solution to get baseline score
6. If score is good but can improve, modify parameters
7. Before next evaluate, consider creating 2-3 variants and using probe_solution
8. Evaluate only the probe winner
9. Repeat or finish

## Common pitfalls

- NOT trying multiple construction methods
- Too few iterations (2000 may be insufficient)
- Only one random seed
- Not using probe_solution to rank variants
- Running out of time before completing search
