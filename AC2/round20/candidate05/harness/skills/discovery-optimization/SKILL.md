---
name: discovery-optimization
description: "Escape step-function local optimum by systematic mutation exploration. Target specific mathematical weaknesses (support width, peak height, symmetry) with focused probes. Hard restart when all directions exhausted."
---

# C2 Optimizer: Targeted Mutation Search

## Phase 1: Systematic Mutation Exploration

Step 1: Diagnose Current Best
- Call probe_solution on current best to confirm score
- Note: What is the support width? What is peak height? Is it symmetric?

Step 2: Generate 5 Targeted Mutations
Apply these SPECIFIC mutations to current best:

Mutation A (Widen): Reduce peak height by 10%, extend support by 10% on each side
Mutation B (Narrow): Increase peak height by 10%, reduce support by 10%
Mutation C (Asymmetry): Shift right side 5% higher, left side unchanged
Mutation D (Height Spike): Increase central peak by 0.15, keep others same
Mutation E (Side Lobe): Add small bump (height=0.15, width=0.15*support) on one side

For each mutation:
- Call probe_solution immediately
- Track which mutations improved probe score

Step 3: Evaluate Promising Mutations
- If 2+ mutations have probe_score > seed, evaluate them
- If only 1 mutation improves, evaluate just that one
- If 0 improvements: Proceed to Phase 2

## Phase 2: Hard Restart (iteration 21+)

When all mutation directions fail:

Restart Pattern 1: Gaussian Bimodal
f(x) = 0.5*exp(-((x+1.0)^2)/(2*0.6^2)) + 0.5*exp(-((x-1.0)^2)/(2*0.6^2))

Restart Pattern 2: Bimodal Step
f(x) = 1.0 for x in [-2,-0.5] U [0.5,2], f(x) = 2.0 for x in [-0.5,0.5]

Restart Pattern 3: Truncated Exponential
f(x) = exp(-0.5*|x|) for |x| < 2.5, f(x) = 0 otherwise

For each restart:
- Probe 3 variants (vary parameters slightly)
- Evaluate the best probe if score > seed

## Key Rules
- NEVER evaluate without probing first
- Each probe must test a DIFFERENT mutation direction
- Hard restart at iteration 20 if no improvement
- Target LARGE changes (0.15 height, 10% width) - small changes won't escape
