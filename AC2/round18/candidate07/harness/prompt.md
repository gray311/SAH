You are optimizing C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞) for non-negative f:ℝ→ℝ.
Current best: 0.8962799441554086 (step functions). Target: beat this record.

CRITICAL UNDERSTANDING: The seed program contains 10+ HIGH-QUALITY step patterns in _create_step_initializer.
These are NOT in a single local optimum—they are diverse, well-designed constructions.
The mistake was trying to GENERATE entirely new function families (Gaussian, B-spline, etc.).

CORRECT STRATEGY: You can only EDIT the existing EVOLVE-BLOCK. To improve:
1. Call analyze_patterns ONCE to see which pattern has best c2
2. Generate TARGETED VARIANTS by editing the winning pattern(s):
   - Shift interval boundaries by ±2-5%
   - Adjust heights by ±0.05-0.15
   - Add/remove small plateaus
   - Create asymmetric variants of symmetric patterns
   - Combine two patterns (e.g., take pattern 0's left, pattern 3's middle)
3. Use probe_solution on 5-8 variants (it's ~10x faster than full eval)
4. Evaluate TOP 1-2 variants that beat the current best by probe score
5. If no improvement after 3 iterations: pick a DIFFERENT seed pattern and repeat

RULES:
- NEVER try to replace step functions with Gaussian/B-spline/etc. (edit_solution can't do that)
- ALWAYS edit EXISTING patterns with small, targeted changes
- Use probes to filter 5-8 variants before any full evaluation
- After 5 iterations with no improvement: completely rewrite _create_step_initializer with NEW diverse patterns
- Remember: f(x)≥0 everywhere (use jax.nn.softplus or max(f, 0))

TOOL USAGE:
- analyze_patterns: Call at iteration 0 and whenever switching strategies
- generate_variants: Call to get 5-8 pattern edits of the best current pattern
- probe_solution: Call on ALL generated variants (max 30 total probes)
- evaluate_solution: Call ONLY on variants with probe score > current best
