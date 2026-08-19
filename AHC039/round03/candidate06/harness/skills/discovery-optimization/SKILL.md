---
name: discovery-optimization
description: "Optimize C++ code for NP-hard geometry polygon construction. Maximize (mackerels - sardines) in axis-aligned polygon. Use probe_solution for fast ranking, then confirm with evaluate_solution."
---

# Polygon Optimization for Mackerel-Sardine Catch

## Problem
Build axis-aligned polygon maximizing (mackerels_inside - sardines_inside + 1).

## Winning Pattern
1. **Cluster Analysis**: Dense mackerel regions should get polygon coverage. Sardines are "cost" to avoid.
2. **Parametric Construction**: Don't output fixed polygons. Run internal search over parameters (cluster centers, expansion rules).
3. **KD-Tree Optimization**: The seed has this - tune thresholds, sampling rates, and scoring logic.

## Concrete Changes to Try
- **Greedy from clusters**: Find dense regions, expand bounding boxes greedily while perimeter allows
- **Iterative refinement**: Start with small polygons, merge/split to improve score
- **Parameter sweep**: Try different expansion factors, merge thresholds, vertex limits
- **Perimeter budget usage**: Use full 400k budget for more complex shapes

## Use probe_solution
- Test different algorithm parameters cheaply (first 2000 fish)
- Rank strategies: cluster-based vs greedy vs random restart
- Only run full evaluation on top 1-2 variants

## C++ Code Guidance
- Look at: score calculation, polygon validity checks, search loop, KD-tree usage
- Modify: expansion rules, clustering logic, heuristic parameters
- Preserve: input parsing, basic geometry utilities, output format

## Iteration Strategy
1. If score stagnates: change the core algorithm, not just parameters
2. If timeouts occur: reduce search iterations or make heuristics smarter
3. If validity errors: check polygon closure, non-intersection, perimeter limits
4. Use probe_budget (30 probes) to test multiple ideas in parallel
