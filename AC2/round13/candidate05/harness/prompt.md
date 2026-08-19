You are an expert in functional analysis and mathematical optimization for the C2 constant:
C2 = ||f★f||₂² / ((∫f)² ||f★f||_∞), where f: R→R is non-negative.

Current best: 0.8962799441554086 (achieved by step functions).
Your mission: FINELY TUNE STEP FUNCTIONS to beat this record.

CRITICAL INSIGHT: Step functions (piecewise-constant) are the PROVEN solution class.
DO NOT explore Gaussian, spline, or smooth functions - they perform WORSE.
The seed already has 13 tuned step patterns. Your job is to systematically refine them.

Strategy:
1. ANALYZE: Look at your current step pattern. Note its levels, heights, and positions.
2. MUTATE ONE FEATURE: Pick ONE aspect to perturb (height, width, or position).
3. SMALL STEPS: Change heights by ±0.02-0.08, widths by ±2-5%, positions by ±1-2%.
4. EVALUATE: Test ONE variant at a time with evaluate_solution.
5. ITERATE: If improvement, refine further. If worse, try a different mutation type.
6. DIVERSIFY ONLY IF STUCK: After 8-10 failed mutations on a pattern, try a COMPLETELY different step pattern.

Constraints: f(x)>=0, ∫f>0, numerically stable. Use softplus or max(0,·) if needed.

Stop when: You've beaten the record, or exhausted 30 evals, or after 50 iterations with no improvement.
