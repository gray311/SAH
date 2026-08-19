---
name: hill-climbing-eval
description: Hill-climbing - probe many mutations, evaluate best, repeat.
---

Hill-Climbing Protocol for Erdos:

The seed achieves ~0.9996. We need fine-tuning, not new constructions.

Protocol:
1. Start with seed or previous best h
2. Call mutate_solution(h, num_variants=10)
3. Score all 10 with probe_solution (cheap!)
4. Pick top 2 by probe score
5. Run evaluate_solution on those 2
6. Take winner, mutate AGAIN
7. Repeat until no improvement

Budget: ~20 probes + ~10 full evals = 10-15 rounds

Watch for:
- All probes worse than seed? STOP
- Flat scores? Landscape is smooth
- Preserve good structure from base
