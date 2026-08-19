You are optimizing C₂ = ||f * f||₂² / ((∫f)² ||f * f||_∞) for the second autocorrelation inequality.

Current best: 0.8963 (step functions). Target: surpass this.

KEY INSIGHT: The seed program already uses piecewise-constant step functions via jnp.piecewise.
Don't try to "fix" the function type - instead, SYSTEMATICALLY EXPLORE the multi-level step space.

STRATEGY:
1. Start with seed's pattern (400 intervals, multi-level steps around 1.0-2.0 heights)
2. Generate structured variations: change heights, widths, positions systematically
3. Use probe_solution heavily (cheap ranking) to guide search
4. Evaluate only top 1-2 candidates (save your 20 evals)
5. If no progress in 10 iterations, try a different initial height range or symmetry

WORKFLOW:
- Generate pattern variation
- Verify it's still a valid step function (check no linear patterns)
- Probe to rank (do this for 3-5 variants per iteration)
- Evaluate the best 1-2
- Iterate with new variations based on what worked

COMBINATORIAL SEARCH: Think of heights as variables (0.5-2.5 range). The best function
likely has multiple levels at different heights. Explore systematically, not randomly.

BUDGET: 20 full evaluations maximum. Use probes liberally (~15-20 probes per eval).
