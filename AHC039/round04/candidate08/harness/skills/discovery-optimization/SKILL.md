---
name: discovery-optimization
description: "Geometric optimization harness for constructing axis-aligned polygons to maximize\nmackerel capture minus sardine capture, with strict perimeter and vertex budget constraints."
---

# Geometric Polygon Construction Harness

## Problem Understanding

You are optimizing C++ code that constructs an axis-aligned polygon (edges parallel to
x/y axes) to maximize: max(0, mackerels_inside - sardines_inside + 1)

**Hard constraints** (violations = invalid score):
- Vertices ≤ 1000
- Perimeter ≤ 400,000
- All edges must be horizontal or vertical
- No self-intersections

## Search Strategy: Geometric Construction with Perimeter Budgeting

### Phase 1: Analyze the Data Distribution
Use KD-tree (already in code) to understand where mackerels and sardines cluster.
Look for:
- Large mackerel-dense, sardine-sparse regions
- The bounding box of all mackerels

### Phase 2: Start Simple, Build Complexity

**Level 1: Single Rectangle (baseline)**
- Create axis-aligned rectangle enclosing many mackerels
- Calculate: perimeter = 2*(width + height), check if ≤ 400,000
- This is your baseline to beat

**Level 2: Strips**
- Horizontal or vertical strips through mackerel clusters
- Calculate perimeter cost vs gain for each strip

**Level 3: Multiple Nested Rectangles**
- Combine rectangles that don't overlap or overlap minimally
- Total perimeter = sum of all rectangle perimeters (simplify for memory)

**Level 4: Hole-Punched Shapes**
- Large rectangle minus smaller rectangles around sardines
- More complex but can achieve higher scores

### Phase 3: Perimeter-Efficient Edits

Before adding complexity, ask:
1. "Does this add perimeter cost?" If yes, is the gain worth it?
2. "Can I achieve similar coverage with less perimeter?" (e.g., larger rectangle instead of multiple small ones)
3. "Am I creating self-intersections?" (check vertex order, simple polygon property)

### Phase 4: Iterative Refinement

Use the analyze_rectangles probe to:
- Test 3-5 different geometric approaches quickly
- Rank them by score on subsampled data
- Invest full evaluation in the top 1-2 candidates

**When to use analyze_rectangles:**
- After drafting a new geometric approach
- Before spending a full evaluation
- When comparing 2+ similar strategies

## Common Pitfalls

1. **Ignoring perimeter**: Don't design a polygon that exceeds 400,000. The validator will reject it.
2. **Self-intersections**: Vertices must be ordered to form a simple polygon. Clockwise or counterclockwise, but no crossing edges.
3. **Over-complexity**: A single well-placed rectangle can beat a complex multi-hex shape if it stays within constraints.
4. **Wasting evaluations**: Use probes first. With only 20 evals, each must advance your best score.

## Editing Strategy

- **Small changes**: Targeted SEARCH/REPLACE on specific functions (e.g., polygon constructor)
- **Large changes**: Full rewrite of the geometric approach
- **Always verify**: Check that the edited code still outputs valid polygon format

## When You're Stuck

1. Try a COMPLETELY different geometric approach (e.g., if you've done rectangles, try strips)
2. Simplify: Does a simpler shape (fewer vertices) work?
3. Check constraints: Are you failing because of invalid output, not poor score?
4. Use analyze_rectangles on 5+ approaches, pick winner, evaluate

## Success Metrics

- Score ≥ 5000 on ALL test cases (perfect: all mackerels, no sardines)
- Score ≥ 4000 indicates good geometric construction
- Score < 1000 suggests invalid output or poor coverage
- Score = 0 means INVALID (constraint violation or crash)
