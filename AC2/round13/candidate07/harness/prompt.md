You are an expert in functional analysis for maximizing C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞).

Current best: 0.8962799441554086 (step function, combined_score 1.03841).

Strategy: The seed has 13 well-tuned step patterns. Beat the record by making **targeted refinements** to existing patterns, not inventing new function classes.

Method:
1. Pick a seed pattern (0-12) from the EVOLVE-BLOCK.
2. Generate 2-3 variants with small, mathematically-informed mutations:
   - Height perturbation: change peak heights by ±0.02-0.08
   - Width adjustment: expand/contract intervals by 3-8%
   - Asymmetry: make symmetric patterns asymmetric (e.g., 1.40 → 1.42, 1.40, 1.38)
3. Use probe_solution to rank variants (30 probe budget). Evaluate only top 1-2.
4. If no improvement after 3 iterations, try a different seed pattern.
5. Function constraints: f(x) ≥ 0, ∫f > 0, numerically stable.

Tools: edit_solution (implement one mutation variant), evaluate_solution (full score), probe_solution (approx score, FAST), generate_step_variants (get 3 related step function variants), finish (report best C₂).
