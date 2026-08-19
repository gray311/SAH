---
name: discovery-optimization
description: "Bounding box edge refinement. Find core mackerel region, optimize 4 edges with \u00b11..\u00b15 shifts, iterative improvement until convergence, 10 restarts."
---

# Bounding Box Edge Refinement Strategy
## Core Idea Instead of building complex multi-lobed polygons, refine a simple bounding box around the mackerel cluster with local edge optimization.
## Step 1: Find Core Region - Parse fish positions from input - Identify region with high mackerel density - Start with a conservative bounding box around this region
## Step 2: Edge-Level Optimization For each of the 4 edges (top, bottom, left, right): - Try shifting edge by ±1, ±2, ±3, ±4, ±5 units - For each shift, calculate: * Mackerels inside new box * Sardines inside new box * Score = M - S - Keep the shift that gives maximum score
## Step 3: Iterative Improvement - After optimizing all 4 edges, repeat the process - Continue until no improvement in 2 consecutive rounds - This ensures local optimum is found
## Step 4: Multiple Restarts - Run 10 restarts with different starting boxes - Each restart: * Pick random point as seed * Expand to capture nearby mackerels * Apply edge-level optimization - Output best polygon across all restarts
## Step 5: Validation - Ensure 4-1000 vertices - Integer coordinates in [0,100000] - Perimeter ≤ 400,000 - No self-intersection
## Implementation Notes - Use O(N) scoring: for each shift, recount mackerels/sardines in O(N) - Total time per eval: < 2.0s with efficient implementation - Use std::random_device for seed generation
