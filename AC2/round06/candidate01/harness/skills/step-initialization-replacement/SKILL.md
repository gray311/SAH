---
name: step-initialization-replacement
description: Method for replacing _create_step_initializer with better step function code. Generate code, replace method, probe, evaluate top 2-3.
---

# Step Function Initialization Replacement Protocol

## Objective
Replace seed's _create_step_initializer with better step function code.

## Phase 1: Generate Code
Call step_function_code_generator with:
- {"num_steps": 2, "symmetric": true} for boxcar
- {"num_steps": 4, "symmetric": true, "heights": [0.5, 1.5, 1.5, 0.5]} for bimodal

## Phase 2: Replace Method
Use edit_solution to:
1. Find lines containing "def _create_step_initializer"
2. Delete all lines from that def through the end of the method
3. Insert the new code at that location

## Phase 3: Probe and Evaluate
1. Call probe_solution to test the new initialization
2. Generate 2-3 variations (different heights, num_steps)
3. Probe each variant
4. Evaluate the TOP 2-3 with evaluate_solution

## Critical Rules
- MAX 4 full evaluations
- Always probe 3-5 variants before eval
- Replace ENTIRE method, not just parts
