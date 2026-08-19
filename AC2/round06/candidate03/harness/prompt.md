You are optimizing C2 for the second autocorrelation inequality.

Current baseline: 1.02665 (seed program). Target: > 1.03.

KEY INSIGHT: The seed uses 9 step function initializations. Create BETTER step functions by editing _create_step_initializer.

DON'T try Gaussian/B-splines - step functions are the mathematical champions (0.8963 theoretical).

STRATEGY:
1. Edit _create_step_initializer with concrete step patterns:
   - Tall narrow peak: 0.25n to 0.5n, height 1.4
   - Bimodal: 0.1n to 0.2n and 0.5n to 0.6n, heights 1.2 and 1.3
   - Asymmetric: 0.1n to 0.4n, height 1.3
   - Three peaks: 0.15n to 0.25n, 0.35n to 0.45n, 0.6n to 0.7n
2. Create 3-5 variants, probe each, evaluate top 2
3. Max 4 evals total

TOOL USAGE:
- edit_solution: Edit _create_step_initializer with exact intervals like: f = f.at[int(0.15*n):int(0.2*n)].set(1.2)
- probe_solution: Test variants cheaply (~10 seconds)
- evaluate_solution: Only top 2-3 after probing
- finish: When done
