You are an expert optimizing a 29x29 ±1 matrix to maximize |det(H)|. The seed uses Paley construction which produces a local optimum. YOU MUST CHANGE THE CONSTRUCTION METHOD.

PRIMARY STRATEGY: RANDOM INITIALIZATION + AGGRESSIVE SIMULATED ANNEALING
1. Initialize matrix RANDOMLY with ±1 entries (not Paley)
2. Run simulated annealing with 100,000 iterations, initial_temp=20.0, cool_rate=0.9995
3. Use numpy.linalg.det for all iterations (fast ~0.001s per det)
4. Total time: ~100k × 0.001s + overhead ≈ 100-150s (under 350s budget)
5. Return the matrix with highest determinant found

WHY THIS WORKS: Random initialization explores the space differently than Paley, potentially finding better local optima. The aggressive temperature and many iterations allow escape from suboptimal regions.

CONSTRAINTS: - MUST use random initialization (not Paley) - MUST use numpy.linalg.det (not Bareiss) - Total iterations 80k-150k - Time < 350s

TOOLS: edit_solution (provide full working code), evaluate_solution (call once on your best result).
