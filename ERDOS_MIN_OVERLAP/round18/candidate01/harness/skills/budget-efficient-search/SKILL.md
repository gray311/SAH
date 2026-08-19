---
name: budget-efficient-search
description: Focus on mutation diversity and probe ranking, evaluate only the single best candidate.
---

# Budget-Efficient Search for Erdos Problem

## Key Insight
30 evals budget means we can only afford 1-2 full optimizations.
Use mutation_diversity_probe to generate candidates and screen them analytically.
Evaluate only the single best candidate to conserve eval budget.

## Workflow
1. mutation_diversity_probe() -> 5 candidates with c5_estimate
2. Pick candidate with LOWEST c5_estimate
3. If c5_estimate < 0.378: evaluate_solution(candidate)
4. If no improvement: repeat step 1 with DIFFERENT mutations
5. MAX 2-3 full evaluations

## Don't Do
- Evaluate multiple candidates (wastes budget)
- Run full optimization without mutation_diversity_probe screening
- Try to get c5 < 0.35 (impossible, focus on beating seed 0.3809)

## Success Criteria
- At least 1 eval with c5_bound < 0.378
- combined_score > 1.0
