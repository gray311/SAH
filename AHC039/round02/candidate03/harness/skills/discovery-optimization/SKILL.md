---
name: discovery-optimization
description: "Optimize orthogonal polygon construction for NP-hard fish-catch task. Use grid-based\nor sweeping-line heuristics to build axis-aligned polygons maximizing mackerel minus\nsardine coverage. Always probe variants before full evaluation to stay within budget."
---

# Orthogonal Polygon Construction Strategy

## Task Understanding
- Maximize: (mackerels inside polygon) - (sardines inside) + 1
- Constraints: ≤1000 vertices, ≤400,000 perimeter, axis-aligned edges, integer coords 0-100000
- 150 test cases, 2.0s total time limit per test

## Core Strategy: Grid-Based Rectangle Union with Strategic Cuts

### Phase 1: Bounding Box Initialization
1. Compute the bounding box of ALL fish (mackerels + sardines)
2. Start with a polygon = this bounding box (4 vertices, 4 edges)
3. Evaluate baseline: This captures everything (score = N_mackerel - N_sardine + 1 = 0)

### Phase 2: Sardine Hole Excavation
1. Find sardine clusters (use spatial grouping by coordinates)
2. For each cluster, propose a rectangular "hole" to cut out
3. Validate: hole must not fragment mackerel groups unnecessarily
4. Keep the modification if it improves score

### Phase 3: Mackerel Capture Enhancement
1. After removing sardines, scan for uncovered mackerel-rich regions
2. Add rectangular protrusions or connected regions to capture them
3. Use dynamic programming or greedy: extend in cardinal directions

### Phase 4: Perimeter Optimization
- Share edges between adjacent rectangles
- Minimize "dead" perimeter (edges that don't border fish)
- Use bounding boxes of fish clusters, not individual fish

### Implementation Pattern (C++):
- Use a grid representation (100000x100000 too large → compress by clustering)
- Implement: bounding box → hole-cutting → filling → hill-climbing
- Time budget: leave 0.1s safety margin, aim for 1.8s internal search

## Tool Usage Sequence:
1. edit_solution: Implement new construction strategy
2. probe_solution: Test 5-10 variants of a parameter (hole size, extension direction)
3. evaluate_solution: Confirm the best probed variant
4. Repeat with refined strategy

## Common Mistakes to Avoid:
- Don't output a static polygon - must search internally
- Don't violate perimeter constraint - count all edges!
- Don't create self-intersecting polygons
- Don't ignore the +1 in scoring formula

## When to Use probe_solution:
- After designing a new polygon construction heuristic
- Before committing to full evaluation (saves budget)
- For parameter tuning (hole positions, expansion amounts)

## When to Call finish:
- When you can't improve beyond current best with 2+ evals left
- When score plateaus despite diverse strategies
- When all 150 test cases score consistently
