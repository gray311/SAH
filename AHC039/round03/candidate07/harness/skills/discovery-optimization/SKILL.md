---
name: discovery-optimization
description: "Iteratively optimize an orthogonal polygon constructor to maximize (mackerels - sardines + 1). Use probe_solution to cheaply rank candidates before full evaluation. Generate multiple candidate polygons using grid-cell expansion and boundary-following strategies, then confirm top performers with evaluate_solution."
---

Discovery optimization for orthogonal polygons:

One tool call per turn. You have 20 evaluation budget calls total. Use probe_solution extensively (it is FREE) to rank many polygon variants before spending evaluate_solution calls.

Step 1: Generate candidate polygons using construct_orthogonal_polygon. This tool creates multiple candidate axis-aligned polygons based on fish density patterns.

Step 2: Call probe_solution for each candidate. It returns approximate scores on ~2000 fish, letting you rank candidates without using your evaluation budget.

Step 3: Call evaluate_solution only on your 1-2 best-ranked candidates from probing.

Step 4: Iterate: refine promising polygons with new parameters or different construction strategies, probe them, and occasionally evaluate.

Key constraint: Your C++ code must run in < 2.0s per test case. The polygon must have <= 1000 vertices and perimeter <= 400,000.

Never evaluate the same polygon twice. Always use probe_solution first. When construct_orthogonal_polygon is not enough, try manually writing different polygon generation strategies in the EVOLVE-BLOCK.

End with finish(summary) when you have evaluated enough variants or cannot improve further.
