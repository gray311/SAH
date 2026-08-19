---
name: discovery-optimization
description: "Use generate_initial_step_function to create valid h with integral=1."
---

# Erdos C5 - Valid Initialization Strategy

## Step 1: Generate Valid Initial h
1. CALL generate_initial_step_function to get h with integral(h)=1
2. CALL probe_solution on candidate
3. CALL evaluate_solution if c5_bound < 0.375

## Critical Rules
- ALWAYS start with generate_initial_step_function
- Ensure integral(h)=1
- Probe before full evaluation
