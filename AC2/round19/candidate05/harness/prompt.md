You are optimizing C2 = ||f★f||₂² / ((∫f)² ||f★f||_∞) for non-negative f: ℝ→ℝ.

BEST KNOWN: 0.89628 (step functions).

CRITICAL: The seed's step patterns ARE the right direction. Don't abandon them for Gaussians/splines.

YOUR STRATEGY - STEP-FUNCTION SPACE EXPLORATION:

PHASE 1 (iterations 1-12): DIVERSE STEP-VARIANT DISCOVERY
1. Analyze current best's structure (note peak positions, height ratios, support width)
2. Generate 3-5 STEP-FUNCTION variants with DIFFERENT:
   - Peak/step positions (try 0.2-0.8 range variations)
   - Height configurations (try 1.3-2.5 range)
   - Number of levels (2-6 levels)
   - Asymmetry (shift left/right support)
3. For each variant: use probe_solution first (cheap, separate budget)
4. Only full-evaluate TOP 2 by probe score
5. If both fail probe > 1.0: generate fresh variants (don't mutate further)

PHASE 2 (iterations 13-30): PRECISION STEP TUNING
1. Take best architecture from Phase 1 (if it beat record)
2. Make SMALL targeted mutations:
   - Height: +/-0.1 per level
   - Positions: +/-2% of interval count
   - Add/remove ONE level
   - Slight asymmetry adjustment
3. Probe all variants, evaluate top 1
4. If stuck for 3 iterations: restart Phase 1 with new random seeds

KEY RULES:
- STAY IN STEP-FUNCTION SPACE - it's the current champion
- ALWAYS PROBE BEFORE FULL EVAL (use 30 probe budget aggressively)
- If probe < 1.0, SKIP full eval and try next variant
- After iteration 10: if no improvement, generate COMPLETELY NEW step patterns (not mutations)
- Use all 30 probes to explore 15-20 variants before exhausting full evals
