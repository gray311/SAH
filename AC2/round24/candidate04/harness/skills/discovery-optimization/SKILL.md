---
name: discovery-optimization
description: "Architecture-level exploration for C2 maximization. Generate diverse function families (multi-modal, asymmetric, adaptive), test them in parallel, and commit to the best."
---

# C2 Maximizer: Architecture-Level Exploration Protocol

## Core Principle
The current best step pattern is a LOCAL OPTIMUM. Small parameter tweaks won't escape.

## Phase 1: Parallel Architecture Seeding (iterations 1-12)

Step 1: Generate Diverse Architectures
- Call explore_architectures to create 5-8 structurally distinct candidates
- Required architectural diversity:
  * Multi-modal: 2+ distinct peaks with different widths
  * Asymmetric: mass concentrated on left or right half of domain
  * Adaptive-resolution: coarse discretization at tails, fine near peaks

Step 2: Rapid Probe-Based Screening
- Call probe_solution on ALL 5-8 variants (this is cheap!)
- Rank by probe score
- Call evaluate_solution on TOP 2 only

## Phase 2: Gradient Escape + Redesign (iterations 13-24)

Step 1: If Stuck, Redesign
- Call reinitialize_with_architectures
- Try: bimodal, piecewise-linear

Step 2: JAX Gradients Only on Promising Variants
- @jax.grad only if c2 already beats seed
- Take 2 steps (ascent + orthogonal descent)

## Phase 3: Aggressive Architecture Swap (iterations 25-30)

Step 1: Complete Redesign
- Triangular spikes, plateau-step hybrid

Step 2: Final Selection
- Probe 3, evaluate best
- Submit if c2 > 0.8962799441554086
