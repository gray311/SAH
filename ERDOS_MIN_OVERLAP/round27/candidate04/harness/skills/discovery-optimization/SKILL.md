---
name: discovery-optimization
description: "Direct constructive pattern search for Erdos C5 problem. Focus on editing pattern initializations to create new candidate h arrays without training. Key: modify the _get_best_initialization patterns directly using mathematical insight about minimizing max_k integral h(x)(1-h(x+k))."
---

# Direct Pattern Construction for Erdos C5

## Understanding the Problem

We want to minimize: max_k integral_{x in [0,2-k]} h(x)(1-h(x+k)) dx

Key insight: The seed optimizer uses gradient descent on sigmoid(latent) which may get stuck.
Direct pattern construction bypasses training entirely.

## Pattern Design Principles

### 1. Alternating Patterns (Best Hope)
h(x) = 1 on [0,a), h(x) = 0 on [a,2-a), h(x) = 1 on [2-a,2]
- Minimizes overlap with shifts where h overlaps 1-h

### 2. Sparse Peak Patterns  
h has narrow peaks at strategic locations, zero elsewhere
- Peaks at 0, 1, 2 (periodic) may minimize cross-correlation

### 3. Coarse-Grained Patterns
Use fewer intervals (100-400) with broad steps
- Simpler structure may avoid local minima

## Action Plan

1. CALL edit_solution to MODIFY _get_best_initialization patterns:
   - Change pattern 12 (Golomb): marks = [0, 0.5, 1, 1.5] instead of [0,0.4,0.8,1.2,1.6]
   - Change pattern 5 (Bipartite): x < 0.5 -> h=0.9, x>=0.5 -> h=0.1 (bypass sigmoid)
   - ADD new pattern: h = jnp.where(x < 0.33, 0.9, jnp.where(x < 0.66, 0.1, 0.9))

2. For each EDITED pattern:
   - Make h values in [0,1] explicitly
   - Normalize so integral(h) = 1 (multiply by 1.0/sum(h)*N)
   - Call probe_solution to check c5_bound

3. If probe shows c5_bound < 0.375:
   - Call evaluate_solution for final score

4. If stuck after 2-3 pattern edits, try HYPERPARAMETER tuning (num_intervals=100, num_steps=10000)

## Critical Edits to Try

### Edit A: Bipartite with high-low-high
Pattern 5: latent = jnp.where(x < 0.4, 8.0, jnp.where(x < 1.6, -8.0, 8.0))

### Edit B: Three equal blocks
Pattern NEW: latent = jnp.where((x >= 0) & (x < 2/3), 4.0, 
                     jnp.where((x >= 2/3) & (x < 4/3), -4.0, 4.0))

### Edit C: Alternating pairs
Pattern NEW: latent = jnp.where((x >= 0) & (x < 0.5), 5.0,
                     jnp.where((x >= 0.5) & (x < 1.0), -5.0,
                     jnp.where((x >= 1.0) & (x < 1.5), 5.0, -5.0)))

Remember: The seed optimizer TRAINING loop is the problem. 
BREAK the loop by providing better INITIAL h directly.
