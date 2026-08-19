---
name: cluster-based-polygon-guide
description: Build polygons around identified mackerel clusters using coordinate-based expansion and refinement.
---

# Cluster-Based Polygon Construction Guide

## Core Strategy

Instead of grid-based approximation, work directly with fish coordinates at the actual positions.
This enables precise polygon edges that capture individual fish.

## Phase 1: Cluster Identification

- Parse all fish positions from input

- Use hash map for O(1) position lookup

- Find mackerel clusters using local density (mackerels within 800 units)

- For each cluster, compute bounding box and sardine count inside

- Rank clusters by mackerel density (mackerels per area)

## Phase 2: Cluster-Centric Expansion

From each high-density cluster:

1. Start with cluster bounding box as initial polygon

2. Extend in 4 cardinal directions (N, S, E, W):
   - Move one coordinate unit at a time
   - At each step, check if extending captures more mackerels or avoids sardines
   - Use hash map to count fish in the extended region

3. Stop conditions:
   - Perimeter reaches 400,000
   - No improvement in M-S score
   - Hitting sardine-rich region (S > M + 3)

## Phase 3: Multi-Cluster Polygons

- Select top 3-5 clusters with highest density

- Build separate small polygons for each

- Ensure total perimeter stays under 400,000

- Consider 4-lobed polygon if clusters are spatially separated

## Phase 4: Edge Refinement

For each polygon edge:

1. Try parallel shifts: ±1, ±2, ±3, ±4, ±5, ±10 units

2. For each shift:
   - Compute which fish positions cross the edge
   - Count mackerels and sardines affected (hash map lookup)
   - Calculate net score change

3. Keep shift with best improvement

4. Repeat 2-3 refinement rounds

## Phase 5: Multiple Restarts

- Run 10-15 restarts

- Each restart: pick random starting cluster or random mackerel position

- Build polygon from seed, refine, track best

## Phase 6: Validation

- Output valid axis-aligned polygon

- Ensure: 4 <= vertices <= 1000, integer coords in [0,100000], perimeter <= 400000

- Output format: m followed by m lines of "x y"
