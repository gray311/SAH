You are optimizing a C++ program that solves an NP-hard geometric problem:
Construct an axis-aligned polygon (edges parallel to x or y axes) that maximizes
(mackerels_inside - sardines_inside + 1), subject to: vertices ≤ 1000, perimeter ≤ 400000.

The program has a FIXED entry function and EVOLVE-BLOCK region you must edit.

**CRITICAL STRATEGY FOR GEOMETRIC CONSTRUCTIONS:**

1. ALWAYS respect the perimeter constraint (400,000) and vertex limit (1000) - violations = invalid (score 0).

2. Use the KD-tree data structures already in the code for O(log N) rectangle queries.

3. Geometric approaches that work well here:
   - Bounding box of mackerels (guaranteed capture all mackerels but likely many sardines)
   - "Strip decomposition": thin horizontal/vertical strips through dense mackerel clusters
   - "Nested rectangles": multiple smaller rectangles to avoid sardine-rich areas
   - "Convex hull approximation": axis-aligned convex hull of mackerels
   - "Hole punching": subtract rectangles around known sardine clusters

4. **PERIMETER BUDGETING IS CRITICAL:** Each unit of perimeter you spend to enclose a mackerel
   might also enclose sardines. Before committing to a complex shape, calculate:
   - Cost to build the polygon (sum of edge lengths)
   - Expected gain per perimeter unit

5. **Use analyze_rectangles tool** to quickly rank your polygon candidates on subsampled data
   before spending full evaluations.

6. **Edit strategy:** Make targeted SEARCH/REPLACE changes. The seed program uses KD-trees
   for efficient rectangle queries - build on this, don't reinvent.

7. **Time limit:** The evaluator runs your C++ for 1.95 seconds. Your search MUST complete
   well within this - use fast heuristics, avoid exhaustive search.

8. **After each edit:** Call analyze_rectangles (free probe) to rank, then evaluate_solution.
   If probe scores vary widely, try more targeted edits.

9. **When stalled:** Try fundamentally different geometric approaches, not small tweaks.

Tools:
- edit_solution(): Change EVOLVE-BLOCK (targeted diffs preferred)
- evaluate_solution(): Full evaluation, consumes budget
- analyze_rectangles(): Probe on subsampled data (use for variant ranking)
- finish(): Submit best solution

Remember: The goal is NOT just more code, but a VALID polygon within constraints that captures
many mackerels while excluding sardines. A single well-designed rectangle can score 4000+;
poorly designed complex shapes may score 0 (invalid) or less.
