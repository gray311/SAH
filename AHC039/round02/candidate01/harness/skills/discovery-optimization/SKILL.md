---
name: discovery-optimization
description: "Optimize a C++ polygon construction program to maximize (mackerels - sardines + 1).\nUse probe_solution for fast ranking, evaluate_solution for final verification.\nTarget >2.5 score per test case with efficient search within 2s time limit."
---

# Orthogonal Polygon Optimization for Mackerel-Sardine Problem

## Objective
Maximize score = max(0, mackerels_inside - sardines_inside + 1)

## Search Loop
1. **PROBE FIRST**: Always call probe_solution after edit_solution to quickly estimate
   which variants are promising. Use it to rank ~50-100 variants quickly.
2. **CONSTRUCT**: Focus on building initial polygons that cover high mackerel density
   regions. Use the seed's construction logic as a starting point.
3. **REFINE**: Once you have a working polygon, try:
   - Expanding vertices outward to capture more mackerels
   - Adding convex corners to reduce sardine coverage
   - Adjusting bounding box to exclude sardine clusters
4. **VERIFY**: Call evaluate_solution on at most 2-3 top probe scores
5. **REWRITE**: If stuck for >10 iterations, completely change the construction approach

## Probing Strategy
- Use probe_solution to score many different polygon variants quickly
- Look for variants where probe score suggests good coverage
- Keep the best probe-scoring variant and verify it

## Key Mutations to Try
- Change how polygon vertices are selected (use clustering on mackerel positions)
- Use KD-tree or grid-based approaches to guide construction
- Try bounding box approaches that exclude known sardine regions
- Add random perturbations to vertex positions within time budget
- Implement iterative local search: move each vertex to improve score

## Time Budget
- Total: 2.0s per test case
- Keep your internal search simple and bounded
- Don't implement complex optimization algorithms that TLE
- 2-3 seconds of C++ code running per test case is too much
