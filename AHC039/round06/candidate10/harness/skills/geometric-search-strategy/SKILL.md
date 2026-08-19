---
name: geometric-search-strategy
description: A playbook for constructing axis-aligned polygons to capture mackerels while avoiding sardines. Guides the solver to use spatial analysis, try multiple polygon shapes, and filter variants efficiently.
---

# Geometric Search Strategy for Fish Capture

## Step 1: Analyze the Fish Distribution
Call analyze_fish_distribution ONCE before making any edits.
This tells you:
- Where mackerels cluster (target these regions)
- Where sardines are sparse (expand these regions)
- The overall density ratio (helps gauge potential score)

## Step 2: Choose Polygon Construction Strategies
Try MULTIPLE approaches, not just one:

### Approach A: Rectangular Grid Cells
- Create rectangles around high-density mackerel regions
- Start small, grow until hitting sardine density > threshold
- Example: Find a 200x200 cell with 50 mackerels, 0 sardines

### Approach B: L-Shaped / U-Shaped Polygons
- Capture mackerels in multiple clusters with one connected polygon
- Use the "elbow" to avoid sardine-rich corridors
- Example: Two rectangles connected by a thin bridge

### Approach C: Gap Expansion
- Find sardine-poor corridors between mackerel clusters
- Expand a polygon to fill these gaps
- Example: Start with one mackerel cluster, grow to adjacent low-sardine areas

### Approach D: Multiple Small Polygons
- Create several small polygons in isolated mackerel regions
- Connect them if beneficial, otherwise output separately
- Note: The evaluator expects ONE polygon, so connect them

## Step 3: Implement Efficient Internal Scoring
Inside your C++ program, implement O(vertices × log N) scoring:
- Use KD-tree to query points inside each polygon edge
- For each edge, count fish in the strip
- For complex polygons, use inclusion-exclusion or sweep-line

## Step 4: Use Probe-Based Filtering
When generating multiple variants of a strategy:
1. Generate 5-10 variants
2. Use probe_solution to quickly rank them (no full eval budget spent)
3. Call evaluate_solution only on the top 1-2 variants
4. If none improve, try a different strategy

## Step 5: Respect Time Limits
- The C++ program must complete in <1.95 seconds
- Use early termination: stop generating variants if time runs low
- Prefer simple constructions over complex ones initially

## Step 6: Output the Best Variant
When done:
- Choose the variant with highest (mackerels - sardines + 1)
- Ensure it meets all constraints (vertices ≤1000, perimeter ≤400000, no self-intersection)
- Output in format: m, then m lines of coordinates
