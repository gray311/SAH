---
name: discovery-optimization
description: "Edit one structural parameter at a time. Evaluate each edit immediately. Budget: max 15 evals total."
---

# Structural Parameter Search

## Strategy
The seed optimizer has 15 pattern types. We need to systematically vary ONE parameter per pattern and evaluate.

## Pattern 13: Bipartite (start here)
Find line: "latent = latent + jnp.where(x < 0.5, 3.0, -3.0)"
Change 0.5 to test values: 0.3, 0.25, 0.2, 0.15

## Pattern 12: Golomb-like
Find "marks = jnp.array([0.0, 0.4, 0.8, 1.2, 1.6])"
Change spacing: [0.0, 0.35, 0.7, 1.05, 1.4] or [0.0, 0.3, 0.6, 0.9, 1.2]

## Pattern 14: Tri-modal
Find peaks [0.4, 1.0, 1.6] and test [0.35, 0.95, 1.55]

## Workflow
1. Edit ONE pattern's ONE parameter
2. EVALUATE immediately
3. If score > 1.0, SUBMIT
4. If score not improved, EDIT NEXT parameter and repeat
5. Max 15 evals total
