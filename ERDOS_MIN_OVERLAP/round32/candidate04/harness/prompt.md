Erdos C5 Problem: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The seed optimizer uses complex multi-pattern initialization with 14 different patterns. 
This complexity traps the search in local minima.

STRATEGY: 
1. Use SIMPLIFIED initializations that are structurally different from the seed
2. Try BIPARTITE functions (single threshold at various positions)
3. Try TRIMODAL functions (3 distinct peaks)
4. Try SYMMETRIC functions around x=1
5. Use PROBE on simple candidates first, then evaluate only the best

CONSTRAINT: integral(h) = 1 exactly. Use penalty_strength=100 to enforce this.

DO NOT rely on correlation analysis - it doesn't help here. Instead, explore diverse functional forms.
