You are optimizing a 29x29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

The seed program uses Paley construction with SA hill climbing. However, you've noticed the best score (0.561608) barely improved from the seed (0.545692), indicating the current approach is stuck in a local optimum.

KEY INSIGHT: Simply varying SA parameters on the SAME deterministic Paley construction won't help. You need to CHANGE the construction strategy itself.

Your goal: TRY DIFFERENT BASE CONSTRUCTIONS, not just tune SA parameters.

STRATEGIES TO EXPLORE (priority order):
1. PERTURB THE PALEY MATRIX: Start with Paley, then flip 5-10% of elements randomly to escape local optima
2. RANDOM INITIALIZATION: Instead of Paley, start with a random ±1 matrix
3. HYBRID APPROACH: Paley + targeted perturbations (flip elements in low-correlation regions)
4. DIFFERENT SEED RANGES: Try seeds 0-500, 1000-1500, etc. (the current 4000-4499 may have bad RNG patterns)

PER EVALUATION WORKFLOW:
- Run 3-5 DIFFERENT construction strategies in parallel (Paley-perturbed, random, etc.)
- Use PROBE with 200 iterations per strategy to quickly rank them
- Use the BEST strategy from probe for the FULL evaluation
- Vary the PERTURBATION SEED and PERTURBATION FRACTION between evaluations

CRITICAL: Do NOT keep Paley "EXACTLY as-is". The fact that parameter sweeps fail means you MUST change the base construction.

Remember: The Paley residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28} are just ONE possible start. Try perturbing this, or skip to random initialization entirely.

With 20 evaluations, you can afford to test 4 different strategies each (5 evals/strategy) to find which base construction works best.
