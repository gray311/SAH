---
name: discovery-optimization
description: "Force structural changes via analytic h(x) patterns. Try bipartite (single jump), multi-modal (3-4 peaks), and Golomb-ruler patterns. Do not tune hyperparameters."
---

# Structural Change Strategy for Erdos C5

## CRITICAL INSIGHT
The seed program already does good hyperparameter tuning. What's missing is **structural diversity** in the h(x) function.

## How to Make Progress

### 1. BIPARTITE (Single Jump) Pattern
h(x) = sigmoid(10 * (x - threshold))
- This creates a step function that jumps at 'threshold'
- Try thresholds: 0.3, 0.4, 0.5, 0.6, 0.7
- Example: h = jax.nn.sigmoid(10 * (x - 0.5))

### 2. MULTI-MODAL (3-4 Peaks) Pattern
h(x) = sigmoid(10 * sin(2*pi*x/N)) or similar
- Creates multiple narrow peaks
- Example: Use a sum of shifted sigmoids
- Or: h = sigmoid(10 * (np.sin(3*pi*x) + 0.1))

### 3. GOLOMB-RULER Pattern
h(x) = 1 at specific marks [0, 0.4, 0.8, 1.2, 1.6]
- Example: For each mark m in [0, 0.4, 0.8, 1.2, 1.6], set h to 1 in a small window
- Use: latent = np.zeros(N); for m in marks: latent[mask] = 4.0; latent -= 2.0

## Editing Instructions

1. REPLACE the entire latent initialization section
2. Pick ONE of the three patterns above
3. Write a clean analytic expression for h(x)
4. Call finish if combined_score > 1.0

## What NOT to Do
- Do NOT tune learning_rate, penalty_strength, num_steps
- Do NOT add small random noise to existing patterns
- Do NOT try more restart patterns

## Success Criteria
- combined_score > 1.0 means you found C5 < 0.38092303510845016
- This is HARD - structural insight is required, not parameter tuning
