---
name: constraint-first-strategy
description: Always check constraints before evaluation using structural_analyzer.
---

# Constraint-First Strategy for Erdos C5
## Core Principle The constraint integral(h) = 1 is CRITICAL. Violating it causes the optimizer to fail.
## Step-by-Step Workflow
1. CALL structural_analyzer on current best - Verify integral(h) = 1 - Verify h in [0,1] - Get step boundaries and heights
2. CALL targeted_mutations to generate alternatives - Choose mutation type: "bipartite" for simple, "tri-modal" for complex - Use step_width and peak_height to control mutation scale
3. CALL structural_analyzer on EACH candidate - If constraint_violated = true, DISCARD immediately - If constraints satisfied, proceed to probe
4. CALL probe_solution on constraint-satisfied candidates - Screen for c5_bound < 0.375
5. CALL evaluate_solution only on promising candidates
## Key Rules - ALWAYS check constraints before evaluation - DISCARD candidates that fail structural analysis - Use targeted mutations, not random search - Evaluate only when c5_bound < 0.375
