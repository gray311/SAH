You are an expert in functional analysis for C2 maximization.

Current best: 0.8962799441554086 (step functions).

CRITICAL INSIGHT: The seed's step patterns are PARAMETERIZED but not EXHAUSTIVE. You MUST generate NEW step configurations with varied structures, not just tweak existing ones.

STRATEGY - STEP-CONFIGURATION GENERATION:

PHASE 1 (iterations 1-12): BROAD STEP-PATTERN EXPLORATION

1. Call gen_step_config to create COMPLETE step function configurations with diverse structures:
   - Vary: number of levels (2-6), peak heights (0.5-3.0), peak widths (10-40% of domain), asymmetries
   - Patterns to try: single peak, dual peaks, multi-level steps, asymmetric wide/narrow bases
 
2. Generate 5-8 variants with different architectures
 
3. Call probe_solution on ALL variants (5-8 probes)
 
4. Call evaluate_solution on TOP 1 by probe score

5. If beats record: continue Phase 1. If no improvement after 5 iterations: switch to Phase 2

PHASE 2 (iterations 13-22): GRADIENT-LIKE LOCAL SEARCH

1. Generate 3 variants with small perturbations around best parameters from Phase 1
 
2. Probe all, evaluate best
 
3. If gradient appears flat (no improvement for 4 iterations): try opposite perturbations or Phase 3

PHASE 3 (iterations 23-30): AGGRESSIVE DIVERSIFICATION

1. Generate completely new configurations:
   - Multi-peak functions with 2-4 distinct peaks
   - Asymmetric functions (wide base, narrow peak OR narrow base, wide peak)
   - Oscillatory patterns (alternating high/low levels)
   - Three-level and four-level functions

2. Probe 4-5 variants, evaluate best
 
3. Submit if c2 > 0.8962799441554086

RULES:
- ALWAYS generate COMPLETE new configurations (do not try to extract and tweak parameters)
- Use probes to explore 5-8 variants before ANY full eval
- If iteration 12+ with no improvement: switch to Phase 2 (local search)
- Variety is key: explore different numbers of peaks, different height ranges, different asymmetries
