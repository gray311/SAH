---
name: explicit-construction
description: Method playbook for constructing step functions with explicit breakpoints. Use when gradient methods fail or when testing specific structural hypotheses.
---

# Explicit Step Function Construction for Erdős C₅

## Core Idea
Instead of optimizing a smooth latent, CONSTRUCT h as a piecewise constant function
with explicit breakpoints. This lets you explore discrete structures that gradient
methods miss.

## Step 1: Choose Breakpoint Structure

### Single Block
- Breakpoints: none (or [1.0])
- h = 1 on [0,1], 0 on [1,2]
- Integral = 1 ✓

### Double Block (Symmetric)
- Breakpoints: [0.5, 1.0, 1.5]
- h = 1 on [0,0.5], 0 on [0.5,1.5], 1 on [1.5,2]
- Integral = 1 ✓

### Double Block (Asymmetric)
- Breakpoints: [a, 2-a] for some a∈(0,1)
- h = 1 on [0,a] and [2-a,2], 0 in between
- Integral = 2a = 1 ⇒ a = 0.5

### Triple Block
- Breakpoints: [a, b, 2-a] with a < b < 2-a
- Adjust heights and positions to get ∫h = 1

## Step 2: Construct with the Tool

Call `construct_step_function` with:
- breakpoints: list of positions where h changes
- heights: value of h on each interval

Example:
```python
args = {
    "breakpoints": [0.5, 1.5],
    "heights": [1.0, 0.0, 1.0]
}
result = construct_step_function(args)
if "error" in result:
    # Fix constraint violation
    pass
else:
    # Use result["h"] for evaluation
    pass

## Step 3: Probe Before Evaluating

Once you construct a candidate:
1. Call `probe_solution` with the code containing your construction
2. Compare c5_bound values across ~5-10 candidates
3. Pick top 1-2 for full `evaluate_solution`

## Step 4: Refine

If c5_bound < 0.3809 but not great:
- Add more breakpoints (3→4→5)
- Adjust existing breakpoint positions
- Try asymmetric patterns
- Probe each variant

## Common Pitfalls

- **Integral ≠ 1**: Normalize h after construction
- **Out of bounds**: Clip h to [0,1]
- **Too many intervals**: Start with 2-5 breakpoints, refine later
- **Not probing**: Use probe_solution to avoid wasting evals!
