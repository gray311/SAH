You are optimizing functions to maximize C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞), where the current best is 0.8962799441554086 (step functions).

CRITICAL INSIGHT: Step functions are trapped in a local optimum. To escape, you must:
1. First, probe 3-5 DIFFERENT mutation directions from current best (width changes, height changes, symmetry breaking)
2. Only call evaluate_solution if probe_score > current_best_score
3. If all 5 probes fail to beat seed, HARD RESTART with a completely different initial pattern

SEARCH STRATEGY:
PHASE 1 (iterations 1-20): MUTATION EXPLORATION
- Analyze current best's structure: where is L2 concentrated? where is sup?
- Generate 5 mutations targeting specific weaknesses:
  * Mutation A: Widen support by +/- 10% (reduce peak height proportionally)
  * Mutation B: Narrow support by +/- 10% (increase peak height)
  * Mutation C: Break symmetry - shift peak left/right by 5%
  * Mutation D: Change peak height by +/- 0.15 (not 0.05 - need larger changes)
  * Mutation E: Add a small side lobe (10% height, 15% width) on one side

PHASE 2 (iterations 21-30): DIVERSIFIED RESTART
If no improvement after iteration 20:
- Switch to completely different initial patterns:
  * Gaussian bimodal: two Gaussians separated by 1.0, each sigma=0.6, weights 0.5 each
  * Bimodal step: flat 1.0 from -2 to -0.5, flat 2.0 from -0.5 to 0.5, flat 1.0 from 0.5 to 2.0
  * Truncated exponential: exp(-alpha*|x|) for |x|<T, 0 otherwise, optimized for sharp cutoff
- Probe 3 variants from new class, evaluate best

RULES:
- Probe FIRST, evaluate SECOND. Never evaluate without probing.
- Each probe should test a DIFFERENT direction. Avoid similar mutations.
- If stuck (same probe pattern for 2 iterations): HARD RESTART with new architecture
