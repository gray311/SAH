---
name: discovery-optimization
description: "Maximize C\u2082 by exploring COMBINATORIAL rearrangements. Use restructure_steps to merge/split steps, create new patterns, probe before evaluate."
---

# C₂ Combinatorial Step Function Search

## Key Insight
Current 12 patterns are local optima. Must REARRANGE combinatorial structure, not tweak parameters.

## Method
### Step 1: Restructure
Call restructure_steps for major edits: merge, split, reorder, reshape, retune, bimodal, plateau.

### Step 2: Probe Before Evaluate
After restructure, probe with probe_solution. Test 3-5 variants. Evaluate only best.

### Step 3: Iterate or Pivot
If probe improves, evaluate and continue. If stuck after 3 attempts, try COMPLETELY DIFFERENT pattern class.

## Common Patterns to Try
- Pyramid: low-high-low
- Bimodal: two peaks
- Plateau: multi-level alternating
- Skewed: asymmetric

## Tool Usage
- restructure_steps: AT LEAST ONCE at start, then when stuck
- probe_solution: After every restructure, before eval
- evaluate_solution: Only for best probe result

## Success: combined_score > 1.03492
