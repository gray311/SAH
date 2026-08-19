---
name: discovery-optimization
description: "Fine-grained mutation and hill-climbing for Erdos optimization. Focus on perturbations around good solutions."
---

# Hill-Climbing for Erdos Minimum Overlap

## Why this works
The seed solution is ALREADY very good (combined_score ~0.9996).
Large structural changes are unlikely to help. We need FINE-TUNING.

## The Protocol
1. Start with seed program (or previous best)
2. Call mutate_solution with 10 variants
3. Score all 10 variants using probe_solution (cheap!)
4. Pick top 2 by probe score
5. Run FULL evaluation on those 2
6. Take winner, call mutate_solution AGAIN on it
7. Repeat until budget exhausted or no improvement

## Budget Management
- You have 30 evaluations total
- Use ~20 probes (2-3 per mutation round)
- Use ~10 full evaluations (top 2 each round)
- This gives you 10-15 mutation rounds

## Key Principle
IMPROVE incrementally. Small changes to a good solution are more likely to beat the seed
than entirely new constructions from scratch.

## What to watch for
- If all probe scores are worse than seed, STOP - no improvement possible
- If probe scores are flat (all similar), the landscape is smooth
- Always preserve the good structure from the base solution
