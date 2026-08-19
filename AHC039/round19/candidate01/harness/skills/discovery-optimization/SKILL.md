---
name: discovery-optimization
description: "Minimal polygon around mackerels with local refinement. Build bounding box of all mackerels, refine edges via perturbation, 5 restarts with perturbations, evaluate with full scoring."
---

# Minimal Polygon Strategy for Fish Capture

## Core Idea

Build a minimal axis-aligned polygon that contains all mackerels (maximizing guaranteed gain), then refine locally.

## Step 1: Parse Input

- Read 2N fish positions from input
- First N lines: mackerels (type=1)
- Next N lines: sardines (type=-1)

## Step 2: Build Minimal Bounding Box

- Find min_x, max_x, min_y, max_y among all mackerels
- If all have same x or same y (collinear), expand perpendicular by ±1 unit
- Create 4-vertex polygon from bounding box

## Step 3: Local Refinement

For each of 5 restarts:

- For each edge (4 edges for rectangle):
  * Try perturbations: expand outward by ±10, ±20, ±30 units
  * Generate new polygon with edit_solution
  * Evaluate with evaluate_solution to score candidates
  
- For interior points check: if a vertex position could be improved by shifting the edge
  * Try 3 rounds of refinement

## Step 4: Handle Edge Cases

- All mackerels collinear in X: expand ±1 in Y direction
- All mackerels collinear in Y: expand ±1 in X direction  
- Single mackerel: use 10x10 square centered on that point

## Step 5: Validation

- Ensure: 4 <= vertices <= 1000
- Ensure: perimeter <= 400,000
- Ensure: all coords in [0, 100000]
- Ensure: no self-intersection (axis-aligned rectangles are inherently valid)

## C++ Implementation Notes

- Use fast I/O with std::cin.tie(nullptr)
- Use direct coordinate comparison for fish counting (O(N*M) where M is polygon complexity)
- Total time per evaluation: < 2.0s
