You are an expert in functional analysis. Your task: maximize C2 = ||f * f||₂² / ((∫f)² ||f * f||_∞).

Current baseline: 1.02872 (seed). Target: > 1.02872.

CRITICAL INSIGHT: The seed uses 9 step-function initializations that are already optimized. The current harness FAILED because it mutated optimizer hyperparameters (learning_rate, num_intervals) instead of CREATING NEW STEP FUNCTION CONFIGURATIONS.

YOUR STRATEGY - Step Function Diversification:

1. DIRECT STEP CONSTRUCTION: Don't edit optimizer params. Edit the _create_step_initializer to create truly diverse step patterns:
   - 2-step: single rectangular peak
   - 3-step: left-middle-right with different heights
   - 4-step: bimodal with valley
   - Asymmetric: shifted peaks
   - Multi-cluster: 3+ separated peaks

2. VARY THESE PARAMETERS EXPLICITLY:
   - Step count: 2, 3, 4, 5, 7
   - Support width: 0.2n to 0.8n (as fraction of num_intervals)
   - Heights: 0.8 to 2.0 (relative)
   - Symmetry: centered vs left/right biased
   - Multi-peak: 2, 3, 5 separated clusters

3. PROBE-THEN-EVAL DISCIPLINE:
   - Create 5-7 step function variants
   - Probe each (cheap, ranks them)
   - Evaluate ONLY top 2

4. IF STILL STUCK: Try polynomial decay f(x) = exp(-alpha*|x|^beta), then Gaussian mixtures.

TOOL USAGE:
- edit_solution: Create NEW step functions with explicit intervals (use jnp.where, jnp.piecewise)
- probe_solution: Rank variants (call 5-7 times before any eval)
- evaluate_solution: Only for top 2 candidates
- finish: When done
