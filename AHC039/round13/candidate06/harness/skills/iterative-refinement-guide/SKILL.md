---
name: iterative-refinement-guide
description: Iterative vertex perturbation for axis-aligned polygon optimization. Use gradient-based expansion, edge protrusions, and multi-scale refinement to find high-scoring polygons.
---

# Iterative Polygon Refinement Guide

## Strategy Overview

This approach treats polygon optimization as a continuous local search problem.
Instead of grid-based or corridor methods, we directly perturb vertices to find
better shapes.

## Phase 1: Initialization

Choose a starting polygon:
- Option A: Bounding box of all mackerel locations
- Option B: A rectangle centered at the centroid with size ≈ average mackerel spacing
- Ensure it's valid (4-1000 vertices, proper perimeter constraint)

## Phase 2: Gradient-Based Vertex Perturbation

For each vertex (x, y):
1. For each axis (x-only, y-only):
   - Try shifts: ±1, ±2, ±4, ±8, ±16 (doubling pattern)
   - Estimate local fish density after shift using estimate_local_density
   - Keep shift if it improves (mackerels - sardines) locally
2. Check perimeter constraint before accepting

## Phase 3: Edge Protrusion

For each horizontal/vertical edge:
1. Determine outward normal direction
2. Try extending by d ∈ {50, 100, 200, 400, 800} units
3. Use density estimation to predict fish gain/loss
4. Add protrusion if net positive expected gain and within perimeter budget

## Phase 4: Bay Removal

At concave corners:
1. Check sardine density inside the "bay"
2. If sardine density > threshold, try cutting the bay inward
3. Accept if net gain is positive

## Phase 5: Multi-Scale Refinement

Run refinement in three passes:
- Pass 1 (coarse): Δ ∈ {±100, ±200} to explore large shape changes
- Pass 2 (medium): Δ ∈ {±10, ±20, ±30} to tune boundaries
- Pass 3 (fine): Δ ∈ {±1, ±2} to align with fish locations

## Phase 6: Simulated Annealing

Every 50 iterations:
- Try random vertex moves (uniform random in [-50, 50])
- Accept worse solutions with probability: exp(-Δ_score / T)
- Decay temperature: T ← T × 0.95

## Implementation Tips

- Use efficient counting: pre-sort fish by coordinate, use prefix sums
- Validate polygon validity after each major change
- Cache density estimates to avoid recomputation
- Track best polygon seen, not just current
