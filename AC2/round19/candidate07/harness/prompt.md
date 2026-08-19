You are an expert in functional analysis optimizing C2. Current best: 0.89628.
SEED SCORE: 1.042 (combined_score = c2/0.89628). The seed uses piecewise step functions.
CRITICAL: Most code generation attempts fail because they try to generate complex architectures too soon.
SOLUTION: TWO-STAGE STRATEGY

PHASE 1 (iterations 1-12): SIMPLE STEP-VARIANT EXPANSION
1. Analyze the current best's step pattern using analyze_convolution_profile
2. Generate EXACTLY 3 variants by MODIFYING the seed's step pattern:
   - Adjust heights (±10%), shift positions (±15%), add/remove one level
   - Keep the same number of levels and basic structure
   - Ensure f(x) >= 0 and numerically stable
3. Probe ALL 3 variants (3 probes)
4. Evaluate the TOP 1 by probe score (1 eval)
5. Repeat until iteration 12 or you find a variant with probe_score > 1.0

PHASE 2 (iterations 13-20): ARCHITECTURE EXPANSION (ONLY IF PHASE 1 SUCCEEDS)
1. Take the best Phase 1 winner
2. Generate 2 variants that ADD complexity: add one level, split one level, or adjust spacing
3. Probe both, evaluate top 1
4. If no improvement after 2 iterations: STAY in Phase 1 and try different mutations

PHASE 3 (iterations 21-30): RADICAL REDESIGN (ONLY IF ALL ELSE FAILS)
1. Switch to a COMPLETELY different family (Gaussian mixture, piecewise-linear)
2. Generate ONLY ONE simple variant from that family (not 5!)
3. Probe it, and if probe_score > 1.0, evaluate
4. Otherwise, return to Phase 1 with fresh step variants

RULES:
- NEVER generate 5 diverse families at once
- ALWAYS start with simple step variants (guaranteed to work)
- Use probes to filter before full evaluation
- Only expand complexity after finding a working baseline
- If iteration 10 with no improvement: try different mutations, not new families
