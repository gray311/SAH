You are an expert in harmonic analysis and constructive mathematics. Design step functions h: [0,2]→[0,1] minimizing max_k ∫ h(x)(1-h(x+k))dx.

OBJECTIVE: Maximize combined_score = 0.38092303510845016 / c5_bound. Need c5_bound < 0.38092303510845016.

CONSTRAINTS: h(x)∈[0,1], ∫₀²h(x)dx=1 exactly.

KEY INSIGHT: Seed uses gradient descent which gets trapped. DO NOT rely on it.

CONSTRUCTIVE STRATEGY: Directly design candidate step functions with these patterns:
1) Symmetric bimodal: h=1 on [a,b] and [2-b,2-a], h=0 elsewhere
2) Tri-level step: Divide [0,2] into 3-5 intervals, heights {0,0.5,1}
3) Concentrated mass: h=1 on single interval of length 1
4) Combinatorial search: For 3-7 intervals, enumerate (0,0.5,1)^n

EXECUTION: COMPLETELY REWRITE EVOLVE-BLOCK to remove gradient descent.
Implement direct construction of candidates. For n=50-200, try exhaustive height assignments.
Test 5-20 candidate structures per evaluation. Pick best.

BUDGET: ~30 evaluations. Each must test fundamentally different constructions.
