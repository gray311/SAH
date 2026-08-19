You are an expert in functional analysis and mathematical optimization for the C2 constant.

Current best: 0.8962799441554086 (achieved by step functions).

SEED SCORE: 1.042 - The seed's step patterns are promising. Systematically explore step-function space with VALID edits.

STRATEGY - SYSTEMATIC STEP-FUNCTION SEARCH:

PHASE 1 (iterations 1-12): STRUCTURED STEP-VARIATION
1. From current best, generate 3 variants with controlled mutations:
   - Height: +/-10% on selected steps
   - Position: +/-5% on selected boundaries  
   - Width: +/-10% on selected intervals
2. Use probe_solution on ALL 3 variants
3. Use evaluate_solution on TOP 2 by probe score
4. Update best and generate fresh variants (don't mutate same code repeatedly)

PHASE 2 (iterations 13-24): COMBINATORIAL EXPLORATION
1. From Phase 1 best, try COMBINATIONS of mutations
2. Generate 4 variants
3. Probe all, evaluate top 2
4. If no improvement after 5 iterations: switch to Phase 3

PHASE 3 (iterations 25-30): FINETUNING
1. Fine perturbations: +/-3% height, +/-2% position
2. Generate 2 variants, probe, evaluate top 1
3. If stuck: reset to seed, try Phase 1 again

CRITICAL: All edits MUST be valid Python. Use .at syntax correctly: f.at[int(a):int(b)].set(c). Ensure f >= 0.
