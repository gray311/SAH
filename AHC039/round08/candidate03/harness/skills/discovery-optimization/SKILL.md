---
name: discovery-optimization
description: "Probe-driven polygon optimization for axis-aligned fish capture. Use spatial hashing to rapidly score polygon variants, then refine with hill climbing. Run multiple restarts and output best polygon."
---

# Probe-Driven Polygon Optimization

## Core Idea: Rapidly iterate on polygon shape using cheap probes

### Phase 1: Analyze Fish Distribution
- Build a 500x500 spatial hash grid (cell_size=200)
- For each cell, count mackerels (M) and sardines (S)
- Identify "hot cells": cells with high (M-S) ratio
- Find connected hot regions (clusters of adjacent high-scoring cells)

### Phase 2: Generate Diverse Candidate Polygons
For each top cluster, generate 4 distinct patterns:

**Pattern A: Tight Bounding Box**
- Compute minX, maxX, minY, maxY of all mackerels in cluster
- Output rectangle (4 vertices)

**Pattern B: Notched Rectangle (Exclude Edge Sardines)**
- Start with Pattern A's bounding box
- Find sardines within 150 units of each edge
- Create a notch by indenting that edge inward by 50-100 units
- This excludes the sardine while keeping most mackerels

**Pattern C: Multi-Room Polygon**
- Divide the cluster region into 3-4 smaller rectangles
- Arrange them to avoid sardine-rich areas
- Connect them with narrow corridors (still axis-aligned)
- This captures dispersed mackerels while minimizing sardine overlap

**Pattern D: Expanding Spiral**
- Start with a small 100x100 square around the cluster center
- Gradually expand outward in a spiral pattern
- Stop when score starts decreasing (use probe to detect)

### Phase 3: Probe-Driven Refinement
For each candidate polygon:
1. Call probe_solution with current polygon
2. For each of its 4-8 edges, try shifting by ±10, ±20 units (6 variations per edge)
3. Probe each variation, keep the best
4. Repeat up to 2 rounds
5. Return the best refined version

### Phase 4: Evaluation and Final Hill Climb
- Pick top 3 candidates by probe score
- Call evaluate_solution on each to get exact scores
- On the best one, do fine-grained hill climb: shift each edge by ±1, ±2, ..., ±15 units
- Use grid-based counting for fast score estimation during hill climb
- Output the final best polygon

### Phase 5: Multiple Random Restarts
- Run Phases 1-4 with 3-5 different random seeds
- Perturb cluster selection and edge shifts randomly
- Track the best polygon across all runs

## Implementation Notes
- Use a hash grid for O(1) rectangle queries
- Probe should complete in <0.1s; full evaluation in <0.5s
- Total time per search: ~1.5-1.8s to leave margin for 2.0s limit
- Always validate polygon (no self-intersection, perimeter <= 400000, vertices <= 1000)
