---
name: discovery-optimization
description: "Use bipartite_searcher to generate step functions, probe to screen, evaluate best candidates.\nAlways start with bipartite functions - they naturally minimize overlap."
---

# Bipartite Strategy for Erdos C5

## Core Idea
The optimal solution is likely a bipartite (two-level) step function: h(x) = 1 for x < t, h(x) = 0 for x >= t.

## Why Bipartite?
- Simple structure that naturally avoids overlapping with its shifted versions
- The integral constraint is easy to satisfy: integral(h) = t, so t should be ~1.0
- Maximum overlap occurs at small k, but bipartite functions have minimal correlation

## Step-by-Step Workflow

1. CALL bipartite_searcher to generate candidates with different thresholds
   - Try t in [0.7, 1.3] to explore beyond the integral constraint
   - The optimizer can fine-tune the exact values

2. CALL probe_solution on each candidate
   - Screen for c5_bound < 0.382 (cheaper than full eval)
   - Keep candidates with good scores

3. CALL evaluate_solution on the best 2-3 candidates
   - If combined_score > 1.0, finish

4. If no improvement in 3 rounds, try multi-modal patterns
   - Three peaks at different locations
   - Asymmetric distributions

## Key Rules
- START with bipartite_searcher (generate 5-10 candidates)
- Always use probe_solution first
- Evaluate only on candidates with c5_bound < 0.382
- BIPARTITE functions are your best bet for this problem
