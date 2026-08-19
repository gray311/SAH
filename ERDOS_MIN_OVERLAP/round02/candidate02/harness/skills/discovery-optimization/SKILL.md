---
name: discovery-optimization
description: "Combinatorial search for step functions in Erdos minimum overlap problem. Avoids gradient descent,\ndirectly tests discrete step function configurations with integral=1 constraint."
---

# Erdos Minimum Overlap - Step Function Search


## Problem
Minimize max_k integral h(x)(1 - h(x+k)) dx for step function h: [0,2]->[0,1] with integral h = 1.
Current best: C5 <= 0.380923 (combined_score > 1.0 is success).


## Why Gradient Descent Fails
The seed program uses sigmoid+gradient descent on latent vectors. This produces smooth functions,
not true step functions. The optimal solution likely has sharp binary transitions.


## Solution: Direct Step Function Search


### Use design_step_configurations()
Call this tool FIRST to generate 10-20 step function candidates:
- Two-step patterns: h=1 on [0,a], h=0 on [a,2] where a=0.5 (integral=1)
- Three-step patterns: two transitions with appropriate heights
- Alternating patterns: high-low-high with integral normalized to 1
- For each, compute C5 bound via FFT


### Workflow
1. Call design_step_configurations() to get ranked candidates
2. For top 3-5 candidates, modify seed program to USE THOSE step patterns directly
3. Edit out the optimizer/Evolve-Block and replace with direct h values
4. Call evaluate_solution to get true score
5. If best score < 1.0, generate more diverse configurations


### Key Patterns to Try
- Two-step: h(x)=1 for x in [0, 0.5], h(x)=0 elsewhere
- Three-step: three regions with heights summing to integral 1
- Alternating: high-low-high patterns


### Implementation
When editing EVOLVE-BLOCK:
- Remove ErdosOptimizer class or disable it
- Hardcode h as a step pattern array
- Compute c5_bound directly via FFT
- Output combined_score


## Tool Guide
- design_step_configurations: Returns dict with keys like 'two_step_simple', 'three_step_balanced', etc.
- edit_solution: Replace optimizer with direct step function
- probe_solution: Quick ranking before final eval
- evaluate_solution: True score; MAXIMIZE combined_score
- finish: End session when best score cannot be improved


## Success Criteria
- combined_score > 1.0 (c5_bound < 0.38092303510845016)
- validity = 1.0 (integral exactly 1)
- Budget: 20 evaluations
