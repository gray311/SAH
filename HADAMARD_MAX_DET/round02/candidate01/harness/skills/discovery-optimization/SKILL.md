---
name: discovery-optimization
description: "Optimize Hadamard-like matrix construction for n=29 (max |det(H)|). CRITICAL: Replace slow Bareiss determinant\nin search loop with fast numpy.linalg.det(). Use multiple construction methods (Paley with diagonal correction),\n10-15 restarts, 5000-8000 iterations each. Use probe_solution to rank variants before full evaluation.\nKeep all searches within 200s. Never use exact determinant inside hill climbing loop."
---

# Hadamard-like Matrix Optimization for n=29

## CRITICAL PERFORMANCE REQUIREMENT

The seed program computes exact determinant (Bareiss algorithm) INSIDE the hill climbing loop for every
iteration. This is catastrophic: for a 29x29 matrix, each Bareiss call takes ~0.1-0.5 seconds in Python.
With 10000 iterations × 15 restarts, you need ~260-2500 seconds per evaluation, far exceeding the 200s budget.

SOLUTION: Use numpy.linalg.det() for ALL iterations during hill climbing. This is implemented in C and
takes ~0.001 seconds per call. You can run 100,000+ iterations in the budget. Only use your exact
Bareiss implementation once at the END on your best matrix for the official evaluation score.

## Strategy: Fast search + multiple constructions

### Phase 1: Fix the Paley construction with diagonal correction

For n=29 (≡ 3 mod 4), use Paley construction:
- Quadratic residues mod 29: {1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
- H[i][j] = 1 if (i-j) mod 29 is a quadratic residue, else -1
- CORRECTION: Force H[i][i] = +1 for all i (Paley may give -1 on diagonal)

### Phase 2: Fast hill climbing with numpy determinant

Replace det_bareiss() calls in the search loop with numpy.linalg.det().

Pseudocode for improved hill_climb:
- Use numpy.linalg.det() for each iteration
- Accept/reject with simulated annealing
- Schedule: T = 2.5, cool_rate = 0.997

### Phase 3: Multiple restarts with fast evaluation

- Use 10-15 different seeds (42, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300)
- Run 5000-6000 iterations per restart
- Total time: 15 restarts × 6000 iters × 0.001s = ~90 seconds (well under 200s budget)
- At the end, use exact Bareiss on best matrix for official score

### Phase 4: Use probe_solution strategically

Before calling evaluate_solution (which consumes your budget), create 2-3 variants:
1. Original fast search result
2. Same search but with different temperature schedule
3. Different construction method (e.g., random perturbations from Paley)

Use probe_solution to rank them (cheap, ~10s, no budget cost). Only evaluate the top 1-2.

### Implementation template

def construct_hadamard_matrix(n=29):
    def det_fast(A):
        return abs(np.linalg.det(np.array(A, dtype=np.float64)))
    
    def det_exact(A):
        # Your existing Bareiss implementation
        pass
    
    def create_paley_with_diagonal_correction(size):
        quadratic_residues = {1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                diff = (i - j) % size
                row.append(1 if diff in quadratic_residues else -1)
            row[i] = 1
            matrix.append(row)
        return matrix
    
    def hill_climb_fast(start_matrix, max_iters=6000):
        current = [row.copy() for row in start_matrix]
        current_det = det_fast(current)
        best_matrix = [row.copy() for row in current]
        best_det = current_det
        T = 2.5
        
        for _ in range(max_iters):
            i, j = random.randint(0, n-1), random.randint(0, n-1)
            current[i][j] *= -1
            new_det = det_fast(current)
            delta = new_det - current_det
            if delta >= 0 or (T > 0 and random.random() < np.exp(delta / max(1.0, T))):
                current_det = new_det
                if new_det > best_det:
                    best_det = new_det
                    best_matrix = [row.copy() for row in current]
            else:
                current[i][j] *= -1
            T *= 0.997
        
        return best_matrix, best_det
    
    best_result = None
    best_det = 0
    
    seeds = [42, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]
    for seed in seeds:
        start = create_paley_with_diagonal_correction(n)
        result, det_val = hill_climb_fast(start, max_iters=6000)
        if det_val > best_det:
            best_det = det_val
            best_result = result
    
    if best_result:
        final_det = det_exact(best_result)
        if abs(final_det) > best_det:
            best_det = abs(final_det)
    
    return best_result if best_result else create_paley_with_diagonal_correction(n)

### Tools

- edit_solution: Change EVOLVE-BLOCK
- evaluate_solution: Full scoring with exact determinant
- probe_solution: Quick ranking (~10s), does NOT use eval budget
- finish: End session

### Workflow

1. Implement hill_climb_fast using numpy.linalg.det()
2. Add diagonal correction to Paley construction
3. Set iterations=6000, restarts=14
4. Call edit_solution, then evaluate_solution
5. If score good, probe 2-3 variants before next evaluate
6. Repeat or finish
