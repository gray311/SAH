You are an expert in harmonic analysis and optimization. Your task: find a step function h: [0,2]→[0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k))dx.

TARGET: Achieve combined_score > 1.0 (i.e., c5_bound < 0.380923)

KEY INSIGHT: This is a combinatorial pattern search problem, not a gradient descent problem. The seed's multi-restart Adam gets stuck in local optima.

STRATEGY: Directly construct candidate step functions using discrete patterns, then optimize just those patterns. Do NOT rely solely on gradient-based search.

CONCRETE PATTERNS TO TRY:
1. Two-step patterns: h=1 on [0,a], h=0 elsewhere (adjust to satisfy integral=1)
2. Three-step symmetric patterns: h=a on [0,b], h=c on [b,d], h=a on [d,2]
3. Five-step patterns: More complex piecewise constant functions
4. Waveform-based: sin/cos compositions with sigmoid activation
5. Concentrated mass: h concentrated on small intervals to reduce overlap

EXECUTION:
- Use the gen_step_function tool to generate candidate patterns
- Evaluate each pattern's c5_bound directly
- For promising patterns, run brief optimization to refine
- Compare against baseline 0.380923

CONSTRAINTS: h in [0,1], integral from 0 to 2 of h(x)dx = 1.0 exactly
