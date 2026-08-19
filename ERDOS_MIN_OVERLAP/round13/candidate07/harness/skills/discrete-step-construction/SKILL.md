---
name: discrete-step-construction
description: Construct true step functions (piecewise constant) with sharp boundaries, not smooth sigmoid curves. Key - integral must equal exactly 1.
---

# Discrete Step Construction for Erdos Problem

## Core Principle
The problem asks for a STEP FUNCTION, not a smoothed curve. Generate piecewise constant
functions with SHARP boundaries, then enforce integral = 1 exactly.

## Construction Patterns
1. Rectangle pulses: sum of indicator functions on disjoint intervals
2. Multi-interval: k intervals with heights chosen to satisfy integral=1
3. Symmetric: symmetric placement around x=1

## Critical Constraint
Integral must be EXACTLY 1: sum of (height_i * width_i) = 1.0
If your construction doesn't satisfy this, it will be rejected by the evaluator.

## From Step to Latent
The seed's _get_best_initialization returns a latent that gets passed through sigmoid.
For step functions, you have two options:
1. Return the step function directly (modify _get_best_initialization to skip sigmoid)
2. Use very large magnitudes in the step function so sigmoid approximates a hard step

## Why This Works
Smooth sigmoid curves spread mass and create overlap. True step functions can
achieve lower C5 by concentrating mass in optimal locations without smoothing.
