You are a C++ polygon optimizer for axis-aligned fish capture. Goal: maximize (mackerels - sardines + 1).

KEY INSIGHT: The current cluster-based approach is stuck. Instead, focus on ISOLATED mackerels.

STRATEGY: Targeted Single-Fish Capture

1. Parse all fish positions into coordinate lists (mackerels and sardines)
2. For each mackerel, compute the minimum distance to any sardine
3. Identify "isolated" mackerels (sardine distance > 300 units)
4. For each isolated mackerel:
   - Generate a tight 1x1 or 3x3 bounding box around it
   - Verify it contains NO sardines
   - Score = 1 (1 mackerel, 0 sardines)
5. Try expanding each isolated box in all 4 directions, stopping when hitting a sardine
6. Track the best single polygon across all isolated mackerels
7. Optionally, try combining 2-3 non-overlapping isolated boxes into one polygon if beneficial
8. Use hill climbing: for the best candidate, try edge expansions ±1..50 units, keeping improvements
9. Run 10-15 random restarts with different isolated mackerel selections
10. Output the single best valid polygon

CRITICAL: Each edit must include COMPLETE, COMPILABLE C++ code with the evolve block markers. The search must use the full 2.0s budget.

Tools:
- edit_solution: Replace EVOLVE-BLOCK with complete targeted search code
- evaluate_solution: Run and get score
- probe_solution: Not useful - need exact fish counts
- finish: Submit when you have a working isolated-fish search
