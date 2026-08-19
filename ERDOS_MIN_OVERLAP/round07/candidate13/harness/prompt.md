You are an expert in harmonic analysis and optimization. Task: find step function h:[0,2]->[0,1] with integral=1 that minimizes max_k integral h(x)*(1-h(x+k)) dx.

OBJECTIVE: Maximize combined_score = 0.38092303510845016 / c5_bound. Target > 1.0.

KEY INSIGHT: Gradient descent fails. CONSTRUCT explicit candidates.

VALIDATION: h in [0,1], integral=1.0.

PATTERNS TO CODE:
1. Single interval: h=1 on [0,1], 0 elsewhere
2. Uniform: h=0.5 everywhere
3. Two bumps: h=1 on [0,0.5] U [1,1.5]
4. Centered scaled: h=2/3 on [0.25,1.75]
5. Four sections: h=0.5 on each quarter

WORKFLOW: Implement ONE pattern, verify integral=1 and h in [0,1], evaluate. Use probe_solution for variants.
