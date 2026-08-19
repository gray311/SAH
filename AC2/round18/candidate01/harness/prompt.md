You are optimizing C2 = ||f*f||₂² / ((∫f)² ||f*f||_∞) where f is non-negative.
Current best: 0.8962799441554086 (step functions).

CRITICAL STRATEGY: The seed has 12 EVOLVE-BLOCK step function patterns.
YOUR JOB: Mutate these patterns to create new variants, then USE COARSE PROBES to rank them.

SEARCH METHODOLOGY:
1. IDENTIFY PATTERN: Look at the current best solution - which pattern (0-11) is it based on?
   Pattern signatures: single step (0-2), multi-level (3-11), asymmetric (8-11)

2. MUTATE SMART (not random!):
   - Change heights: +/- 0.05 to 0.20
   - Change positions: shift start/end by +/- 5%
   - Add/remove levels: split a level into two, merge adjacent levels
   - Asymmetric variants: make left/right sides different heights
   - Novel structures: try patterns the seed hasn't explored (e.g., double peaks, plateau with spikes)

3. COARSE PROBING (MUST DO):
   - Call probe_solution on ALL 3-5 variants BEFORE any full eval
   - Probe uses ~10% subsample - FAST (~10s vs minutes)
   - ONLY call evaluate_solution on TOP 1-2 by probe score
   - With 30 evals budget, you need ~6-10 probes + 3-5 full evals

4. ITERATION PATTERN:
   - Iterations 1-15: Generate 3-5 mutations, probe all, eval top 2
   - If neither beats record: Generate NEW pattern class (e.g., if all single-level, try multi-level)
   - Iterations 16-30: Focus on the best architecture with finer mutations

RULES:
- NEVER call evaluate_solution without prior probing (wastes budget)
- If iteration 10+ with no improvement: try ENTIRELY NEW pattern class
- Mutation types: height tweaks, position shifts, level splits/merges, asymmetric designs
