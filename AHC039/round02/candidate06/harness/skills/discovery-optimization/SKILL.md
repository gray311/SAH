---
name: discovery-optimization
description: "Iteratively optimize a C++ polygon-discovery program for the mackerel-sardine fishing problem.\nEach iteration adds internal search logic to improve the polygon within the 2.0s time limit.\nHigher combined_score (mackerels - sardines + 1) is better. Validity=0 means constraint violation or crash."
---

# Heuristic Polygon Discovery Optimization

## Objective
Construct an axis-aligned polygon (edges parallel to x/y axes) that maximizes:
score = max(0, mackerels_inside - sardines_inside + 1)

## Constraints
- Vertices: 4 to 1000
- Perimeter: <= 400,000
- Coordinates: integers in [0, 100000]
- No self-intersection
- 150 test cases, each must complete in ~2.0s total

## Winning Strategy Pattern
The C++ code MUST contain a runtime search loop that:
1. Starts from an initial polygon (rectangle, or random vertices)
2. Iteratively tries vertex modifications (swap, add, remove, move)
3. Evaluates each variant quickly (use KD-tree for point-in-polygon + point counting)
4. Accepts improvements (hill-climbing) or sometimes worse moves (to escape local optima)
5. Runs until time expires, then outputs the best polygon found

## Code Structure to Target
Look for these sections and ADD SEARCH LOGIC:
- After reading input: initialize polygon (simple rectangle covering all fish or random 8-12 vertices)
- Main loop: while (timer < 1.8s) {
    generate candidate (vertex modification)
    compute score efficiently
    if (score > best) { best = score; update polygon; }
  }
- Output: print best polygon vertices

## Vertex Modification Operators to Implement
- **Swap**: Try two random vertices in different positions
- **Extend**: Add a vertex at a grid point (aligned to axis) that extends perimeter
- **Contract**: Remove a vertex (simplify polygon)
- **Move**: Shift a vertex along axis by 1-10 units
- **Grow**: Add outward vertices to capture more fish

## Efficient Scoring
- Use KD-tree (already present) for fast point-in-polygon classification
- For point-in-orthogonal-polygon: trace rays and count crossings
- Cache results to avoid recomputation
- Use simple geometry: point is inside if ray casts odd number of crossings

## Perimeter Control
- When adding vertices, check cumulative perimeter
- Limit vertex count to ~800 to stay safely under 1000
- Prune excessive vertices if perimeter exceeds 400000

## Time Budget
- Must complete well before 2.0s (aim for 1.8s cutoff)
- Use std::chrono to track elapsed time
- If close to time limit, output current best immediately

## Debugging Invalid Results
- validity=0 means: self-intersection, wrong vertex count, perimeter overflow, or program crash
- Fix by: adding self-intersection checks, capping vertex count, checking perimeter mid-search

## Evaluation Budget
- You have ~20 external evals. Use each wisely:
  - First few: establish baseline, try different search strategies
  - Middle: refine search parameters (iteration count, operator weights)
  - Final: consolidate improvements, ensure robustness

## When to Add New Capabilities
- If current search is too slow: add stronger heuristics (simulated annealing, beam search)
- If stuck at local optimum: add restarts from different seeds
- If scoring is bottleneck: optimize point-in-polygon, use GPU if available
