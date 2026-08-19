---
name: broad-exploration
description: Test 5-10 diverse architectures per eval with internal selection.
---

# Broad Exploration Protocol

## Core Principle

Each eval must test 5-10 diverse architectures. Don't refine one pattern.

## Categories

1. Peak shapes: narrow, wide, medium
2. Multi-peak: bimodal, trimodal, quad-modal
3. Smooth: Gaussian, spline
4. Asymmetric: left-skewed, right-skewed
5. Extreme: very narrow/high/width

## Workflow

1. Generate 5-10 variants across categories
2. Implement with internal argmax selection
3. Evaluate once, record winner's architecture class
4. Next eval: mix 60% from winner class, 40% exploratory

You have 30 evals = 200+ variant tests. Maximize this.
