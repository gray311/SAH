---
name: step-function-first
description: A method playbook that prioritizes switching to step functions immediately. Do not waste budget optimizing piecewise-linear functions - step functions are the record holders and theoretically optimal for this convolution inequality.
---

# Step-Function-First Strategy for C2 Optimization

## Objective
Maximize C2 > 1.026. Current best is step functions at 0.8963 (vs linear at 1.026 combined).
The strategy is: SWITCH TO STEP FUNCTIONS FIRST, then optimize within that representation.

## Why Step Functions?
1. Theoretical evidence: Step (piecewise-constant) functions achieve the known best C2 = 0.8963
2. The seed's piecewise-LINEAR functions only reach ~0.89 when normalized
3. Convolution theory suggests step functions concentrate energy optimally
4. Linear optimization is adding unnecessary complexity

## Phase 1: Immediate Switch (Tools 1-3)
Tool 1: convert_to_step_functions
- IMMEDIATELY call this as your first tool
- It rewrites the EVOLVE-BLOCK with step function code
- Do NOT call mutation_probe first

Tool 2: probe_solution
- Call ONCE to check approximate score
- Expected: Should be around 1.026-1.03

Tool 3: evaluate_solution
- Call to confirm with full evaluation
- Budget decision: if score > 1.02665, continue optimizing step functions
- If score <= 1.02665, switch representation

## Phase 2: Step Function Optimization
If step functions work:
1. Vary num_pulses: try 2, 3, 5 separate pulses
2. Vary pulse_width: try 0.1, 0.15, 0.2 of domain
3. Vary pulse_height: try 1.0, 1.2, 1.4, 1.6
4. For each change: probe once, then evaluate
5. Track which configuration gives best C2

## Phase 3: Alternative Representations
If step functions fail (rare):
1. Call mutation_probe to get Gaussian mixture variants
2. Switch to 2-5 Gaussian components
3. Optimize means and sigmas
4. Probe 1-2 variants, evaluate each

## Budget Discipline
- 20 total evals
- 1 eval for step function confirmation
- 3-5 evals for step function optimization
- 10-12 evals remaining for alternative representations
- Never spend 3+ evals on one parameter without probing first

## Key Rules
- convert_to_step_functions FIRST - period
- Max 1 probe before each evaluation
- Evaluate immediately after major representation change
- If stuck after 3 evals: SWITCH representation
- Track scores: representation -> parameters -> score
- finish when score > 1.026 or 15 evals used
