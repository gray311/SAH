---
name: discovery-optimization
description: "Direct mackerel cluster analysis with minimal bounding boxes. Find groups of mackerels within 10000 units, build bounding boxes, connect top clusters, aggressive hill climbing with \u00b1500..5000 shifts, 10-15 diverse restarts."
---

# Cluster and Bounding Box Strategy

## Core Strategy
Find mackerel clusters via 10000-unit proximity, build minimal bounding boxes, connect top clusters with corridors, use LARGE hill climbing shifts (±500..5000).

## Phase 1: Cluster Discovery
1. Parse all mackerel coordinates
2. Use 10000-unit proximity grouping
3. Compute bounding box, mackerel count, sardine count for each cluster

## Phase 2: Bounding Box Construction
- Select top 10-15 clusters by net score
- Create minimal axis-aligned rectangles

## Phase 3: Corridor Connection
- Connect adjacent clusters with minimal corridors

## Phase 4: Polygon Assembly
- Order by score and combine
- Ensure no self-intersection, perimeter <= 400,000

## Phase 5: AGGRESSIVE Hill Climbing
For each edge, try LARGE shifts: ±500, ±1000, ±2000, ±3000, ±5000 units
Repeat 2 refinement rounds

## Phase 6: Multiple Restarts
Run 10-15 restarts with different strategies

## Why Large Shifts?
Small shifts (±5..25) barely change which fish are captured. Large shifts can move edges between fish clusters, dramatically improving scores.
