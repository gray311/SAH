---
name: discovery-optimization
description: "Escape local optima by exploring new function architectures (spikes, bi-modal, cascades, plateaus) beyond seed step patterns. Use probes to compare architectures, not parameters."
---

C2 Architecture Search - Escape Local Optima

## Diagnosis

The seed achieves 1.03492 with heights 1.40-2.30. Small changes won't improve. Try DIFFERENT ARCHITECTURES.

## Architecture Classes

A. Ultra-Narrow High Spikes
Code: f = jnp.zeros(n); f = f.at[int(0.42*n):int(0.58*n)].set(4.0)
Width 15-25%, Height 3.0-5.0

B. Bi-Modal Dual Peaks
Code: f = jnp.zeros(n); f.at[int(0.18*n):int(0.32*n)].set(2.2); f.at[int(0.68*n):int(0.82*n)].set(2.2)
Two 16-20% peaks, 40% gap, Height 2.0-3.0

C. Asymmetric Cascade
Code: f.at[0:0.25n].set(1.0); f.at[0.25n:0.35n].set(3.5); f.at[0.35n:0.5n].set(2.0)
25% rise, 10% peak (3.5), 15% decay

D. Plateau with Shoulders
Code: f.at[0:0.15n].set(1.5); f.at[0.15n:0.85n].set(2.5); f.at[0.85n:1.0n].set(1.5)
15% shoulder, 50% plateau, 15% shoulder

E. Tri-Modal with Gaps
Code: f.at[0.05n:0.15n].set(2.0); f.at[0.25n:0.35n].set(2.0); f.at[0.65n:0.75n].set(2.0)
Three 10% peaks, 20% gaps

## Execution Protocol

1. Call analyze_step_params at start
2. If heights in 1.0-2.5 range, you are stuck
3. Use probe_solution to test 5-10 DIFFERENT architectures
4. Pick best probe result
5. Only call evaluate_solution on best architecture
6. If no improvement, FORCE new architecture class
7. Never tweak seed parameters - DELETE and rewrite
