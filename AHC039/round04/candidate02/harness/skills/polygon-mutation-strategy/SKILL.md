---
name: polygon-mutation-strategy
description: Guide how to mutate polygons for the mackerel-sardine fishing task. Focus on exploiting mackerel-rich regions while avoiding sardine clusters through targeted shape modifications.
---

# Polygon Mutation Strategy for Mackerel-Sardine Fishing

## Core Principle
The polygon should be shaped like a "net" that captures mackerels while excluding sardines.
Think of it as carvings in a sea: eat the good fish, avoid the bad.

## Understanding the Fish Distribution
The input gives you N mackerels and N sardines as points.
Visualize:
- Mackerels = tasty prey (want to maximize)
- Sardines = unwanted catch (want to minimize)

## Region Analysis (do this FIRST each iteration)
1. **Boundary analysis**: Which polygon edges are near fish?
   - Near mackerels: GOOD NEWS → extend boundary outward
   - Near sardines: BAD NEWS → retract or indent boundary
   
2. **Density zones**: 
   - "Mackerel corridors": linear arrangements of mackerels → create finger-like extensions
   - "Sardine clumps": grouped sardines → create indentations/cuts around them

3. **Corner analysis**:
   - Convex corners: good for capturing, but may trap sardines
   - Concave corners: better at avoiding, but might miss mackerels
   - Adjust based on what's nearby

## Mutation Operators (pick 2-3 per iteration)

### EXPLOIT OPERATORS (capture more mackerels)

**Operator E1: Boundary Extension**
- Find a polygon edge with mackerels within 50 units
- Extend that edge perpendicular to itself, 50-100 units outward
- Ensure new perimeter + old perimeter ≤ 400000
- Check: does this extend capture more mackerels? Yes.

**Operator E2: Corner Spherization**
- Round a sharp convex corner into a quarter-circle (discretized)
- This can capture mackerels in the "corner region" that were missed
- Only do if sardines aren't nearby

**Operator E3: Finger Creation**
- From an existing edge, extend a "finger" perpendicular to it
- Length: 50-200 units (long enough to reach mackerels)
- Width: keep it narrow (just 2-4 points wide)
- Targets: mackerels in "corridors" or "channels"

### AVOID OPERATORS (reduce sardines)

**Operator A1: Boundary Retraction**
- Find a polygon edge with sardines nearby (within 30 units)
- Retract edge inward by 30-50 units
- Consider retracting asymmetrically to create a "bite" out
- Trade-off: might lose some mackerels, but sardines are worse

**Operator A2: Corner Cut**
- At a convex corner that encloses sardines:
  - Create a concave notch by removing the corner
  - The cut edge should "avoid" the sardine cluster
  - Keeps perimeter roughly similar
- This is often the MOST effective mutation

**Operator A3: Split and Remove**
- If polygon has a compartment that's mostly sardines:
  - Create a narrow cut into that compartment
  - This effectively "removes" the compartment from the interior
  - Watch out for self-intersection

### SHAPE OPERATORS (optimization)

**Operator S1: Tighten**
- Move all edges slightly inward by 1-2 units
- Creates a smaller, more efficient polygon
- Good when "overflow" sardines are on the edges

**Operator S2: Smooth Corners**
- Replace sharp turns with gentle curves
- Use multiple short segments to approximate curve
- Captures fish that are "between edges"

## Mutation Generation Rules
1. Generate 3-5 candidate mutations (mix of E, A, S types)
2. For each, mentally compute: perimeter, vertex count, axis-alignment
3. Discard obviously invalid ones
4. For remaining, validate with the `validate_mutation_candidate` tool
5. Evaluate top 1-2 valid candidates
6. Keep the best result

## Stalled? Try:
- Complete reshape to a simple rectangle or L-shape
- If current shape is complex, simplify first
- Use validation tool aggressively - don't waste evals on invalid polygons
- Remember: score = max(0, m - s + 1), so capturing 1 extra mackerel is worth losing 0 sardines

## Key Insight
The problem is HEURISTIC, not optimization. You won't find perfect solution.
Build a "good enough" net that captures many mackerels and avoids most sardines.
Start simple, then add complexity ONLY if it improves score.
