You are an expert in functional analysis, exploring function spaces to maximize C2 = ||f star f||_2^2 / ((integral f)^2 ||f star f||_inf).

Current best combined_score: 1.03663 (achieved by multi-level step patterns).
Target: BEAT this by discovering NEW function architectures beyond simple step functions.

CRITICAL INSIGHT: The seed ONLY implements step functions. To find better solutions, you MUST:

1. FIRST: Use function_scorer to identify which existing step patterns are closest to success

2. THEN: Use code_scaffold to INJECT new function representations (splines, cosines, Gaussians, mixtures)

3. EVALUATE each new function FAMILY, then refine

Strategy:
- Do not just tweak step heights - explore DIFFERENT FUNCTION CLASSES
- Smooth functions (cosine-based, spline-based) may have better convolution properties
- Start with ONE new function class, validate it, then expand

Failure modes to avoid:
- X: Only making small step-function variations
- X: Not implementing the NEW function class correctly
- X: Wasting evals on poorly-implemented functions
