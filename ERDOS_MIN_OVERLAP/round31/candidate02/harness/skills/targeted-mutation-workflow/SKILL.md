---
name: targeted-mutation-workflow
description: Use get_correlation_profile to find problematic k, then targeted_h_optimizer to reduce overlap at those k.
---

# Targeted Mutation Workflow for Erdos C5

## Step 1: Analyze Correlation
CALL get_correlation_profile
- This identifies top 3 k values with highest overlap
- Example output: {"problematic_k": [245, 490, 735], "max_overlap": 0.381}

## Step 2: Generate Targeted Mutation
CALL targeted_h_optimizer with:
  problematic_k: [k1, k2, k3]  # from step 1
  strategy: "spread_peaks"  # or "asymmetric", "bimodal"

This creates a new h array that:
- Reduces overlap at the specified k values
- Maintains integral(h) = 1
- Keeps h in [0,1]

## Step 3: Screen with Probe
CALL probe_solution on the new h
- Keep if c5_bound < 0.375

## Step 4: Evaluate and Iterate
CALL evaluate_solution on best candidates
- If combined_score > 1.0, finish
- Otherwise, repeat with different strategy

## Strategy Guidelines
- spread_peaks: Best for reducing overlap at multiple k values
- asymmetric: Good when one side dominates the overlap
- bimodal: Useful when current h is unimodal
