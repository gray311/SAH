---
name: analysis-first-strategy
description: Always start with correlation analysis, then target mutations at problematic shifts.
---

# Analysis-First Strategy for Erdos C5

## Core Principle
Do not guess - analyze the correlation structure first, then target mutations at the problematic k values.

## Step-by-Step Workflow

1. CALL correlation_analyzer on the current best program
   - Identifies top 5 k values with highest overlap
   - Tells you exactly where to focus

2. CALL structure_inspired_mutations with target_shifts=[problematic_k]
   - Creates mutations specifically to reduce overlap at these k values
   - Not random - targeted structural changes

3. CALL probe_solution on each mutation candidate
   - Screen candidates cheaply
   - Keep those with c5_bound < 0.375

4. CALL evaluate_solution on best 1-2 candidates
   - If combined_score > 1.0, finish

5. If no improvement, REPEAT with different mutation_type
   - Try "spread_peaks", then "bipartite", then "localized"

## Key Rules
- ALWAYS start with correlation_analyzer
- Use target_shifts from analysis
- NEVER do random mutations without analysis
- Evaluate only on candidates with c5_bound < 0.375
