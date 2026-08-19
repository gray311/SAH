You are optimizing a 29x29 +/-1 matrix to maximize |det(H)|. Theoretical max is ~155.5.

The seed program uses Paley construction + SA but is stuck at |det|~80 (score 0.51).
Root causes: (1) Only Paley construction, (2) Single-entry SA has tiny steps, (3) 50k iterations insufficient.

REQUIREMENT: Try 5+ construction methods systematically:
- Paley, Random, Block, Genetic, Permutation

For EACH evaluation:
1. Test 3-5 variants across DIFFERENT constructions (not same method with different params)
2. Probe 5-7 variants before evaluate_solution
3. Evaluate only the top probe winner
4. Return global best across ALL methods

Protocol: Rotate methods every eval. If you just tried Paley, try Random/Block/GA next.

Tool: use evaluate_construction_method to explore parameter grids for ONE construction type.

Time budget: 350s per eval. Max 180s per method. Use numpy.linalg.det only.
