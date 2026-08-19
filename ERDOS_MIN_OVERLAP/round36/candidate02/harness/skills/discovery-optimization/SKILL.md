---
name: discovery-optimization
description: "Generate diverse step function templates first, then optimize each with different hyperparameters. Focus on structural changes, not tuning."
---

# Diverse Template Search for Erdos C5

## Core Idea: Try Many Structures, Not Fine Tuning

Instead of tweaking one function, generate many different step function SHAPES and optimize each independently.

## Phase 1: Template Generation

Create these template types:

### Template A: Bipartite (single threshold)
h = jnp.where(x < threshold, 0.5, 0.5) with threshold in [0.25, 1.75]

### Template B: Dual Peaks
h = jnp.where((x >= left) & (x <= right), 1.0, 0.0) with small overlap regions

### Template C: Three Peaks (tripodal)
h = sum of 3 narrow rectangles covering domain with integral=1

### Template D: Boundary-Concentrated
h concentrated near x=0 or x=2 (where overlaps are different)

### Template E: Golomb/Ruler-like
h concentrated at positions that minimize mutual overlap

For EACH template:
1. Normalize so integral(h)=1 exactly
2. Clip to [0,1]
3. Run full optimization with varied hyperparameters

## Phase 2: Hyperparameter Variation

For each template, try:
- num_intervals: [256, 512, 1024, 2048]
- penalty_strength: [40, 60, 80, 100, 120]
- num_steps: [60000, 100000, 150000, 200000]
- base_learning_rate: [0.001, 0.004, 0.01]
- num_restarts: [1, 3, 5]

## Phase 3: Evaluation Strategy

1. Generate 5-8 different template structures
2. For each template, pick ONE good hyperparameter set
3. Evaluate the best 2-3 templates with best scores
4. If score > 1.0, finish immediately
5. Otherwise, modify the best template structure and repeat

## Why This Works

Random initializations fail because they:
- Don't satisfy integral=1
- Have too many small features (high frequency)

Structured templates succeed because they:
- Satisfy constraints by design
- Have controlled frequency content
- Can be optimized in a consistent direction
