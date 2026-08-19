Task: Maximize |det(H)| for a 29×29 matrix with entries ±1.

Key insight: The seed uses Paley construction from quadratic residues, which may already be near-optimal for this approach. To find BETTER solutions, you MUST explore fundamentally different matrix CONSTRUCTIONS, not just tune SA parameters.

Available construction strategies (experiment with ALL of them):

1. RANDOM INITIALIZATION: Start with a random ±1 matrix, then apply simulated annealing. Use 20-30 seeds with 20k iterations each.

2. PALEY CONSTRUCTION: Use quadratic residues mod 29: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}. But try VARIATIONS: add/remove residues randomly, shuffle the residue set, use different SA seed values.

3. GAUSSIAN ELIMINATION APPROACH: Construct a matrix greedily by flipping entries to maximize orthogonality between rows, using det as the optimization metric.

4. MULTI-START STRATEGY: Run 3-5 completely independent SA runs from different starting matrices (random, Paley, greedy). Each run can have different parameters. Take the BEST result across all runs.

CRITICAL STRATEGY:
- Run 3-5 DIFFERENT starting constructions (not just 500 seeds from one)
- Each starting construction should be fundamentally different
- Use numpy.linalg.det for ALL determinant calculations (fast ~0.001s)
- Time budget per eval: < 250 seconds

Workflow for each evaluation:
1. Implement 3-5 different starting construction methods
2. Run simulated annealing from each starting point
3. Track the BEST matrix across all runs
4. Return only the best result

Tool usage:
- probe_solution: Test 2-3 construction strategies quickly (100 iterations each)
- evaluate_solution: Run full search with multiple diverse starting constructions
- edit_solution: Provide COMPLETE working code implementing your chosen strategy
