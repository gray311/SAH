You are optimizing a C++ program for an NP-hard geometry problem: construct an axis-aligned polygon to maximize (mackerels inside - sardines inside).

Key constraints: ≤1000 vertices, perimeter ≤400,000, integer coords 0-100000.
Scoring: max(0, mackerels_inside - sardines_inside + 1) averaged over 150 test cases.

Your program has an EVOLVE-BLOCK containing C++ code. You control ONLY this region.

STRATEGY FOR THIS TASK:
1. The seed uses KD-tree + some search. This is correct but needs tuning.
2. A winning solution likely: (a) identifies dense mackerel clusters, (b) builds polygons around them, (c) minimizes sardine overlap.
3. Use the probe_solution tool to cheaply test parameter variations (separate 30-probe budget).
4. Focus on the core algorithm: consider trying (i) greedy expansion from best fish, (ii) cluster-based bounding boxes, (iii) iterative polygon refinement.
5. Ensure every C++ edit compiles and stays within 2.0s per test case.
6. Don't rewrite unrelated code; make targeted changes to the search/algorithm logic.

Use these tools:
- edit_solution: Change EVOLVE-BLOCK (targeted diff preferred)
- evaluate_solution: Full score (limited budget, verify every change)
- probe_solution: Cheap score on subsampled data (~2000 rows) to rank variants fast
- finish: Submit best when done

Think like an algorithm engineer: what would actually improve coverage of mackerels while avoiding sardines?
