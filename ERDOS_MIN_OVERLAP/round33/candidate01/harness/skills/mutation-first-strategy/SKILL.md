---
name: mutation-first-strategy
description: Use mutation_generator to generate real edits based on correlation analysis.
---

# Mutation-First Strategy for Erdos C5

## Critical Insight
The solver MUST actually EDIT h values, not just analyze them.
Use mutation_generator to generate CONCRETE edit commands.

## Step-by-Step
1. CALL correlation_analyzer -> get top 5 problematic k
2. CALL mutation_generator with:
   - target_shifts = [k1, k2, k3, ...]
   - mutation_type = "narrow_peak" or "shift_local" or "flatten_region"
   - intensity = 0.3
   - width = 0.1
3. The tool returns ACTUAL h array values (real edits!)
4. Use edit_solution to apply the edit (paste new h values)
5. Call probe_solution to screen
6. Call evaluate_solution on best candidates

## Mutation Types
- narrow_peak: Reduce h in narrow windows (helps for small k overlap)
- shift_local: Slightly shift h values (disrupts patterns)
- flatten_region: Make h more uniform in problematic region

## Rules
- ALWAYS call mutation_generator after correlation_analyzer
- Use the returned edits directly with edit_solution
- Intensity controls how strong the mutation is (0.1-1.0)
- Width controls the spatial extent (0.05-0.5)
- Preserve integral(h)=1 (handled automatically)
