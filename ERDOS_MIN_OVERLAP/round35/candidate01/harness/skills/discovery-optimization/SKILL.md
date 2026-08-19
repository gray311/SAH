---
name: discovery-optimization
description: "Construct simple step functions with plateau patterns. Test bipartite, tri-partite, and alternating patterns. Use probe_solution to quickly screen candidates. Focus on configurations where h=1 on intervals totaling length 1.0."
---

# Step Function Construction for Erdos C5
## Core Strategy: Build Simple Step Functions
The optimal h is likely a simple step function (plateaus of 0 and 1), not a complex sigmoid.
## Pattern Types to Try
### Pattern 1: Bipartite (Single Transition) - h = 1 on [0, 0.5], h = 0 on [0.5, 2] - This is the natural constraint-satisfying step function - Calculate overlap for k in [0, 2]
### Pattern 2: Tri-partite (Two Transitions) - h = 1 on [0, a], h = 0 on [a, b], h = 1 on [b, 2] - Constraint: a + (2-b) = 1 (total "on" time = 1) - Try various a, b values: (0.4, 0.6), (0.3, 1.0), (0.25, 0.75), etc.
### Pattern 3: Alternating (Multiple Short Plateaus) - h = 1 on multiple small intervals totaling length 1 - Example: h = 1 on [0, 0.2], [0.8, 1.0], [1.2, 1.4], [1.8, 2.0] - Test if spreading the "on" regions reduces peak overlap
### Pattern 4: Centered Pattern - h = 1 on [c-0.5, c+0.5] (centered plateau) - Try c = 0, 0.5, 1.0, 1.5, 2
## Workflow
1. Start with bipartite pattern a=0.5 2. Probe it quickly 3. If combined_score <= 1.0, try other patterns 4. Test tri-partite with various (a,b) pairs 5. Test alternating patterns 6. Evaluate the best probe candidates fully 7. Finish when combined_score > 1.0
## Key Constraint Always ensure: measure of {x: h(x)=1} = 1.0 exactly.
