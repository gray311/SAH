---
name: geometric-construction-playbook
description: A playbook for constructing axis-aligned polygons in the H2 harness. Use this when optimizing a code that builds polygons for point-set coverage.
---

# Geometric Construction Playbook for H2 Harness

## Core Principles

1. **Perimeter Budget is King**: Every unit of perimeter costs. Calculate gain per unit perimeter.
   - Simple rectangle: perimeter = 2*(W+H), covers W*H area
   - Strip: perimeter = 2*height + length, covers strip_area
   - Always ask: "Is the perimeter cost worth the coverage gain?"

2. **Start Simple**: A single bounding-box rectangle is your baseline.
   - If it scores < expected, complexity won't help
   - Only add complexity if baseline is already strong

3. **Cluster-Aware Construction**:
   - Identify dense mackerel regions using KD-tree or simple binning
   - Build polygons around these clusters
   - Avoid sardine-dense areas (check during planning)

4. **Perimeter-Efficient Shapes**:
   - Larger rectangles > multiple small rectangles (less total perimeter)
   - Nested rectangles > disjoint rectangles (may share boundaries)
   - Rectangles with small holes only if sardines are very concentrated

5. **Validation Checklist Before Full Eval**:
   - Does perimeter ≤ 400,000? (calculate: 2*sum of edge lengths)
   - Are vertices ≤ 1000? (count vertices in output)
   - Are edges axis-aligned? (check adjacent vertices have diff in only one coord)
   - Is it simple? (no self-intersections, use winding number or ray casting)
   - Output format correct? (first line: m, then m lines of x y pairs)

6. **Iterative Strategy**:
   a. Probe: Try 3-4 different geometric approaches, rank with analyze_rectangles
   b. Evaluate: Full eval on top 1-2 candidates
   c. Refine: If score improves, analyze what changed and why
   d. Pivot: If no improvement in 2 tries, try fundamentally different approach

## Common Geometric Approaches

### Bounding Box
  Pros: Simple, captures all mackerels in region
  Cons: Likely captures many sardines, perimeter might exceed limit
  Best for: When mackerels form a tight cluster

### Horizontal/Vertical Strips
  Pros: Can target specific rows/columns of mackerels
  Cons: May miss mackerels between strips, complex to optimize
  Best for: When mackerels form linear patterns

### Nested Rectangles
  Pros: Can avoid sardine-rich areas by subtracting regions
  Cons: More vertices, more perimeter cost
  Best for: When sardines are concentrated in known areas

### Convex Hull Approximation
  Pros: Tightly fits mackerel distribution
  Cons: May need many vertices, complex to construct axis-aligned
  Best for: Irregular mackerel distributions

## Debugging Invalid Output

If validity=0 (score 0), check:
1. Perimeter exceeded? (print sum of edge lengths)
2. Vertices > 1000? (count vertices)
3. Self-intersection? (debug polygon rendering)
4. Output format error? (check exact format, escape sequences)
5. Compilation error? (check missing includes, syntax errors)

## Time Budget (1.95s per eval)

- KD-tree construction: O(N log N) ≈ 5000*13 ≈ 65,000 ops (fast)
- Polygon area calculation: O(m) for m vertices
- Fish query: O(N) or O(m*log N) with KD-tree
- Total should be < 0.1s for reasonable approaches

Avoid:
- Exhaustive search over vertex positions
- Generating >100 candidate polygons per eval
- Complex geometric operations (convex hull, Delaunay)

## Using the Analyze Rectangles Probe

The probe tool computes approximate scores on ~2000 fish.

**Workflow:**
1. Draft geometric approach A (e.g., single rectangle through cluster)
2. Draft geometric approach B (e.g., two nested rectangles)
3. Draft geometric approach C (e.g., strip decomposition)
4. Call analyze_rectangles for each → get probe scores
5. Keep top 2 candidates
6. Call evaluate_solution on each → get real scores
7. If one wins, refine that approach. If tied, try more targeted edits.

**Probe Score Interpretation:**
- 4000+: Excellent, proceed to full eval with confidence
- 2000-4000: Worth investigating with full eval
- <1000: Likely invalid or poor coverage, reconsider approach
- 0: Invalid, check constraints
