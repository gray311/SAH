---
name: discovery-optimization
description: "Iteratively optimize C++ polygon construction code for fish catch optimization. Use edit_solution/evaluate_solution/probe_solution to explore the search space efficiently under time and budget constraints."
---

# Polygon Construction Strategy for Fish Optimization

Phase 1: Region Analysis
1. Use input analysis to identify high-net-gain rectangles
2. Identify regions where mackerels exceed sardines
3. Identify regions to avoid (high sardine density)

Phase 2: Candidate Generation
1. Generate polygon variants around promising regions
2. Ensure each candidate has 4+ vertices and perimeter <= 400000
3. Build non-self-intersecting polygons
4. Try unions of multiple rectangles

Phase 3: Rapid Screening
1. Use probe_solution to score top 10-15 candidates
2. Sort by probe score
3. Keep top 3-5 for full evaluation

Phase 4: Refinement
1. For promising candidates:
   - Try small expansions in positive regions
   - Try small contractions in negative regions
   - Use targeted SEARCH/REPLACE edits
2. Validate each variant carefully

Phase 5: Final Selection
1. Evaluate top candidates with evaluate_solution
2. Choose highest valid score
3. Output with finish

Time Budget Discipline
- Total search time: less than 1.9s
- Use fast I/O and efficient data structures
- Time-box each phase: if not advanced by 1.8s: return best
- Avoid O(N^2) operations
