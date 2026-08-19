---
name: fish-capture-strategy
description: Expert strategy for axis-aligned fish-capture polygon optimization. Focus on stepped/terraced boundaries, grid-based rapid scoring, and multi-restart local search.
---

# Fish Capture Polygon Optimization Strategy

## Core Insight
This is a maximum-weight axis-aligned polygon problem. The optimal solution uses STEPPED boundaries that can include many mackerels with minimal perimeter cost while excluding sardines.

## Phase 1: Grid-Based Rapid Exploration
- Create a 200x200 grid over [0, 100000] coordinates (cell size = 500)
- For each grid cell, count mackerels vs sardines using the fast probe
- Identify "profitable" cells: those with more mackerels than sardines
- Build initial polygons from contiguous profitable cell clusters

## Phase 2: Polygon Construction Patterns
### Pattern A: Cluster Bounding Boxes
- Divide mackerels into quadrants (top/bottom, left/right)
- For each quadrant, create a bounding box
- Score each, keep best 10

### Pattern B: L-Shaped Polygons  
- Take bounding box of all mackerels
- Try removing each corner (top-left, top-right, bottom-left, bottom-right)
- Each removal creates an L-shape with 6 vertices
- Score each variant, keep top 5

### Pattern C: Stepped/Terraced Boundaries
- For each row of grid cells, include cells with majority mackerels
- Connect cell boundaries to create stepped polygon
- This can achieve high density with low perimeter cost

### Pattern D: Hull-Like Construction
- Find extreme points (min_x, max_x, min_y, max_y mackerels)
- Connect them in sequence: bottom-left → bottom-right → top-right → top-left
- Refine each edge by adding intermediate points for local optima

## Phase 3: Local Optimization with Time Budget
- For each candidate polygon:
  * Run 100-200 iterations of edge perturbation
  * For each edge, try ±1 to ±50 unit shifts
  * Keep only improvements
  * Record best score

## Phase 4: Multi-Random-Restart
- Generate 10-20 diverse starting points:
  * 5 from quadrant bounding boxes
  * 5 from L-shapes
  * 5 from stepped patterns
- Run local optimization on each
- Return global best

## Key Parameters
- Grid resolution: 500x500 cells (balances speed and accuracy)
- Perturbation range: ±1 to ±50 units per edge
- Iterations per restart: 100-500
- Total restarts: 10-20
- Time budget: 1.9s for all of the above

## Common Pitfalls
- Don't use overly complex polygons (>1000 vertices)
- Don't ignore perimeter constraint (400,000 max)
- Don't hardcode a single shape - search actively
- Don't forget to exclude sardine-dense regions
- Ensure polygon is non-self-intersecting (axis-aligned guarantees if edges alternate properly)
