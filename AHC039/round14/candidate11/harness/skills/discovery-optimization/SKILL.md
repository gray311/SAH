---
name: discovery-optimization
description: "Direct geometric search for mackerel cluster optimization. Use random rectangle generation and local vertex perturbation on fish coordinates (no grid abstraction). 10-15 restarts, 30-50 rectangles per restart."
---

# Direct Geometric Search Strategy

## Core Idea

Instead of coarse grid-based corridor expansion, work directly with fish coordinates to build tight polygons around mackerel-rich regions.

## Phase 1: Coordinate Analysis

- Read all fish positions directly from input

- Identify mackerel clusters by proximity (gap > 5000 = separate clusters)

- Compute bounding boxes around each cluster

## Phase 2: Random Rectangle Generation

- Generate random axis-aligned rectangles with vertices in [0,100000]

- Size diversity: small (100x100) to large (20000x20000)

- Generate 30-50 rectangles per evaluation

- Validate: 4 vertices, perimeter ≤ 400,000, no self-intersection

## Phase 3: Local Perturbation

For each candidate polygon:

- Perturb each vertex by ±10, ±25, ±50, ±100, ±200 units in each direction

- Try swapping x and y coordinates of adjacent vertices

- Keep perturbations that improve (mackerels - sardines)

- Repeat up to 3 refinement rounds

## Phase 4: Polygon Combination

- Try combining 2-3 nearby rectangles into larger shapes

- Ensure constraints: vertices ≤ 1000, perimeter ≤ 400,000

## Phase 5: Multiple Restarts

- Run 10-15 restarts with different seeds

- Each restart: 30-50 random rectangles + perturbation search

- Output best valid polygon

## Implementation Notes

- O(N) fish analysis at startup
- Efficient rectangle generation (4 vertices per rectangle)
- Fast self-intersection check for axis-aligned polygons
- Total time: < 2.0s per evaluation
