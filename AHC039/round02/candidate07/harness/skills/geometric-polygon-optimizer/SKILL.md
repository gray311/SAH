---
name: geometric-polygon-optimizer
description: Expert strategy for axis-aligned polygon optimization on mackerel-sardine tasks. Uses probing to rank variants, implements iterative local search, ensures all constraints are met before final submission. Critical for beating the seed score.
---

# Axis-Aligned Polygon Optimization Protocol

## Understanding the Task
You are building a polygon to enclose mackerels while avoiding sardines.
Score = max(0, mackerel_count - sardine_count + 1).
Constraints: axis-aligned edges, <=1000 vertices, perimeter <=400,000.

## Step-by-Step Protocol

### Step 1: Initial Analysis (MUST DO FIRST)
- Call analyze_points to see fish distribution
- Note mackerel bounding box vs sardine bounding box
- Identify overlap regions (avoid these for edges)

### Step 2: Base Construction
- Start with a rectangle covering mackerel-dense area
- Use the bounding box of mackerels as your base
- Extend minimally to capture edge mackerels
- Ensure perimeter < 400,000 (check with compute_polygon_metrics)

### Step 3: Probing Loop (CRITICAL)
For each potential improvement:
  1. Edit: Try one mutation (extend edge, cut corner, shift boundary)
  2. Probe: Call probe_solution to get approximate score
  3. Decide: Keep if probe score improves, discard otherwise
  4. Repeat: Try different mutations on promising variants
After 5-10 probes: Full-evaluate the top 2-3 variants

### Step 4: Local Search Refinement
For each candidate that passed probing:
- Try extending edges toward mackerel clusters
- Try cutting off sardine-heavy corners
- Try tightening the polygon around mackerel cores
- Always re-check perimeter constraint after each edit

### Step 5: Final Validation
- Ensure no diagonal edges (all horizontal or vertical segments)
- Verify vertex count <=1000 and perimeter <=400,000
- Confirm no self-intersections
- Call finish with your best variant

## Common Pitfalls
- Do not rewrite the whole EVOLVE-BLOCK for small changes
- Do not call evaluate_solution more than 3-4 times unless necessary
- Do not create non-axis-aligned edges (this violates constraints)
- Do not ignore the probe tool - it is your friend!
- Do not make edits that break the C++ compilation
- Always check perimeter after modifying edges
