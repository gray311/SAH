You are optimizing for the Erdős minimum overlap constant C₅.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound
where c5_bound = max_k ∫₀² h(x)(1-h(x+k))dx

**CONSTRAINTS**: h: [0,2] → [0,1], ∫₀² h(x)dx = 1 exactly

**CRITICAL INSIGHT**: The optimal h is likely a piecewise constant function with FEW breakpoints (3-7 regions). Gradient descent on 800-dimensional latent spaces consistently fails because:
- The landscape has many bad local optima
- Sigmoid relaxation doesn't produce sharp step functions well
- The integral constraint is hard to satisfy with continuous optimization

**STRATEGY**: Use the construct_piecewise tool to build explicit candidates:
1. Start with 3-5 intervals, assign heights in [0,1]
2. Scale heights to satisfy ∫h = 1 exactly
3. Try different breakpoint configurations (e.g., [0,1], [1,1.5], [1.5,2])
4. Evaluate each candidate
5. Only use gradient-based refinement if construction succeeds

**BUDGET**: ~30 evaluations. Each construction+eval is one eval.

**FORMAT for construct_piecewise**: Specify intervals as [(start, end, height), ...]
The tool will return the computed c5_bound directly.
