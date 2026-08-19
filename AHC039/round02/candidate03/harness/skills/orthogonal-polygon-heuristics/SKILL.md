---
name: orthogonal-polygon-heuristics
description: Expert playbook for orthogonal polygon construction - grid-based rectangle unions, hole-cutting for sardines, perimeter-efficient expansions. Use when building initial solutions or refining after edit/evaluate loops. Critical for tasks requiring axis-aligned polygons with bounded perimeter.
---

# Orthogonal Polygon Heuristics for NP-Hard Covering Tasks

## 1. Initial Construction: Bounding Box with Strategic Cuts

Start with a single axis-aligned rectangle covering all fish. Then:

a) Identify sardine clusters:
   - Sort sardines by x-coordinate
   - Find dense clusters (within same x-strip of width ~1000)
   - For each cluster, propose a rectangular "hole" to cut out
   - Hole parameters: x_min, x_max, y_min, y_max (all aligned to grid)

b) Hole-cutting optimization:
   - Calculate new perimeter: original_perimeter - shared_edges + new_edges
   - Ensure hole doesn't isolate mackerel groups (check connectivity)
   - Validate: hole must not self-intersect or create invalid polygons

c) Perimeter budget management:
   - Budget: 400,000 total perimeter
   - Each new hole adds approximately: 4 * (hole_width + hole_height)
   - Each protrusion adds: 4 * (protrusion_width + protrusion_height)
   - Rule of thumb: keep new features under 20,000 perimeter each

d) Mackerel capture enhancement:
   - After hole-cutting, find uncovered mackerel-rich regions
   - Add rectangular protrusions or connected sub-regions
   - Use greedy extension: from cluster center, grow in 4 cardinal directions

## 2. Perimeter-Aware Construction

CRITICAL: Every edge counts toward the 400,000 budget.

Strategy: Use bounding boxes of fish CLUSTERS, not individual fish.
This reduces vertex count and shares edges between adjacent regions.

Steps:
1. Cluster fish by proximity (e.g., using grid with cell size 5000)
2. For each cluster, compute its bounding box
3. Union overlapping bounding boxes (merge shared edges)
4. Result: fewer vertices, shared perimeter, better score

## 3. Time-Bounded Internal Search

Your C++ program must implement a SEARCH LOOP:

- Phase 1 (0.3s): Build initial polygon (bounding box of all fish)
- Phase 2 (0.5s): Hill-climbing with greedy extensions
  * Try extending in each cardinal direction
  * Keep extension if it improves (mackerels - sardines)
- Phase 3 (0.5s): Local optimization
  * Test small moves (shift vertices, extend edges)
  * Accept improvements, reject deteriorations
- Phase 4 (0.4s): Final validation and output
  * Check all constraints (vertices ≤ 1000, perimeter ≤ 400000)
  * Output final polygon in required format

Total: 1.7s internal search, 0.2s safety margin

## 4. Common Mistakes

- Static polygon output: MUST search internally
- Perimeter overflow: count ALL edges, including shared ones
- Self-intersection: validate polygon validity before output
- Wrong scoring: formula is (mackerels - sardines + 1), NOT just difference
- Time limit exceeded: always leave 0.1s buffer in internal search

## 5. When to Apply Each Technique

- Bounding box initialization: Always first step
- Hole-cutting: When sardines are concentrated in regions
- Protrusion expansion: When mackerels are in clusters outside current polygon
- Cluster union: When many fish form dense groups
- Hill-climbing refinement: After any major construction change"
