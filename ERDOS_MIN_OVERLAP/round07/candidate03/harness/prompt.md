You are an expert in harmonic analysis and optimization. Find a step function h:[0,2]→[0,1] minimizing max_k ∫ h(x)(1-h(x+k))dx.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound. You MUST find c5_bound < 0.380923.

**CONSTRAINTS**: h values in [0,1], ∫₀² h(x)dx = 1 exactly.

**CRITICAL APPROACH**: The seed program uses gradient descent but is STUCK at 0.999641 (c5_bound ≈ 0.380923). DO NOT use gradient descent from random starts.

Instead, use **DIRECT CONSTRUCTION** of piecewise constant functions. Start simple, then refine:

1. First, generate candidate step functions with FEW INTERVALS (e.g., 2-10 steps), exact integral=1.
2. Test these candidates - if combined_score > 1.0, you've succeeded.
3. Only use gradient descent AS A REFINEMENT step after you have a decent construction.
4. Try MANY different constructions before any optimization.

**Construction patterns to try**:
- Single block: h=1 on [0,1], 0 elsewhere (adjust for integral=1)
- Double block: split mass at different positions
- Uniform distribution: h = 1/2 everywhere on [0,2]
- Asymmetric distributions: more mass near center or edges
- Triangular-like: linearly varying step heights

**Use the construct_step_functions tool FIRST** to generate diverse candidates. Then use probe_solution to rank them cheaply before full evaluation.

**Do NOT waste evaluations on** 800-interval random gradient descent from scratch.
