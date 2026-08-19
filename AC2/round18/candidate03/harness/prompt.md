You are optimizing C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞) for f≥0.

Current best: 0.8962799441554086.

YOUR METHOD: Mutate the 12 step patterns in the seed's _create_step_initializer method.

STRATEGY - SYSTEMATIC PERTURBATION:

STEP 1: Read the current best step pattern (which of the 12 patterns is being used).
STEP 2: Choose ONE perturbation from this menu:
  - Height: ±0.10 to ±0.25 (adjust peak heights)
  - Width: ±5% to ±15% of current interval (shift start/end boundaries)
  - Asymmetry: Swap left/right bounds by ±10%
  - Split: Divide one level into two with new intermediate height
  - Merge: Combine adjacent levels into one
  - Shift: Move all levels left/right by ±10% of domain
STEP 3: Generate 3-5 variants with DIFFERENT perturbations.
STEP 4: Call probe_solution on ALL variants (cost: 1 probe per variant).
STEP 5: Call evaluate_solution on TOP 2 by probe score.
STEP 6: If no improvement after 3 iterations: try perturbation type from a different menu item.

RULES:
- Edit the EVOLVE-BLOCK: modify NUM_INTERVALS, LEARNING_RATE, NUM_STEPS, or REINIT_* params
- Or edit the _create_step_initializer method: change pattern heights, start/end positions
- Always ensure f≥0 (seed already does this with jnp.maximum)
- Use 30 probes to explore 8-15 variants before spending full evaluations
- Call evaluate_solution only on top 1-2 variants per iteration
- If probe score ≈1.0: your perturbation is ineffective; try different type
- Don't change 3+ parameters at once; one change per variant

WHY THIS WORKS: Small, targeted perturbations have explored the step-function landscape more thoroughly than random architectures.
