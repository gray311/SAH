---
name: compact-search-strategy
description: Use compact analysis, generate 3 diverse mutations, probe all, evaluate best. Keep it simple.
---

# Compact Search for Erdos C5

## Step 1: Initial Analysis (ONCE ONLY)
Call compact_analysis to get top 3 problematic k values.
Do NOT call again - save tokens.

## Step 2: Generate Mutations
Call simple_targeted_mutations with:
- mutation_type: "spread" (first try)
- target_k: [k1, k2, k3] from analysis (or empty if no analysis)

## Step 3: Screen with Probes
Call probe_solution on each mutation (aim for c5_bound < 0.385)

## Step 4: Evaluate Best
Call evaluate_solution on 1-2 best probes

## If No Improvement:
Try mutation_type: "bipartite", then "localized"

## Key Rules:
- Call compact_analysis ONCE at start only
- Generate 3 mutations, probe all, evaluate best 1-2
- Keep outputs short to fit token budget
- Diverse mutation types improve coverage
