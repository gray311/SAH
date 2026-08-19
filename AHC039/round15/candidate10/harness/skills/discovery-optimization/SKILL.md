---
name: discovery-optimization
description: "KD-tree based rectangular querying with vertex-level hill climbing. Build KD-tree, use for O(log N) fish counts, seed from mackerel clusters, climb by expanding/shrinking vertices."
---

# KD-Tree Polygon Optimization Strategy

## Phase 1: KD-Tree Construction
- Build balanced KD-tree on all fish positions
- Split alternately by x and y coordinate
- Store fish index at each node

## Phase 2: Rectangle Query
- Recursive function: query_rectangle(node, minX, maxX, minY, maxY)
- If node point inside rectangle: count it
- If axis=0 (split by x): query left if minX <= node.x, query right if maxX >= node.x
- If axis=1 (split by y): query left if minY <= node.y, query right if maxY >= node.y
- Return (mackerel_count, sardine_count)

## Phase 3: Seed Generation (8 restarts)
Restart 1: Minimal square around median fish position

Restarts 2-8: 
  - Randomly select 2-5 mackerel positions
  - Create bounding box around them
  - Start polygon as this rectangle

## Phase 4: Vertex-Level Hill Climbing
For each candidate polygon:
  For iteration in 0..49:
    For each vertex i in 0..vertices-1:
      For direction in [N,S,E,W] and offset in [±1,±2,±3,±4,±5]:
        Compute new vertex position
        Form new polygon (replace vertex i)
        Query rectangle for score using KD-tree
        If score improves, accept change
    If no improvement this iteration, break
  Output best polygon from this restart

## Phase 5: Output
- Print vertex count
- Print each vertex coordinate
- Ensure all constraints satisfied
