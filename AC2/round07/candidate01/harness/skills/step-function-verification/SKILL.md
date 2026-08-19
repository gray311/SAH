---
name: step-function-verification
description: Playbook for verifying TRUE step function creation. Use analyze_step_structure to confirm edits create piecewise-constant functions before expensive evaluation.
---

# Step Function Verification Playbook

## Critical: Detect Linear vs Step Functions

The seed program creates PIECEWISE-LINEAR functions. You need PIECEWISE-CONSTANT steps.

### Step 1: Initial Analysis
Call analyze_step_structure immediately after loading the seed:
- Should report function_type: "unknown" or "linear"
- is_piecewise_constant should be False or None
- This confirms the seed uses linear optimization

### Step 2: After Each Edit
After calling edit_solution, call analyze_step_structure:
- Look for function_type: "step" or is_piecewise_constant: True
- Check num_regions and estimated_num_steps (should match your intended steps)
- If is_piecewise_constant is False, EDIT AGAIN with jnp.piecewise

### Step 3: Pattern Recognition

Good step function indicators:
- 'jnp.piecewise(x, [cond1, cond2, ...], [h1, h2, ...])' where h1, h2 are constants
- Multiple 'jnp.where' chains with constant values
- No linear expressions like '+ x', '- x', '* x' in the function body

Bad indicators (linear ramps):
- 'jnp.linspace' or 'np.linspace'
- 'lambda x: x' or similar
- Linear expressions in where conditions

### Step 4: Before Evaluation
NEVER evaluate without first calling analyze_step_structure!
- If function_type is not "step", discard and re-edit
- Waste ~10s of analysis is better than wasting an eval on linear functions
- Only evaluate if is_piecewise_constant: True

### Step 5: Iterative Refinement
1. Generate config with step_config_generator
2. Edit to create step function
3. Verify with analyze_step_structure
4. If wrong, go back to step 2
5. Once verified as step function, probe and then evaluate

## Checklist

- [ ] Called analyze_step_structure after edit
- [ ] function_type shows "step"
- [ ] is_piecewise_constant: True
- [ ] num_regions matches intended step count
- [ ] Only then call probe/evaluate
