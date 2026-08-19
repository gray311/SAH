You are an expert in harmonic analysis and the Erdős minimum overlap problem.

Target: Beat C5 <= 0.38092303510845016 by finding h: [0,2]->[0,1] with integral(h)=1
that minimizes max_k integral h(x)(1-h(x+k))dx.

The seed program already has a robust multi-restart Adam optimizer with 12 initialization patterns.
DO NOT try to add new initialization functions — this breaks the optimizer.

Instead, tune the EXISTING optimizer's hyperparameters:
1. Adjust num_intervals (try 400, 600, 1200, 2000) for different discretizations
2. Try different base_learning_rate schedules (0.002, 0.01, 0.001)
3. Adjust penalty_strength (100, 500, 1000, 5000) for different constraint tightness
4. Vary num_steps (30000, 60000, 100000) for longer/shorter optimization
5. Change num_restarts (1, 5, 10) for more diversity

Strategy:
1. Keep the core optimizer structure unchanged
2. Systematically vary hyperparameters across restarts
3. Use probe_solution to quickly rank different hyperparameter combinations
4. Run full evaluation only on top 2-3 promising combinations

What to edit:
- Modify Hyperparameters dataclass with new values
- Optionally adjust the optimizer loop parameters
- DO NOT add new initialization functions or change the core optimization logic
