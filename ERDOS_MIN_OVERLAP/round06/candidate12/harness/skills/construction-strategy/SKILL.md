---
name: construction-strategy
description: Use explicit mathematical construction to create step function candidates. Focus on structural patterns, not gradient optimization.
---

# Construction-Based C₅ Optimization

## Why Construction Over Optimization?

The Erdős minimum overlap problem has a combinatorial structure that gradient methods miss.
The optimal step function likely has specific properties:
- Symmetric breakpoints
- Binary or near-binary values
- Specific ratios between step heights

## Construction Blueprint

### Step 1: Choose a Structural Pattern
Select from these proven patterns:
- Symmetric two/multi-step functions
- Concentrated mass with specific width
- Binary functions (0/1 only)
- Rational breakpoint constructions

### Step 2: Parameterize Within Constraints
For each pattern, parameterize the degrees of freedom:
- Breakpoint positions (must satisfy ∫h=1)
- Step heights (bounded in [0,1])
- Number of steps (2 to 10+)

### Step 3: Generate Candidate Set
Create 5-20 diverse candidates:
- Vary the number of steps
- Vary breakpoint rational positions
- Vary height distributions
- Mix symmetric and asymmetric designs

### Step 4: Evaluate and Iterate
- Test all candidates
- Keep the best c5_bound
- If best is good, do focused refinement
- If best is poor, try completely different pattern

## Key Constraints to Maintain

- h(x) ∈ [0,1] for all x
- ∫₀² h(x) dx = 1 (exactly, or close enough)
- Minimize max_k ∫₀² h(x)(1-h(x+k)) dx

## Common Pitfalls

- Forgetting the integral constraint
- Creating values outside [0,1]
- Using too many steps (overfitting to discretization)
- Not trying diverse structural patterns
