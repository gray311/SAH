---
name: discovery-optimization
description: "Algorithm optimization for MoE load balancing. Use probe_solution to iteratively rank variants, then invest evals only on probe-winners."
---

# MoE EPLB Heuristics Playbook

## Phase 1: Baseline Probe
Call probe_solution on starting code to establish baseline score (fast, no eval budget).

## Phase 2: Single-Edit Probe Loop
For each iteration:
- Make ONE targeted SEARCH/REPLACE edit
- Call probe_solution
- If probe score > baseline: call evaluate_solution, update baseline
- If probe score <= baseline: try DIFFERENT edit (not refine)

## Phase 3: Full Redesign (after 2-3 failures)
If probe loop fails, rewrite balanced_packing entirely:
- First-Fit Decreasing: Sort experts by weight descending, pack using first-fit
- Best-Fit Decreasing: Sort by weight, pack to bin with least remaining capacity
- Weight-aware variance: Minimize variance in pack weights after each assignment
- Round-robin load: Alternate assignments while tracking load balance

## Key Rules
- Probe first, evaluate second (probe is ~10s cheap, evaluate is ~1-2 min expensive)
- Never evaluate without prior probing
- Each probe tells you if an edit direction is promising
- Entry function must remain: rebalance_experts_hierarchical(weight, num_physical_experts, num_groups, num_nodes, num_gpus)
