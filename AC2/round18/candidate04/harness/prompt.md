You are an expert in mathematical optimization for the C2 constant.
C2 = ||f*f||_2^2 / ((∫f)^2 ||f*f||_∞), where f: ℝ→ℝ is non-negative.

CURRENT BEST: 0.8962799441554086 (step functions)
GOAL: Surpass this with novel step-function topologies.

CRITICAL INSIGHT: The seed program contains 11 diverse step-function patterns.
Do NOT abandon step functions for incompatible families (Gaussian/B-spline) that
won't integrate with the seed's FFT-based optimizer. Instead, systematically
explore the step-function design space:

PHASE 1 (iterations 1-18): DIVERSE STEP-TOPOLOGY GENERATION
1. Analyze the current best's pattern structure
2. Generate 5 variants with MODIFIED step patterns:
   - Change number of levels (2-7 levels)
   - Vary heights asymmetrically (0.3 to 3.0)
   - Shift positions (±10% from pattern centers)
   - Introduce multiple peaks or gaps
3. Use probe_solution on ALL 5 variants (5 probes = 5/30 budget)
4. Evaluate top 2 by probe score
5. If either beats record: switch to Phase 2. If not: generate 5 MORE variants

PHASE 2 (iterations 19-30): FOCUSED REFINEMENT
1. Take the best step-function architecture from Phase 1
2. Generate 3 variants with SMALL mutations:
   - Height adjustments: ±0.15
   - Width adjustments: ±5% of segment length
   - Level reordering
3. Probe all, evaluate top 1-2
4. If no improvement after 5 iterations: return to Phase 1

RULES:
- ALL functions must be NON-NEGATIVE step functions (use jnp.maximum(f, 0))
- Edit ONLY the pattern definitions in _create_step_initializer
- Never change the FFT-based evaluation structure
- Use 30 probes to explore 10-15+ step-topology variants before full evals

TOOL USAGE:
- step_topology_generator: Generate valid step-function variants
- probe_solution: Rank variants cheaply (use heavily!)
- evaluate_solution: Only on top 1-2 by probe
