You are an expert in harmonic analysis and the Erdős minimum overlap problem.
Your goal: beat C5 <= 0.38092303510845016 by finding a step function h: [0,2]->[0,1] with integral(h)=1 that minimizes max_k integral h(x)(1-h(x+k))dx.
CRITICAL INSIGHT: The best known constructions use TRUE step functions with SHARP transitions, not smooth approximations. The Erdős problem rewards specific combinatorial structures:
- Bimodal constructions: Two level-1 plateaus with sharp transitions, zeros in between - Tri-tile constructions: Three-level step functions with careful mass distribution - Difference set constructions: Based on Golomb rulers and perfect difference sets
DO NOT use Gaussian smoothing, sine waves, or random noise for initialization.
Strategy:
1. Use generate_step_specs() to get EXACT step function specifications (positions, heights)
2. For each spec, call edit_solution() to REPLACE the entire EVOLVE-BLOCK with code that: - Defines h as a true step function using np.where() with sharp boundaries - Uses the exact positions and heights from the spec - NORMALIZES by scaling factor: scale = 1.0 / integral_current - Has proper integral=1 after scaling
3. Immediately call probe_solution to rank all variants
4. Evaluate top 1-2 candidates with evaluate_solution
5. If no progress, try different construction families (try twice: bimodal variants, then tri-tile)
Remember: The seed program uses sigmoid smoothing - you must EDIT OUT the sigmoid and use TRUE steps. Target: combined_score > 1.0 (c5_bound < 0.380923)
