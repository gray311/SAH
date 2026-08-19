You are optimizing the C2 constant: C2 = ||f*f||₂² / ((∫f)² ||f*f||_∞)
Current best: 0.8962799441554086 (combined_score=1.042)

PROBLEM: The seed is a gradient optimizer with 11 step-function patterns.
ALL 6 previous harnesses failed because they tried to generate COMPLETE programs
from code snippets, but the EVOLVE-BLOCK edits should MODIFY the existing optimizer,
not replace it. The optimizer already has 11 diverse patterns; the issue is the
SEARCH STRATEGY, not the function library.

SOLUTION: Systematically tune the optimizer's hyperparameters:
1. Try DIFFERENT learning rates (0.05, 0.1, 0.2, 0.3) - the seed uses 0.15
2. Try DIFFERENT num_intervals (400, 800, 1200) - the seed uses 600
3. Try DIFFERENT num_steps (15000, 30000, 50000) - the seed uses 25000
4. Try DIFFERENT reinit_fraction (0.05, 0.1, 0.2) - the seed uses 0.12
5. Try DIFFERENT stagnation_window (50, 200, 500) - the seed uses 100

STRATEGY:
PHASE 1 (iterations 1-12): HYPERPARAMETER GRID SEARCH
- Generate 3-5 hyperparameter variants with ONE changed parameter at a time
- Use probe_solution on ALL variants (up to 30 probes)
- Evaluate TOP 1-2 by probe score
- Track which parameter ranges give best probe scores

PHASE 2 (iterations 13-25): FOCUSED TUNING
- Take best hyperparameter region from Phase 1
- Generate fine-grained variants (+/- 20% on promising parameters)
- Probe all, evaluate top 1-2
- If no improvement after 5 iterations: go back to Phase 1 with NEW parameter

RULES:
- NEVER generate complete programs from scratch - edit the existing OptimizerHyperparameters class
- ALWAYS change at least one hyperparameter (learning_rate, num_intervals, num_steps, reinit_fraction, or stagnation_window)
- Use probes to quickly filter hyperparameter combinations before full eval
- If probe < 1.0, skip full eval and try different hyperparameters
