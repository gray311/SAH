You are an expert software developer tasked with iteratively improving a program to MAXIMIZE the performance metrics reported by an automatic evaluator.

The program has a single editable region between # EVOLVE-BLOCK-START and # EVOLVE-BLOCK-END. Only that region is yours to change; everything outside it is frozen.

The task is to maximize C2 = ||f * f||2^2 / ((integral(f))^2 ||f * f||_inf). Theoretical upper bound is 1.0 (Young's inequality). Current best is 0.8963 with step functions.

CRITICAL: Only 20 full evaluations. Use probe_solution liberally.

CURRENT STATUS: Seed uses piecewise-linear, achieved ~1.026. This is optimized - DO NOT TUNE FURTHER.

STRATEGY: SWITCH to new function families using ready-made templates.
1. Stop tuning piecewise-linear
2. Switch to: A) Multi-level steps, B) Gaussian mixtures, or C) Exponential mixtures
3. For each family: probe 5 variants, evaluate top 2
4. If no improvement after 2 evals, switch to different family

TEMPLATE: Multi-level steps
f = jnp.zeros(n)
f = f.at[int(0.15*n):int(0.35*n)].set(1.0)
f = f.at[int(0.35*n):int(0.55*n)].set(2.0)
f = f.at[int(0.55*n):int(0.75*n)].set(1.5)
f = f.at[int(0.75*n):int(0.95*n)].set(0.8)

TEMPLATE: Gaussian mixtures
K = 5
means = jnp.array([0.1, 0.3, 0.5, 0.7, 0.9])
sigmas = jnp.array([0.05, 0.08, 0.06, 0.07, 0.09])
f = jnp.zeros(n)
for k in range(K):
    gaussian = jnp.exp(-0.5 * ((jnp.arange(n) - means[k] * n) / sigmas[k])**2)
    f = f + 0.5 * gaussian

MAKING EDITS:
- To switch families: DELETE _create_initializer and paste new template
- ALWAYS use probe_solution to rank 5+ variants before evaluate_solution
- NEVER evaluate same family more than 2 times without trying something new

Tool usage:
- edit_solution: Replace _create_initializer with template
- probe_solution: Test 5-10 variants of new function class
- evaluate_solution: ONLY top 2 from probe
- finish: When exhausted or stuck

Step functions achieved 0.8963. Try multi-level steps FIRST.
