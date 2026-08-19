---
name: discovery-optimization
description: "Optimize C++ polygon-constructing code for NP-hard fish-capture. Use KD-tree for fast scoring,\nthen iteratively refine edges using analyze_polygon to identify sardine-dense and mackerel-rich\nregions, applying targeted mutations that increase (mackerels - sardines) score within time limits."
---

# KD-Tree Polygon Optimizer for Fish Capture

## Core Algorithm
1. **Build KD-tree** of all 10,000 fish (5000 mackerels + 5000 sardines) at startup
2. **Score polygons** in O(log N) per rectangle using KD-tree queries
3. **Iterative refinement**: Use analyze_polygon to identify which edges need adjustment
4. **Local search**: Perturb edges by ±1 to ±20 units, keep improvements

## Step-by-Step Process

### Phase 1: Initialization (0.1s)
- Parse fish positions, build KD-tree
- Create initial polygon (axis-aligned rectangle covering mackerel extent)

### Phase 2: Analysis (0.05s per iteration)
- Call analyze_polygon to get:
  - sardine_count_by_edge: how many sardines each edge captures
  - mackerel_density_by_edge: mackerels per unit length along each edge
  - recommended_mutation: specific edge shift that maximizes score change

### Phase 3: Mutation (0.2s per iteration)
- Apply recommended mutation:
  - Shift edge toward mackerel-dense region
  - Indent edge away from sardine-dense region
  - Ensure polygon remains valid (non-self-intersecting, perimeter ≤ 400,000)
- Score new polygon using KD-tree

### Phase 4: Accept/Reject (0.05s)
- If score improved, keep mutation
- If not improved but valid, try next mutation
- Early terminate if no improvement for 0.3s

### Phase 5: Final Polish (0.4s)
- Try random restarts with different initial polygons
- Try L-shapes that combine two rectangles
- Output best valid polygon found

## Key Optimizations
- **KD-tree**: O(1) fish counting after O(N log N) build
- **Spatial queries**: Only query rectangles that could change score
- **Local search**: Focus mutations near polygon edges with high fish density
- **Perimeter constraint**: Always validate perimeter ≤ 400,000

## Avoid Pitfalls
- Never output a static polygon - must search actively
- Always check polygon validity (non-self-intersecting, axis-aligned edges)
- Respect time budget - use early termination
- Don't make mutations that break validity without checking
- Track best score across all iterations
