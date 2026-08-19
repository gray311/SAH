You are an expert in harmonic analysis and mathematical construction. Your task is to find a step function h: [0,2]→[0,1] with ∫h=1 that minimizes max_k ∫h(x)(1-h(x+k))dx.

**THE OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound (need >1.0)

**CRITICAL INSIGHT**: The seed program's gradient-based optimizer with 12 initializations is trapped in local optima. Do NOT rely on tweaking the optimizer. Instead, use the construct_solution tool to manually build high-quality step function candidates.

**STRATEGY**: 
1. Use construct_solution to create explicit step functions with controlled breakpoints
2. Try: single-step (h=1 on [0,1]), double-step patterns, asymmetric steps
3. Try: concentrated mass patterns (high value on small interval, zero elsewhere)
4. Try: symmetric patterns around x=1
5. For each candidate, call evaluate_solution to get exact score
6. Track best combined_score across all candidates

**CONSTRAINTS**: h∈[0,1], ∫h=1 over [0,2]. The construct_solution tool handles normalization.

**BUDGET**: ~30 evaluations. Each construct_solution call builds a complete candidate ready for evaluation.

**AGENCY**: Complete rewrites encouraged. Build solutions from scratch using the construct tool.
