You are an expert in harmonic analysis and the Erdos minimum overlap problem. Your task is to find a step function h: [0,2]->[0,1] with integral(h)=1 that minimizes max_k integral(h(x)(1-h(x+k)) dx).

CURRENT BEST: 0.38092303510845016 (combined_score = 0.38092303510845016 / c5_bound)
GOAL: Achieve combined_score > 1.0 (c5_bound < 0.38092303510845016)

KEY INSIGHT: The seed program's Adam optimizer is trapped in local optima. You must use structural, non-gradient approaches:

1. Try piecewise constant functions with SPECIFIC breakpoint patterns (not random initializations)
2. Use constructions that satisfy integral(h)=1 EXACTLY
3. Start with simple patterns: h=1 on single interval of length 1, or h=1 on two intervals of length 0.5 each

SEARCH PRIORITY:
- First: Try 3-5 carefully constructed candidate solutions with few intervals (50-200), evaluate each
- Second: Only then attempt gradient-based refinement

Use the new tool analyze_earthys_candidates to see structured suggestions before editing.
