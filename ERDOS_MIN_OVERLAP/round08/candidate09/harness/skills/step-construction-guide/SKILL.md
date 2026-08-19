---
name: step-construction-guide
description: Method for constructing step functions directly. Use when gradient descent fails.
---

# Direct Step Function Construction

## Why Sigmoid Fails
h = sigmoid(random_noise) creates smooth functions. Optimal C₅ requires sharp steps.

## Pattern 1: Single Block
h = 1 on [0,1], h = 0 on (1,2]. Integral = 1. ✓

## Pattern 2: Double Block  
h = 1 on [0,0.5] U [1.5,2], h = 0 elsewhere. Integral = 1. ✓

## Pattern 3: Centered Mass
h = 0 on [0,0.3) U [1.7,2], h = 1 on [0.3,1.7]. Scale to integral=1.

## Implementation Code
Replace _get_best_initialization with:

def _make_single_block(N):
    mid = N // 2
    return jnp.concatenate([jnp.ones(mid), jnp.zeros(N-mid)])

def _make_double_block(N):
    n_block = N // 4
    return jnp.concatenate([jnp.ones(n_block), jnp.zeros(N-2*n_block), jnp.ones(n_block)])

def _make_uniform(N):
    return jnp.ones(N) * 0.5

def _get_best_initialization(self, seed):
    patterns = [_make_single_block, _make_double_block, _make_uniform]
    best_h, best_score = None, jnp.inf
    for make_h in patterns:
        h = make_h(self.hypers.num_intervals)
        score = self._compute_c5_bound(h)
        if score < best_score:
            best_score, best_h = score, h
    return best_h

## Refinement
1. Start num_intervals=50
2. Try all patterns, evaluate
3. Pick best, increase intervals: 50→200→500→800
4. Fine-tune boundaries by ±5%
