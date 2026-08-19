You are an expert in harmonic analysis and mathematical construction. Your task is to find step functions h: [0,2]→[0,1] with ∫h=1 that minimize max_k ∫h(x)(1-h(x+k))dx.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound. Target: >1.0 (c5_bound < 0.380923)

**CRITICAL INSIGHT**: The seed's gradient-based optimizer is trapped in local optima. You must use **explicit construction strategies**, not gradient descent.

**STRATEGY**: Construct piecewise constant functions directly, then evaluate. Try:

1. **Symmetric binary patterns**: h=1 on symmetric intervals, h=0 elsewhere (adjust height for ∫h=1)
   - e.g., h=0.5 on [0,0.4]∪[1.6,2], h=0 elsewhere (integral=0.8, scale to 1)
   - e.g., h=1 on [0.25,0.75] (integral=0.5, scale to 1: h=2 on this interval)

2. **Multi-scale constructions**: Combine patterns at different scales
   - Base: single step h=2 on [0,0.5]
   - Refined: add smaller steps to reduce overlaps

3. **Symmetric 3-part patterns**: h=a on [0,a], h=b on [a,1-a], h=a on [1-a,1] with a,b∈[0,1], ab≥1

4. **Fourier-optimal patterns**: Functions whose autocorrelation is concentrated

**CONSTRAINTS**: 
- h must stay in [0,1] (this is hard: some constructions need h>1, which may be invalid)
- ∫h over [0,2] must equal exactly 1
- Test each construction's integral before submitting

**EXECUTION**: 
- Rewrite the EVOLVE-BLOCK with COMPLETE NEW CONSTRUCTION STRATEGIES
- Don't use gradient descent on latent vectors
- Try 5-10 different explicit constructions per evaluation
- Keep code simple: define h as piecewise constant, compute c5_bound directly

**PATTERN LIBRARY** (implement at least 3):
- Single block: h=2 on [0,0.5], 0 elsewhere (integral=1)
- Double block: h=1 on [0.25,0.75] scaled to integral=1
- Symmetric triple: h=a on [0,a] and [1-a,1], h=b in middle
- Concentrated: very narrow high-value regions

Spend 5-10 evals exploring diverse constructions. You likely need to submit 20-30 complete rewrites to find something better than the seed.
