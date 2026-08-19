---
name: discovery-optimization
description: "Fast KD-tree based polygon optimization. Build KD-tree once, generate 20-30 random rectangles per restart,\nscore using quick_score_polygon tool, combine top rectangles, light edge adjustment with \u00b110..20 shifts.\n6 restarts only. Target <1.8s per eval."
---

# Fast KD-Tree Polygon Optimization

## Core Strategy

Replace expensive grid-based search with KD-tree powered rectangle exploration.

## Phase 1: KD-Tree Setup

- Parse all fish coordinates at program startup
- Build balanced KD-tree over all 2N points (N mackerels + N sardines)
- Each node stores bounding box for efficient rectangle queries

## Phase 2: Rectangle Generation and Scoring

For each restart:
- Generate 20-30 random axis-aligned rectangles
- For each rectangle (x1,y1,x2,y2):
  * Query KD-tree for mackerel count (O(log N))
  * Query KD-tree for sardine count (O(log N))
  * Score = M - S + 1
  * Store if valid (perimeter <= 400000)

## Phase 3: Rectangle Combination

- Take top 5-8 rectangles by score
- Try combining adjacent rectangles (share x-range or y-range)
- Merged rectangle = union bounds
- Recalculate score for merged rectangle
- Keep non-intersecting combinations

## Phase 4: Light Edge Adjustment

- For best polygon(s), adjust each corner by ±10, ±20 units
- Use quick_score_polygon tool for fast evaluation
- Repeat 2 passes (total 4 adjustments per corner)
- Keep best result

## Phase 5: Multiple Restarts

- 6 restarts with different random seeds
- Each restart is independent
- Output single best polygon across all restarts

## Implementation Notes

- Use std::set for O(log N) rectangle storage and deduplication
- Quick rectangle scoring: sum of mackerels - sum of sardines + 1
- Simple validation: check perimeter and bounds only (rectangles can't self-intersect)
- No complex geometry needed — stick to rectangles and simple unions
