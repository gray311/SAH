---
name: constructive-erdos-strategy
description: Use constructive algorithms to build step functions for the Erdos C5 problem. Do not rely on gradient descent.
---

# Constructive Strategy for Erdos C5 Problem

## Core Principle
Build piecewise constant functions directly.

## Known Structures

### 1. Uniform Function
h(x) = 0.5 for all x in [0,2]. Integral = 1.

### 2. Single Support
h(x) = 1 for x in [0,1], 0 elsewhere. Integral = 1.

### 3. Bipartite
h(x) = 1 on [0,0.5] U [1.5,2], 0 elsewhere. Integral = 1.

### 4. Concentrated
h(x) = 2 for x in [0,0.5], 0 elsewhere. Integral = 1.

### 5. Symmetric Pattern
4 active intervals with h = 4/3.

## Execution
1. Use gen_candidates with each structure
2. Evaluate each (30 evals available)
3. If combined_score > 1.0, success!

## Important
- Verify integral h = 1
- Target c5_bound < 0.38092303510845016
