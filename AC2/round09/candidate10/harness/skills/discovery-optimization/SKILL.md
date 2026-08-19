---
name: discovery-optimization
description: "Step-function optimization for C\u2082 constant maximization. Use probes to test height/width/position variations, then evaluate the best variant. Build on the seed's 1.03431 baseline."
---

# Step-function C₂ optimizer playbook

## Core Strategy
The seed achieves 1.03431 using multi-level step functions. You must IMPROVE this, not explore random constructions.

## Probe-First Workflow (MANDATORY)
1. Edit the EVOLVE-BLOCK to change ONE parameter (height, width, or position of a step)
2. Call probe_solution immediately — this costs nothing and tells you if your edit helps
3. If probe < 1.03431, your edit is bad. Revert to baseline and try a DIFFERENT parameter change
4. If probe > 1.03431, call evaluate_solution to confirm, then continue building on this improved version

## Parameter Spaces to Explore
- **Peak heights**: Test heights from 1.6 to 2.0 in the central region
- **Peak widths**: Widen/narrow the central interval (try 0.2-0.8 fractions)
- **Multi-level patterns**: Add 2-3 intermediate levels (0.7-1.5) around the peak
- **Asymmetric variants**: Make left/right tails unequal
- **Step transitions**: Add extra steps at boundaries

## Edit Templates (SEARCH/REPLACE)
```
# Example 1: Increase central peak height
old: f = f.at[int(0.30*n):int(0.70*n)].set(1.62)
new: f = f.at[int(0.30*n):int(0.70*n)].set(1.70)

# Example 2: Widen central peak
old: start = int(0.25 * n)
     end = int(0.75 * n)
new: start = int(0.20 * n)
     end = int(0.80 * n)

# Example 3: Add decay wings
old: f = f.at[int(0.05*n):int(0.2*n)].set(0.62)
new: f = f.at[int(0.02*n):int(0.15*n)].set(0.62)
```

## Safety Rules
- NEVER remove the `jnp.relu` constraint
- NEVER change num_intervals < 400 (numerical stability)
- NEVER reduce num_steps < 30000 (needs optimization)
- ALWAYS preserve dataclass and class structure
- ONLY edit the _create_step_initializer method

## Evaluation Budget
- 30 full evaluations — use probe_solution to test 25+ variants
- Call evaluate_solution ≤ 5 times total
- Always pick the highest-probe variant for final evaluation

## When Stuck
- If all probes < 1.03431, try radically different: (a) two-peak vs single-peak, (b) triangular pyramid, (c) shifted central peak
- If no probes improve, REVERT to seed and call finish with score 1.03431
