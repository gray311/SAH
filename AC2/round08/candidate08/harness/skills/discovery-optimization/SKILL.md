---
name: discovery-optimization
description: "C2 maximization via TRUE step functions. Must use jnp.piecewise with CONSTANT heights, NOT linear ramps. Generate random step specs, convert to code, verify, probe, evaluate top."
---

# C2 Maximization: TRUE Step Functions

## Critical Distinction

- Seed uses PIECEWISE-LINEAR optimization (fails)
- You need PIECEWISE-CONSTANT step functions (succeeds)
- Step functions are FLAT over intervals, not sloped

## Workflow

### Step 1: Analyze Current Structure
CALL analyze_step_structure to detect if current code creates:
- Linear ramps (bad)
- Piecewise-constant steps (good)

Typical analysis output:
- function_type: "linear" or "step"
- num_regions: number of distinct regions
- is_piecewise_constant: true/false

### Step 2: Generate Step Configuration
CALL step_config_generator with appropriate parameters:
- num_steps: 2-6 steps (more complex = better?)
- symmetric: true/false (try both)
- base_height: 1.0-2.0

### Step 3: Edit to TRUE Step Function
Use edit_solution to create piecewise-CONSTANT function:
- Use jnp.piecewise: f = jnp.piecewise(x, [cond1, cond2, ...], [h1, h2, ...])
- Use jnp.where chains: f = jnp.where(cond1, h1, jnp.where(cond2, h2, 0))
- Key: VALUES are CONSTANTS, not linear functions of x

### Step 4: Verify with analyze_step_structure
Call analyze_step_structure again. If is_piecewise_constant is false, EDIT AGAIN.

### Step 5: Probe & Evaluate
- Probe 3-5 variants to rank them
- Evaluate only TOP 2 (max ~4 evals)
- If no improvement, try different num_steps or symmetric settings

## Common Mistakes

- Creating linear ramps instead of flat regions
- Not verifying with analyze_step_structure before eval
- Creating too many evals (use probes for ranking)
- Using seed's initialization patterns (they're linear!)
