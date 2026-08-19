You are optimizing the C2 constant: C2 = ||f*f||2^2 / ((∫f)^2 ||f*f||_∞).
Current best: 0.8962799441554086 (step functions). Target: >0.89628.

CRITICAL: The EVOLVE-BLOCK contains a C2Optimizer with editable hyperparameters.
Your task is to EDIT the optimizer's hyperparameters and initialization logic.

SEARCH STRATEGY:
1. Call analyze_optimizer_params ONCE to understand current hyperparameters
2. Generate CONCRETE code edits for hyperparameters:
   - Try different num_intervals (200-1000), learning_rate (0.01-0.3), num_steps (5000-50000)
   - Try different pattern initializations (9 step patterns available)
   - Try reinitialization strategies (reinit_fraction 0.05-0.2, reinit_std 0.01-0.05)
3. Call probe_solution on edited variants (cheap ranking)
4. Call evaluate_solution on top 1-2 variants

RULES:
- NEVER call tools that don't exist (no analyze_convolution_profile, no generate_candidates)
- ALWAYS ensure f >= 0 (use jax.nn.relu or jax.nn.softplus)
- Edit the OptimizerHyperparameters dataclass or C2Optimizer.__init__ directly
- Use JAX array mutation: f = f.at[start:end].set(value)
