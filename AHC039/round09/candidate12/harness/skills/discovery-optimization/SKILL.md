---
name: discovery-optimization
description: "Rectangle enumeration with KD-tree scoring. Generate candidate axis-aligned rectangles by varying widths/heights and centering around mackerel positions. Use KD-tree for O(log N) fish counting. Run 20-25 restarts, output best rectangle as 4-vertex polygon."
---

# Rectangle Enumeration with KD-Tree Scoring

## Phase 1: KD-Tree Construction
- Build KD-tree from all fish positions (mackerels and sardines)
- Use existing seed KD-tree implementation
- Query time: O(log N) for rectangle intersection

## Phase 2: Rectangle Candidate Generation
For each restart:
- Sample 3-5 mackerel positions as candidate centers
- For each center, try rectangle dimensions:
  * Widths: 500, 1000, 2000, 5000, 10000
  * Heights: 500, 1000, 2000, 5000, 10000
- Ensure rectangle stays within [0, 100000]x[0, 100000]

## Phase 3: KD-Tree Scoring
For each candidate rectangle:
- Query KD-tree for mackerels inside: count1 = query_rect(center_x - w/2, center_x + w/2, center_y - h/2, center_y + h/2)
- Query KD-tree for sardines inside: count2 = query_rect(...)
- Score = count1 - count2
- Track best rectangle by score

## Phase 4: Polygon Output
- Convert best rectangle to 4 vertices (bottom-left, bottom-right, top-right, top-left)
- Ensure perimeter <= 400,000 (max rectangle: 100000x100000 = 400,000 perimeter)
- Output as valid polygon

## Phase 5: Multiple Restarts
- Run 20-25 restarts with different random seeds
- Each restart explores different mackerel clusters
- Output best rectangle from all restarts

## Key Implementation Notes
- Total time per evaluation: < 2.0s
- Use std::random_device for seed generation
- KD-tree query is O(log N), enumeration is O(restarts * num_centers * num_dimensions * 2)
- For N=5000 fish, this is very efficient
- Axis-aligned rectangles cannot self-intersect (trivial validation)
