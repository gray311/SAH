---
name: discovery-optimization
description: "Optimize C++ geometric solver via bounded search. Enforce polygon constraints\n(vertices 4-1000, perimeter <=400k, axis-aligned, no self-intersect). Use\nKD-tree spatial queries. Time-bounded internal search must complete ~1.8s.\nUse probe for ranking variants, evaluate for final scoring."
---

# Geometric Polygon Optimizer Harness

## Task Understanding
You're improving a C++ program that constructs an axis-aligned polygon to maximize
mackerel captures while avoiding sardines. Score = max(0, mackerels - sardines + 1).

## Hard Constraints (score = 0 if violated)
1. Vertex count: 4 <= m <= 1000 (all distinct coordinates)
2. Perimeter: total edge length <= 400,000
3. Edges axis-aligned: each edge has dx=0 or dy=0
4. No self-intersection

## Strategy: Constraint-First, Then Optimize

### Phase 1: Build a Valid Base Polygon
Your C++ must construct a COMPLETE, VALID polygon on first try:
- Start with a simple rectangle (4 vertices)
- OR build an orthogonal polygon with monotone chains
- Ensure all constraints satisfied BEFORE any optimization

### Phase 2: Bounded Internal Search
Implement a search loop with HARD limits:
For i in range(fixed_iterations, e.g., 500-1000):
    Make a small edge perturbation
    Update KD-tree structure if needed
    If time_remaining < 0.3s: break

- Use EXPLICIT iteration counts, not "while time" loops
- Add timer check: if (timer.elapsed() > 1.8) break;

### Phase 3: Score Optimization  
Guide the search toward:
- Expanding toward mackerel clusters (from your point queries)
- Contracting away from sardine-heavy regions
- Trying multiple base rectangles, picking best

## Evaluation Protocol

1. Call edit_solution with one focused change:
   - If perimeter too high: reduce polygon size or simplify shape
   - If too many vertices: merge collinear points
   - If edges not axis-aligned: enforce dx=0 or dy=0
   - If search too slow: reduce iterations or simplify KD-tree

2. Call evaluate_solution to get full score

3. If score 0: diagnose constraint violation from error message
4. If score improved: build on the successful pattern

## Critical Edits (targeted diffs)
- Perimeter: ensure complete calculation, add max check
- Vertices: ensure m >= 4 and m <= 1000
- Self-intersection: can add simple check or simplify polygon
- Time limit: add explicit timer breaks in search loop

## Tool Usage Priority
1. edit_solution: always change something substantive
2. evaluate_solution: after each meaningful edit (not after every minor change)
3. probe_solution: to compare variants before full eval (if implemented)

## Example Search Loop Structure
auto end_time = timer.elapsed_since_start() + 1.8;
while (timer.elapsed() < end_time) {
    // Make ONE small perturbation
    // Check if still valid
    // If time near limit, stop early
}
