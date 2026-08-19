---
name: construct-step-functions
description: Build direct step functions with binary plateaus. Start with bipartite, try tri-partite, alternating patterns. Enforce integral(h)=1 exactly.
---

# Constructing Step Functions for Erdos C5
## Direct Step Function Approach
Forget the sigmoid latent space. Build h directly as a step function with binary values.
## Pattern Hierarchy
### Level 1: Bipartite (1 Transition) Try these first: - LEFT-BASED: h=1 on [0, 0.5], h=0 on [0.5, 2] - RIGHT-BASED: h=0 on [0, 0.5], h=1 on [0.5, 2]
These are the simplest integral=1 satisfying functions.
### Level 2: Tri-partite (2 Transitions) h=1 on [0,a], h=0 on [a,b], h=1 on [b,2] Constraint: a + (2-b) = 1
Try these (a, b) pairs: - (0.4, 0.6), (0.3, 1.0), (0.25, 0.75), (0.2, 0.8) - (0.45, 0.55), (0.35, 0.95)
### Level 3: Alternating (Multiple Plateaus) Spread the "on" regions: - Four plateaus: [0,0.2], [0.8,1.0], [1.2,1.4], [1.8,2.0] - Three plateaus: [0,0.33], [0.67,1.0], [1.33,2.0]
## Workflow
1. Generate bipartite patterns first (LEFT and RIGHT) 2. Use step_function_builder to get code for each 3. Probe each quickly with probe_solution 4. Evaluate the best probe candidates 5. If no improvement, try tri-partite patterns 6. Finally, try alternating patterns
## Remember - Integral must be EXACTLY 1.0 - h values must be EXACTLY 0 or 1 - Simpler = better for step functions
