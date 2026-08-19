---
name: piecewise-constant-optimization
description: Replace smooth initializations with piecewise-constant step functions.
---

# Piecewise-Constant Optimization for Erdos Problem

## Why Replace the Initialization?

The seed's 12 patterns are smooth (Gaussian, sinusoidal). The Erdos problem rewards SHARP step functions.

## What to Replace

DELETE the entire _get_best_initialization method and replace with a 3-5 level piecewise-constant function.

## How to Edit

1. Find the _get_best_initialization class method in the seed code.

2. Delete all lines from "def _get_best_initialization" to the next method.

3. Insert the new piecewise-constant code from analyze_and_replace_init.

4. Set num_restarts=1 (no need to try 12 patterns when you have a good one).

5. Set seed_start=0 to use the new initialization.

## Success Pattern

Look for smooth+sharp contrasts: high values (1.2-1.5) on disjoint intervals, low values (0.3-0.6) elsewhere.
