---
name: discovery-optimization
description: "Optimize C++ code for the mackerel-sardine fishing problem by implementing a rectangle-based polygon construction with bounded internal search. Use analyze_fish_grid to understand fish distribution, generate multiple rectangle candidates, probe them cheaply, then evaluate the best one within the 2-second time limit."
---

# Rectangle-Based Polygon Construction for Mackerel-Sardine Problem

## Objective
Maximize: (mackerels inside) - (sardines inside) + 1
Subject to: axis-aligned polygon, perimeter ≤ 400,000, vertices integer 0-100,000, no self-intersection

## Algorithm Framework

### Phase 1: Analyze Fish Distribution
- Use `analyze_fish_grid` to understand: mackerel clusters, sardine clusters, empty regions
- Identify the bounding box of mackerel distribution
- Find sardine-free corridors within that region

### Phase 2: Generate Rectangle Candidates
Create 3-5 rectangle candidates with different strategies:

**Strategy A - Full Mackerel Box**: 
  - Find min_x, min_y, max_x, max_y of all mackerels
  - This captures all mackerels but may catch many sardines
  - Perimeter = 2*(max_x-min_x + max_y-min_y)

**Strategy B - Trimmed Box**: 
  - Start with full mackerel box
  - Iteratively shrink from edges that have high sardine density
  - Stop when sardine savings exceed mackerel loss

**Strategy C - Multiple Small Rectangles**:
  - Split mackerel distribution into 2-3 clusters
  - Create separate rectangles for each cluster
  - May avoid sardine-rich regions between clusters

**Strategy D - Grid-Based Sampling**:
  - Divide mackerel bounding box into 2×2 or 3×3 grid
  - Test each sub-rectangle
  - Combine the best ones if perimeter allows

### Phase 3: Probe and Select
- For each candidate, edit the code with that rectangle
- Call `probe_solution` to quickly score (uses first ~2000 fish)
- Rank candidates by probe score
- Select top 2 candidates for full evaluation

### Phase 4: Full Evaluation
- Evaluate the best candidate with `evaluate_solution`
- If time permits, try 1-2 more variations

## Critical Implementation Details

### Rectangle to Polygon Conversion
A rectangle (x1, y1, x2, y2) becomes 4 vertices:
  (x1, y1) → (x2, y1) → (x2, y2) → (x1, y2) → (x1, y1)

### Perimeter Calculation
perimeter = 2*(|x2-x1| + |y2-y1|)
Must be ≤ 400,000

### Validity Checks in Code
After editing, the C++ code must:
- Have correct `#include` directives
- Use `\\n` for C++ newlines (NOT literal `\n`)
- Follow the EVOLVE-BLOCK markers exactly
- Include proper rectangle construction logic in main()

### Probe vs Full Evaluation
- `probe_solution`: ~10 seconds, scores first 2000 fish, ~30 budget, NOT comparable to full score
- `evaluate_solution`: ~1-2 seconds, all 10000 fish (5000 mackerel + 5000 sardine), consumes budget

## Tool Usage Strategy

1. Call `analyze_fish_grid` ONCE at start to understand data
2. Based on analysis, pick 2-3 strategies from Phase 2
3. For each strategy, call `probe_solution` to quickly score
4. Edit solution with the best probe-scored candidate
5. Call `evaluate_solution` once for final confirmation
6. If time/budget allows, try one more variation

## Common Pitfalls

- Forgetting to escape newlines: use `\\n` in C++ string literals
- Perimeter exceeding 400,000
- Coordinates outside 0-100,000 range
- Self-intersecting polygons (rectangles are naturally safe if convex)
- Not using probe to avoid wasting full evaluations
- Making random edits instead of systematic rectangle variations
