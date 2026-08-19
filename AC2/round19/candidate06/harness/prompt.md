You are optimizing C2 = ||f*f||2^2 / ((int f)^2 ||f*f||_inf) for non-negative f: R->R.
Current best: 0.8962799441554086 (Google's AlphaEvolve step functions).

CRITICAL: The seed implements 12 diverse step-function patterns with high resolution (600 intervals).
Do NOT discard this. Instead, SYSTEMATICALLY MUTATE it:

STRATEGY (2 iterations per full cycle):
PHASE 1 (iterations 1-20): EXPLORE MUTATIONS
1. Call probe_solution on the seed first to establish baseline
2. Generate 3-5 MUTATIONS of seed patterns: change heights by +/-0.1-0.2, shift boundaries by +/-5%,
   combine adjacent levels, or try asymmetric patterns
3. Probe ALL mutations (aim for 15-20 probes total)
4. Evaluate TOP 2 by probe score (max 2 full evals per cycle)
5. If best beats seed: switch to Phase 2. If not: generate MORE mutations.

PHASE 2 (iterations 21-40): REFINEMENT
1. Take best mutation that beat seed
2. Generate 3 fine mutations (+/-2% parameters)
3. Probe all, evaluate top 1
4. If no improvement after 5 iterations: go back to Phase 1 with fresh mutations

RULES:
- ALWAYS ensure f >= 0 (use jax.nn.softplus or max(0,·))
- Use probes aggressively: aim for 20+ probes before any full eval
- Never waste evals on clearly suboptimal variants (probe score < seed)
- Try MUTUALLY EXCLUSIVE changes: if one mutation raised peak height, try another that lowers it
- Seed has 12 patterns: try variations of ALL of them
