---
name: polygon-construction-strategy
description: Playbook for constructing axis-aligned polygons. Focus on region analysis, bounded search, and validity.
---

Phase 1: Run analyze_rectangular_regions to find high-value areas.
Phase 2: Generate polygons around positive regions. Ensure 4+ vertices and perimeter <= 400000.
Phase 3: Use probe_solution for quick ranking of 10-15 candidates.
Phase 4: Refine top 3-5 with targeted edits.
Phase 5: Evaluate best with evaluate_solution and finish.
Time budget: Keep search under 1.9s total. Use O(N) or O(N log N) algorithms.
