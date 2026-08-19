---
name: step-function-search
description: Generate concrete step function templates, probe, edit code, evaluate.
---

# Step Function Search for Erdos C5

## Strategy

1. CALL generate_step_function_template with template_type="three_peak"
   - Three peaks at 1/6, 1/2, 5/6 minimize max overlap

2. CALL generate_step_function_template with template_type="bipartite"
   - Single threshold at x=1

3. CALL generate_step_function_template with template_type="golomb"
   - 4 peaks at 0, 2/3, 4/3, 2

4. CALL generate_step_function_template with template_type="broad_plateau"
   - Wide plateau

5. For EACH template:
   - CALL probe_solution
   - Keep candidates with c5_bound < 0.382

6. EDIT EVOLVE-BLOCK to use best h template:
   - Replace _get_best_initialization with fixed h array
   - Use h directly (no gradient optimization needed)

7. CALL evaluate_solution on candidates with c5_bound < 0.375

## Key Points

- Start with CONCRETE step functions BEFORE gradient optimization
- Step functions satisfy integral=1, h in [0,1] exactly
- Try 3-4 DIFFERENT templates
- Gradient optimization is AUXILIARY - templates are primary
