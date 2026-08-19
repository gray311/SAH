You are optimizing f for C2 = ||f★f||₂² / ((∫f)² ||f★f||_∞). Current best: 0.8962799441554086 (step functions).

KEY INSIGHT: The seed's 12 step-patterns are promising (seed score 1.042). Don't abandon them.

STRATEGY - Systematic Step-Function Tuning:

PHASE 1 (iterations 1-20): TUNING EXISTING PATTERNS
1. Study the seed's _create_step_initializer: 12 patterns with heights 0.6-2.8 at positions 0.06-0.90
2. For EACH pattern, try 3 targeted mutations:
   - Height boost: +0.1 to peak height (increases ||f★f||_∞ but may reduce L2)
   - Width expansion: ±0.02 to interval boundaries (widens support)
   - Asymmetry: Shift peak left/right by 0.03 (tests symmetry effects)
3. For each mutation: probe first, then eval only if probe > 1.0

PHASE 2 (iterations 21-30): TRY ONE NEW FAMILY (if no step pattern improved)
1. Only try Gaussian mixtures: f(x) = sum w_i * exp(-((x-μ_i)²)/(2σ_i²))
2. Use 3 Gaussians centered at -1, 0, 1 with σ=0.5-0.8, weights summing to 1
3. Probe all 3-5 variants, eval top 1

RULES:
- NEVER skip probing: always probe before full eval
- If probe < 1.0: skip eval, try next variant
- Try all 12 seed patterns first before any new family
- When editing step patterns: use f = f.at[start:end].set(new_value)
- After 3 failed mutation attempts on a pattern: switch to next pattern
- At iteration 20+: if best is still seed pattern, try Gaussian mixture
