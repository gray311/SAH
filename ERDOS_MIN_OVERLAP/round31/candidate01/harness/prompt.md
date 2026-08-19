Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. FIRST, use step_function_generator to create valid step functions with integral=1
   - This tool creates guaranteed constraint-satisfying functions
   - Call it to generate diverse candidates directly
   - Don't rely on the seed's optimizer which has flaws

2. Generate 3-5 diverse step function candidates
3. CALL probe_solution on each to screen (c5_bound < 0.381)
4. Evaluate the best 1-2 candidates
5. If no improvement, try different step function patterns from the generator

KEY INSIGHT: The seed program's optimizer has broken initialization code and may not explore effective regions.
Use step_function_generator to create valid candidates from scratch.
