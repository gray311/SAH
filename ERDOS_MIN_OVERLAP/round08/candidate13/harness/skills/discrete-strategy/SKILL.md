---
name: discrete-strategy
description: Abandon gradient descent for C5. Use explicit piecewise constant constructions. Generate candidates, probe to rank, evaluate top few.
---

# Discrete Strategy for C5 Optimization

## Core Idea
Gradient-based methods fail on this non-convex problem.
Manually construct candidate step functions and evaluate.

## Candidate Library
1. Single block: h=1 on [0,1]
2. Uniform: h=0.5 everywhere
3. Two symmetric bumps at x=1
4. Three equal blocks
5. Concentrated narrow peak
6. Oscillatory patterns

## Workflow
1. Generate 5-10 candidates
2. Probe all candidates (~30 probes)
3. Evaluate top 1-2
4. Success if combined_score > 1.0

## Constraints
- integral(h) = 1 exactly
- h in [0,1]
