---
name: discovery-optimization
description: "Mackerel enclosure with point-level sardine exclusion. Start with bounding box of all mackerels, then greedily add L-shaped notches to exclude individual sardines from the inside while minimizing perimeter cost. Run 20-25 restarts with different sardine exclusion orders."
---

# Mackerel Enclosure with Sardine Exclusion Strategy

## Core Insight

The optimal polygon starts by enclosing ALL mackerels, then strategically excludes sardines using minimal boundary modifications. This is fundamentally different from grid-based approaches because fish positions are exact points, not cell aggregates.

## Phase 1: Initial Enclosure

- Parse all fish coordinates
- Compute minimal axis-aligned bounding box of all mackerels
  * x_min = min(x_i for all mackerels)
  * x_max = max(x_i for all mackerels)
  * y_min = min(y_i for all mackerels)
  * y_max = max(y_i for all mackerels)
- Initial polygon: rectangle with 4 vertices at (x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)
- Count sardines inside this box (points where x_min <= x <= x_max and y_min <= y <= y_max, including boundary)

## Phase 2: Sardine Exclusion via L-Shaped Notches

For each sardine inside the polygon (process in priority order):

1. **Check if exclusion is beneficial**: Only proceed if perimeter + cost <= 400,000 and vertices + 4 <= 1000

2. **Compute minimal notch**: An L-shaped notch to exclude a sardine at (sx, sy) requires:
   - Find the closest edge of the current polygon to (sx, sy)
   - Create a notch that extends from that edge, going around the sardine
   - Notch adds exactly 4 vertices (2 corner points + 2 vertices to close)
   - Perimeter cost = 2 * (horizontal span + vertical span of notch)

3. **Greedy selection**: 
   - Sort sardines by: distance to nearest polygon edge, or by ratio of perimeter cost to sardine value
   - Apply exclusions in this order, stopping when:
     * Budget exhausted (perimeter or vertex limit)
     * No more beneficial exclusions

## Phase 3: Priority-Driven Exclusion Order

Run multiple restarts with different sardine processing orders:

- **Random permutation**: Try each sardine in random order
- **Distance-based**: Process sardines closest to boundary first
- **Value-based**: Process sardines that cost least per unit of perimeter
- **Hybrid**: Combine distance and value heuristics

## Phase 4: Output Generation

- Output polygon vertices in order (clockwise or counterclockwise)
- Ensure all constraints satisfied before submission
- Return single best polygon from all restarts

## Complexity Analysis

- Initial box: O(N) to find min/max coordinates
- Sardine exclusion: O(N * M) worst case where M = number of sardines, but can be optimized with spatial indexing
- Total per eval: O(N^2) for N=5000 is ~25M operations, fits in 2s with efficient C++

## Key Advantages Over Grid-Based Methods

1. **Point-level precision**: Decisions based on exact fish positions, not coarse cells
2. **Minimal boundary modifications**: Each exclusion costs minimal perimeter
3. **Guaranteed mackerel capture**: Starting with all mackerels eliminates trade-offs
4. **Scalable**: Works even with dense fish clusters
