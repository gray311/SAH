You are an expert in harmonic analysis and mathematical optimization. Your task is to find a step function h: [0,2]→[0,1] that minimizes the maximum overlap integral, achieving combined_score > 1.0.

**KEY INSIGHT**: This is a combinatorial construction problem. The seed's gradient-based optimizer gets trapped in local optima because it tries to fine-tune continuous latents. You need to CONSTRUCT explicit piecewise-constant functions with few breakpoints.

**PROVEN STRATEGY**: Try simple geometric patterns FIRST:
- Single interval: h=1 on [0,1], h=0 elsewhere (integral=1)
- Two intervals: h=a on [0,x], h=b on [x,2] where ax+b(2-x)=1
- Three intervals: alternating blocks
- Step functions: h=1 on multiple disjoint intervals

**DIVERSITY**: Each evaluation should try a DIFFERENT explicit construction strategy, not just re-run gradient descent from different seeds.

**BUDGET**: ~30 evaluations. Spend the first 10-15 on explicit constructions with few breakpoints. Only use optimization if constructions fail.

**CONSTRAINTS**: h∈[0,1], ∫h=1 over [0,2]
