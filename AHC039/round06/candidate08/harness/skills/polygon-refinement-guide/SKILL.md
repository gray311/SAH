---
name: polygon-refinement-guide
description: Guide for iterative polygon optimization using bounded loops and local adjustments.
---

# Polygon Refinement Strategy

1. Start Simple: Begin with a bounding box or minimal polygon.

2. Time-Bounded Loop:
   Use chrono::steady_clock to track elapsed time.

3. Local Modifications:
   - Shift one vertex by +/-1 in x or y
   - Keep perimeter and vertex count constraints

4. Validity Checks:
   - Ensure edges are orthogonal
   - Check no self-intersections
   - Verify perimeter <= 400000 and vertices <= 1000

5. The evaluator runs your ENTIRE program including the search loop.
Your search must complete within the time limit.
