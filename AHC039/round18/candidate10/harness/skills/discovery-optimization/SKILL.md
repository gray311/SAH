---
name: discovery-optimization
description: "Mutation-based hill climbing using KD-tree for fast scoring. Mutate vertices/edges in 3 rounds, try multiple polygon shapes, use probe for quick ranking."
---

# Mutation-Based Polygon Optimization with KD-Tree

## Overview
Use the seed's existing KD-tree infrastructure for fast fish counting. 
Perform mutation-based hill climbing instead of grid-based approaches.

## Phase 1: Build KD-Tree
- Read N mackerels and N sardines
- Use seed's KDNode structure and build_kdtree() function
- Each node stores fish index and splits alternately by x/y

## Phase 2: Generate Candidates
Generate 5 base polygons:
1. Rectangle: bounding box covering all fish
2. L-shape: two rectangles connected
3. Multi-lobed: 8-16 vertices with protrusions
4-5. Random axis-aligned polygons with 12-24 vertices

## Phase 3: Hill Climbing (3 Rounds)

### Round 1 - Vertex Mutation (Fine)
For each vertex (x,y):
  Try: (x±1,y), (x±2,y), (x±5,y), (x,y±1), (x,y±2), (x,y±5)
  Score each with KD-tree query
  Keep best

### Round 2 - Edge Mutation (Medium)
For each horizontal edge (y1,y2) at row y:
  Try extending/shrinking by 1,2,3,4,5 units
For each vertical edge (x1,x2) at col x:
  Try extending/shrinking by 1,2,3,4,5 units
Score with KD-tree, keep improvements

### Round 3 - Coarse then Refine
Try larger mutations: ±10, ±15 on vertices
Then refine promising variants with ±1, ±2

## Phase 4: Probe Before Final Eval
- Use probe_solution to rank top 5-10 candidates cheaply
- Only run full evaluate_solution on best 1-3 candidates

## Phase 5: Output
- Pick best polygon by full evaluation
- Output format: vertex count, then vertex coordinates

## Implementation Notes
- Reuse: KDNode, build_kdtree, query_kdtree_rectangle, Point, XorShift RNG
- Mutations per candidate: ~50-100 (fast with KD-tree)
- Total time: <1.8s, leaving 0.15s safety margin
- Use seed's timer: global_timer.elapsed() to monitor
