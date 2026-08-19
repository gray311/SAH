---
name: seed-pattern-screening
description: Screen the seed's 15 initialization patterns using compute_analytical_c5. Evaluate only patterns with c5 < 0.37.
---

# Seed Pattern Screening for Erdos Minimum Overlap

## The Seed Has 15 Pre-built Patterns
The seed optimizer's _get_best_initialization generates 15 patterns:
1. Random normal
2. Random uniform (-2,2)
3. Sin/cos combination
4. Scaled normal (scale=1.5)
5. Scaled uniform (scale=2.0)
6. Bipartite (x>0.5 -> 3.0, else -3.0)
7. Bipartite (x<1.0 -> 3.0, else -3.0)
8. Scaled normal (scale=0.5)
9. Bipartite (x<2/3 -> 3.0, else -3.0)
10. Bipartite (0.5<=x<1.0 -> 3.0, else -1.0)
11. Bipartite (0.25<=x<=1.75 -> 2.5, else -2.5)
12. Golomb ruler (marks at 0.0, 0.4, 0.8, 1.2, 1.6)
13. Bipartite (x<0.6 -> 3.0, else -3.0)
14. Tri-modal (3 peaks at 0.4, 1.0, 1.6)
15. Random normal + noise

## Screening Workflow
1. FOR EACH PATTERN, generate latent and compute h = sigmoid(latent)
2. CALL compute_analytical_c5 for each pattern
3. RECORD c5_bound for each
4. SELECT patterns with c5 < 0.37 for full evaluation
5. CALL evaluate_solution on selected patterns

## Golomb Ruler Optimization
The seed's Golomb pattern (pattern 12) uses 5 marks. You can improve by:
- Using 7 marks: [0.0, 0.35, 0.7, 1.05, 1.4, 1.75, 2.0] (but 2.0 is at boundary)
- Adjusting spacing for 5 marks: [0.0, 0.4, 0.8, 1.2, 1.6] or [0.0, 0.45, 1.0, 1.45, 1.9]

## Expected Success Rate
With compute_analytical_c5, you should identify 1-3 patterns with c5 < 0.37.
Evaluate those with evaluate_solution. Combined score > 1.0 means success.
