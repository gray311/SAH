Erdos minimum overlap (C5): Find h: [0,2]->[0,1] with integral(h)=1 minimizing max_k integral h(x)(1-h(x+k))dx.

Current best: C5 <= 0.38092303510845016 (combined_score=1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL STRATEGY: The seed optimizer has 15 initialization patterns. Most successful candidates come from MUTATING these patterns:
1. START with num_restarts=1, num_steps=30000 to quickly test individual patterns
2. USE pattern_mutation_generator to create SPECIFIC variants: Golomb (4-5 marks), Tri-modal (3 peaks), Bipartite
3. For each variant, normalize integral=1 BEFORE evaluation
4. Use probe_solution to filter (keep c5_bound < 0.375)
5. Only evaluate candidates with combined_score > 0.9995 after full training

PATTERN INSIGHTS:
- Golomb ruler (equally spaced marks): marks at 0, 0.4, 0.8, 1.2, 1.6 minimize overlap
- Tri-modal (3 narrow peaks at 0.4, 1.0, 1.6) with proper width
- Bipartite (step at 0.5): [0, 0.5) high, [0.5, 2] low

BEST APPROACH: Call pattern_mutation_generator ONCE to get 3-4 pattern variants with integral-checked candidates, then evaluate each with num_restarts=1, num_steps=30000.
