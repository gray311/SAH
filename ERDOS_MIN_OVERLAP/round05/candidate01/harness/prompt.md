You are an expert in mathematical optimization and algorithm design. Your task is to optimize
the seed program to find a better upper bound for the Erdős minimum overlap constant C₅.

**THE OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound
where c5_bound is the maximum overlap integral found. You must find c5_bound < 0.38092303510845016.

**CONSTRAINTS**: The step function h must have values in [0,1] and integrate to exactly 1 over [0,2].

**SEARCH STRATEGY**: The seed program uses a multi-restart Adam optimizer but is stuck at 0.999641.
Don't try to "fix" it with small edits. Instead, explore fundamentally different approaches:

1. **Coarse-to-fine**: Start with num_intervals=100-200, find good patterns, then refine to 800-1000
2. **Different initializations**: Try step functions, waveforms, concentrated mass patterns
3. **Simpler strategies**: Direct construction of candidate solutions, less reliance on gradient descent

**BUDGET**: ~30 evaluations. Spend wisely.

**AGENCY**: Complete rewrites of the EVOLVE-BLOCK are encouraged for strategic changes.
