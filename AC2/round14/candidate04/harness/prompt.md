You are optimizing C2 = ||f★f||_2^2 / ((int f)^2 ||f★f||_inf) for a non-negative function f: R->R.

Current best: 0.8962799441554086 (step function).

Critical insight: Step functions are LOCAL optima. To beat them, explore STRUCTURED VARIATIONS of step patterns:
1. Vary heights asymmetrically (e.g., 1.40, 1.45, 1.38)
2. Perturb widths by 3-8% (not 10%+)
3. Shift centers by 1-2%
4. Add small bumps to existing steps
5. Mix levels differently

Strategy:
- Generate 2-3 diverse step-pattern mutations per iteration
- Use probe_solution to rank them FAST (30 probes = rank many variants)
- Evaluate only top 2-3 by probe
- If no improvement after 10 iterations, try a DIFFERENT mutation type
- Focus on SMALL perturbations (step functions are sensitive)

Constraints: f>=0, integral>0, numerically stable.

Tools: edit_solution (make small, precise changes), evaluate_solution (full score, budget 30), probe_solution (approx score, use to filter), finish.
