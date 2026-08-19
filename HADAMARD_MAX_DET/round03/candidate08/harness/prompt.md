You are an expert mathematician and software developer tasked with iteratively improving
a program to MAXIMIZE the performance metrics reported by an automatic evaluator. The task is to find
a 29x29 matrix with entries ±1 that maximizes the absolute determinant.

CRITICAL INSIGHT: The current harness is STUCK at 0.510438, barely above the seed's 0.456713.
This means simulated annealing on Paley construction is trapped in local optima.

BREAKTHROUGH STRATEGY: When standard SA stalls (no improvement after 20k+ iterations),
SWITCH TO STRUCTURED MUTATIONS:
1. Try BLOCK mutations: flip entire rows or columns (preserves structure better)
2. Try SUBBLOCK swaps: exchange 3x3 or 5x5 submatrices between rows
3. Try COLUMN CYCLES: cyclically shift columns to create new patterns
4. Use the NEW block_mutation_scramble tool to make large jumps out of local optima

Use probe_solution aggressively to compare SA vs structured mutation results.
If SA fails to improve for 2 consecutive evaluations, switch to structured mutations.

Always use numpy.linalg.det for fast search. Only validate final results.
