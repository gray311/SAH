---
name: architectural-exploration-protocol
description: Architecture-level search focusing on structural diversity (interval count, peak count, symmetry) over parameter refinement.
---

# Architecture-Level Exploration Protocol

## Core Principle
The current harness tried parameter refinement but failed because the executor could not reliably edit the EVOLVE-BLOCK. Instead, focus on generating COMPLETELY different step function architectures with different numbers of intervals, different peak counts, and different symmetry properties.

## Phase 1: Structural Diversity (iterations 1-12)

### Architecture Types to Explore:

1. Resolution Change: Seed has 600 intervals. Try 400 (coarse) OR 900 (fine).

2. Peak Count Change: Try 2-peak, 3-peak, or 4-peak patterns with symmetric or asymmetric spacing.

3. Asymmetry: Concentrate mass on left side (peak at 0.2-0.4) or right side (peak at 0.6-0.8).

4. Narrow Peak Test: Very narrow high peak with height 2.0-2.8 and width 10% of domain.

## Phase 2: Gradient Refinement (iterations 13-22)
Use JAX gradients for fine-tuning once a promising architecture is found.

## Phase 3: Radical Redesign (iterations 23-30)
Try 300 intervals with 5-level pattern, or 900 intervals with 3 narrow peaks.

## Key Rules
- Structural changes > parameter tweaks
- Use probes to explore architecture variants
- Probe 4-6 variants per iteration
