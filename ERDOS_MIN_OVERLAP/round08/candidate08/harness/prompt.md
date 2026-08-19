You are optimizing for the Erdős minimum overlap constant C5.
Goal: Find c5_bound < 0.38092303510845016 to achieve combined_score > 1.0.

**CRITICAL INSIGHT**: The seed's gradient-based Adam optimizer gets trapped in local optima (~0.999641 combined_score). To escape:

1. **Use struct_generate_candidates** to create programs with DIFFERENT ansatz families:
   - Pure step functions (few breakpoints)
   - Sinusoidal mixtures
   - Piecewise constant with 2-5 segments
   - Non-gradient optimization (GA, SA)

2. **Strategy**: Generate 3-5 diverse candidates, evaluate top 2-3, then refine the best.
