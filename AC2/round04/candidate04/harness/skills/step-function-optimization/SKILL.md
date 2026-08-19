---
name: step-function-optimization
description: Playbook for optimizing C2 using step functions (the current record-holders at 0.8963). Focus on diverse step configurations, multi-level steps, and asymmetric patterns.
---

# Step Function Optimization Playbook for C2

## Core Principle
Step functions (piecewise-constant) are the CURRENT RECORD-HOLDERS at 0.8963. The piecewise-linear seed may not beat them. You MUST create and explore step functions aggressively.

## Step 1: Generate Step Variants
Use create_step_function_variant to generate 5-10 concrete step function code snippets with different parameters:
- Single wide steps
- Multi-level steps (2-4 height levels)
- Asymmetric steps
- Narrow multiple steps
- Steps with gaps

## Step 2: Probe Before Evaluate
For each generated variant:
1. Call edit_solution to replace the EVOLVE-BLOCK with the variant
2. Call probe_solution to get a cheap score (~10s, doesn't use eval budget)
3. Track the probe scores
4. Probe 5-10 variants BEFORE spending any full evaluations

## Step 3: Full Evaluation on Top Candidates
Select top 3 variants from probe scores:
1. Each: run with MULTIPLE random seeds (2-3 per candidate)
2. Use evaluate_solution for these only
3. Total: 3-5 evaluations maximum
4. Track: which step configuration achieved the best C2

## Step 4: Iterate on Successful Patterns
If a step configuration works:
- Vary its parameters (width, height, number of levels)
- Generate new variants with successful patterns
- Continue probing before evaluating

## Critical Rules
1. STEP FUNCTIONS FIRST: Create step variants before refining piecewise-linear
2. PROBE LIBERALLY: Use 8-10 probes per step configuration family
3. LIMITED EVALS: Max 3-5 full evaluations, pick the best probed candidates
4. DIVERSIFY: Try wide steps, narrow steps, multi-level, asymmetric
5. RESET: If stuck at same score for 3 evals, generate completely new step variants

## Expected Results
- Should find step function variant > 0.8963
- Probe scores should correlate reasonably well with full evals
- Success requires exploring the step function space, not just piecewise-linear
## Tool Usage Priority
1. create_step_function_variant — generate step function code (PRIMARY)
2. probe_solution — rank step variants cheaply (USE LIBERALLY!)
3. edit_solution — implement step variants from tool output
4. evaluate_solution — confirm top candidates only (LIMITED BUDGET!)
5. finish — when evals exhausted or beat 0.8963
