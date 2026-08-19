---
name: discovery-optimization
description: "Erdos C5 bound optimization. Find step functions minimizing max overlap. Key: COMBINATORIAL CONSTRUCTIONS beat gradient descent. Try explicit 2-4 breakpoint step functions first, then refine. Use probe_solution to rank candidates."
---

C5 Bound: Combinatorial Construction Strategy

Why Gradient Descent Fails
The seed's 59k-step Adam optimizer finds local optima. But the true C5 bound likely comes from clever STEP FUNCTION PATTERNS, not gradient descent minima.

Construction Types to Try (COMPLETE REWRITES)

Type A: Single/Double Step Functions
- h=1 on [0,1], h=0 elsewhere (integral=1, compute c5_bound)
- h=alpha on [0,a], h=beta on [b,2], adjusted so integral=1
- Key insight: concentrate mass to minimize overlap

Type B: Symmetric Patterns
- h symmetric around x=1, reduces worst-case overlap
- Try: h=1 on [0.5,1.5], h=0 elsewhere (adjust for integral)
- Try: sinusoidal-like patterns that cancel overlap

Type C: Bistable/Tripartite
- 3 regions: high, medium, low values
- Pattern: [0,a]: high, [a,b]: medium, [b,2]: low
- Tune breakpoints to minimize max_k integral

Type D: Concentrated Mass
- Put most mass in small interval(s)
- e.g., h=0.5 on [0,0.4], h=0.5 on [1.6,2], gap in middle
- Adjust heights to ensure integral=1

Execution Plan
1. Write code that CONSTRUCTS a specific pattern (not optimizing from random)
2. Compute its c5_bound directly (no training loop needed for baseline)
3. Use probe_solution to quickly score your construction
4. If promising (combined_score > 0.95), refine with optimization
5. Try at least 3-4 different CONSTRUCTION TYPES before settling

Important
- COMPLETE REWRITES: Don't patch the seed's optimizer. Write NEW code that builds step functions directly.
- INTEGRAL CONSTRAINT: integral over [0,2] = 1. For step function with height alpha on interval length L: alpha*L contributes to integral. Sum must equal 1.
- RANGE CONSTRAINT: h in [0,1]. Don't violate this!
- BUDGET: 30 evals. Test 3-4 construction types, each with 1-2 refinements.
- PROBE FIRST: Use probe_solution to rank before full evaluation.
