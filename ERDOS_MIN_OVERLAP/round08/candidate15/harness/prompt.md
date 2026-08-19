You are an expert in harmonic analysis and mathematical optimization.

**THE OBJECTIVE**: Find a step function h: [0,2]→[0,1] with ∫h=1 that minimizes
c5_bound = max_k ∫ h(x)(1-h(x+k))dx

Then maximize combined_score = 0.38092303510845016 / c5_bound

**CONSTRAINTS**: h∈[0,1], ∫_0^2 h(x)dx = 1 exactly

**STRATEGY**: Try these concrete families of step functions:

1. **Single-block**: h=1 on [0,1], h=0 elsewhere (c5_bound ≈ 0.333)
   - This should give combined_score ≈ 1.14 (> 1.0!)

2. **Two-block symmetric**: h=α on [0,b]∪[2-b,2], h=0 elsewhere

3. **Three-block symmetric**: h=α on [0,a]∪[1,b]∪[2-b,2]

4. **Optimized breakpoints**: Coarse grid (20-50 intervals), optimize positions, refine to 800.

**Key insight**: The seed uses 800 intervals and Adam which gets trapped. Try simpler constructions first.

**BUDGET**: ~30 evaluations. Each edit should be a complete, runnable program.
