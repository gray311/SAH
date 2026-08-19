---
name: geometric-construction-playbook
description: Specialized playbook for constructing valid axis-aligned polygons in fish-capture problems. Use when stuck at low scores or when current polygon strategy fails. This playbook guides complete redesigns rather than incremental edits.
---

# Geometric Polygon Construction Playbook

## Phase 1: Data Analysis (MANDATORY FIRST STEP)
Before writing any C++ code, you MUST call analyze_geometric_potential.
- Review the returned bbox values
- Examine mackerel_density: which grid cells have high mackerel concentration?
- Check sardine_locations: where are sardines clustered?
- Read suggested_shapes: what does the tool recommend?

## Phase 2: Choose Construction Strategy
Based on Phase 1 analysis:

### Strategy A: Tight Rectangle (best when sardines are outside mackerel cluster)
- Use mackerel_bbox directly or slightly expanded
- Polygon: 4 vertices at min_x, min_y, max_x, min_y, max_x, max_y, min_x, max_y
- Perimeter: 2 times width plus height must be <= 400000
- C++: read all mackerels, compute min/max x/y, output 4 vertices

### Strategy B: Avoidance Shape (when sardines overlap mackerel area)
- Build polygon that goes around sardine clusters
- Example: Start at top-left, go right past first sardine column, down, left past second, etc.
- Polygon: 6 to 10 vertices tracing around high-density sardine zones
- C++: sort sardines by x, create zigzag polygon that indents at sardine positions

### Strategy C: Plus Shape (for linear or clustered mackerels)
- Central rectangle with 4 arms extending in cardinal directions
- Total 8 vertices: center plus 4 corner adjustments
- Good when mackerels form a cross or plus pattern
- C++: compute center, measure arm lengths in each direction

### Strategy D: Multi-Rectangle Union (for irregular clusters)
- 2 to 4 separate rectangles arranged to capture disjoint mackerel groups
- Output as a single polygon with notches or use approximation
- Caution: may violate simplicity if rectangles too far apart

## Phase 3: Validate Before Submitting
Check your C++ code produces:
1. At least 4 vertices, at most 1000
2. Perimeter calculation <= 400000
3. All coordinates integers in [0, 100000]
4. Axis-aligned edges only (each edge has delta_x equals zero or delta_y equals zero)
5. No self-intersection (simple polygon)

## Phase 4: C++ Implementation Tips
- Use greedy construction: compute bbox or centroid, build polygon directly
- No need for complex search if construction is simple
- Hardcode safe perimeter checks
- Use integer arithmetic only (avoid floating point)
- Time limit: keep entire main function under 1.5 seconds
- Read all fish data in O of N, compute bbox in O of N, output in O of 1 or O of V

## Common Failures to Avoid
- Forgetting axis-alignment: ensure each consecutive pair of vertices shares either x or y
- Self-intersection: don't create twisted polygons
- Perimeter overflow: calculate 2 times width plus height and verify < 400000
- Timeouts: simple construction beats complex optimization here
- Invalid coordinates: clamp all values to [0, 100000]

## Testing Your Strategy
1. Analyze with analyze_geometric_potential first
2. Pick one strategy (don't try all simultaneously)
3. Write minimal C++ that implements just that strategy
4. Evaluate, score approximately 2 to 5 equals valid construction improving on seed
5. Only then iterate within the strategy
