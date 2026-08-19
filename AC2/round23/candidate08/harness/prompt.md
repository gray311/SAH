You are an expert in functional analysis for C2 maximization.

Current best: 0.8962799441554086 (step functions).

CRITICAL INSIGHT: The seed program uses a HIGH-RESOLUTION (600 intervals) optimization with hardcoded step patterns. 

STRATEGY - ARCHITECTURE-LEVEL SEARCH:

PHASE 1 (iterations 1-12): STRUCTURAL DIVERSITY EXPLORATION

1. Generate variants by:
   (a) Adding/removing step boundaries (change num_intervals)
   (b) Creating multi-peak patterns (2-4 peaks instead of 1)
   (c) Asymmetric designs (left vs right weighted)
   (d) Narrow vs wide peak experiments

2. Probe ALL variants (aim for 4-6 probes per iteration)

3. Evaluate TOP 1 probe winner

4. If no improvement after 3 iterations: switch to Phase 2

PHASE 2 (iterations 13-22): GRADIENT-FOCUSED OPTIMIZATION

1. Use JAX autodiff on the -c2_ratio objective

2. Generate 2 variants following gradient direction

3. Probe and evaluate best

4. If gradient norm < 0.001 for 5 iterations: switch to Phase 3

PHASE 3 (iterations 23-30): AGGRESSIVE ARCHITECTURE REDESIGN

1. Completely restructure the step function:
   - Try 300 intervals with 5-step patterns
   - Try 900 intervals with narrow multi-peak
   - Try Gaussian-windowed steps (smooth transitions at boundaries)

2. Probe 2-3 architectures, evaluate best

3. Submit if c2 > 0.8962799441554086

RULES:
- Use probes to filter: 4-6 probes before any full eval
- If stuck: try COMPLETELY different architecture, not parameter tweaks
- JAX autodiff enables gradient-based refinement
