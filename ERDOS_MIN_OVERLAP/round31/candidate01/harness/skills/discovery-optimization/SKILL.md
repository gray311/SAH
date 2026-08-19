---
name: discovery-optimization
description: "Use step_function_generator to create valid step functions with integral=1, then probe and evaluate."
---

# Step Function Generation for Erdos C5

## Core Principle
Create valid step functions directly with integral(h)=1, bypassing the flawed optimizer.

## Step 1: Generate Candidates
1. CALL step_function_generator to create 3-5 diverse step functions
   - Each will satisfy integral(h)=1 exactly
   - Values in [0,1] guaranteed
   - Different patterns: bipartite, multi-modal, sparse

2. EXAMINE the generated functions
   - Check the number of steps
   - Note the pattern type

## Step 2: Screen with Probe
1. CALL probe_solution on each candidate
2. Keep those with c5_bound < 0.381
3. Select best 1-2 for full evaluation

## Step 3: Evaluate
1. CALL evaluate_solution on selected candidates
2. If combined_score > 1.0, finish

## Step 4: Iterate
If no improvement:
- Call step_function_generator again with different parameters
- Try bipartite, then multi-modal, then sparse patterns
- Always probe before full eval

## Key Rules
- ALWAYS start with step_function_generator
- Use integral=1 constraint to guide generation
- NEVER trust the seed's optimizer - it has bugs
- Evaluate only candidates with c5_bound < 0.381
