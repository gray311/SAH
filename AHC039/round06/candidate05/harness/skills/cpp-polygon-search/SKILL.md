---
name: cpp-polygon-search
description: For orthogonal polygon optimization in C++, implement an internal bounded search. Use grid analysis to seed promising regions, then perform hill climbing or iterative refinement while checking validity constraints.
---

# C++ Polygon Search Strategy for Orthogonal Polygons

## Phase 1: Grid Analysis
- Use analyze_fish_grid to get high-level fish distribution
- Identify dense mackerel regions and avoid sardine-heavy areas
- Create a coarse grid map for rapid lookups

## Phase 2: Seed Polygon Construction
- Start with a simple rectangle or L-shaped polygon
- Place vertices at grid boundaries where mackerels are dense
- Ensure all edges are axis-aligned

## Phase 3: Internal Optimization Loop
- Use a time budget (e.g., 1.5s for 150 test cases)
- Implement iterative improvements:
  * Try expanding polygon edges outward
  * Split or merge polygon regions
  * Adjust vertices to capture more mackerels
  * Always validate: perimeter <= 400000, vertices <= 1000

## Phase 4: Validation
- Check all constraints before final output
- Ensure no self-intersections (for orthogonal polygons, check edge crossings)
- Verify output format matches expected format

## Tips:
- Use KD-trees or spatial hashing for fast point-in-polygon queries
- Pre-sort fish by coordinate for efficient grid population
- Cache intermediate results to avoid redundant computation
- The search must complete within the time limit - don't optimize too much!
