You are an expert in functional analysis and mathematical optimization. Your task: maximize
C2 = ||f * f||_2^2 / ((int_f)^2 ||f * f||_inf) for the second autocorrelation inequality.

- Theoretical upper bound: 1.0 (Young's inequality)
- Current best in literature: 0.8963 (achieved by step functions)
- Target: surpass 0.8963

CRITICAL: The seed program uses PIECEWISE-LINEAR optimization with _create_step_initializer that creates LINEAR ramps. This fails!

You must create TRUE PIECEWISE-CONSTANT step functions (flat over intervals, not sloped).

STRATEGY:
1. Generate random step function SPECIFICATIONS (num_steps=3-8, heights 0.5-2.5, interval boundaries at fixed fractions of domain)
2. Convert SPEC to CODE using jnp.piecewise: f = jnp.piecewise(x, [cond1, cond2, ...], [h1, h2, ...])
3. Use jnp.linspace to create domain points, then assign constant values via piecewise

WORKFLOW:
1. Generate step config: random num_steps (3-8), random symmetric/asymmetric, random heights (0.5-2.5)
2. Edit to create TRUE step function using jnp.piecewise with CONSTANT heights
3. Verify structure matches your config
4. Probe 3-5 variants to rank
5. Evaluate TOP 1-2 only (max ~5 evals total)

The seed's _create_step_initializer creates LINEAR ramps (e.g., jnp.linspace). YOU MUST USE jnp.piecewise with CONSTANT values.
