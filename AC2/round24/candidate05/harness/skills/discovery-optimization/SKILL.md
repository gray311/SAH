---
name: discovery-optimization
description: "Architectural exploration over step function designs. Generate different interval counts, symmetries, and multi-level structures. Don''t refine - redesign."
---

# C2 Maximizer: Architectural Exploration Protocol
## Core Principle
The current best (0.8962799441554086) uses specific step patterns. Instead of refining them, generate NEW architectures: different interval counts, symmetries, and peak structures.
## Phase 1: Architecture Generation (iterations 1-10)
Step 1: Generate New Architectures
- Call design_step_architecture with parameters: - num_intervals: try [400, 600, 800, 1200] - symmetry: ["even", "none", "asymmetric"] - num_levels: [3, 4, 5] - target_peak_height: [1.5, 2.0, 2.5]
Step 2: Generate 3-4 Architectural Variants
- Variant A: Even symmetry, 5 levels, 800 intervals - Variant B: Asymmetric, 3 levels, 400 intervals - Variant C: High peak (2.8), narrow support, 600 intervals
Step 3: Probe and Evaluate
- Probe ALL variants (3-4 probes) - Evaluate TOP 1 only - If beats record: continue Phase 1. If not: try different architectural params.
## Phase 2: Refinement (iterations 11-20)
Step 1: If improvement found, refine
- Take best from Phase 1 - Small perturbations: adjust peak width by 5%, height by 0.05 - Probe 2 variants, evaluate best
Step 2: If no improvement after 3 iterations:
- Generate new architecture with different seed - Continue Phase 1
## Phase 3: Aggressive Search (iterations 21-30)
Step 1: Mix and match
- Odd-symmetry peaks - Wide base with narrow spike - Multiple narrow peaks
Step 2: Evaluate aggressively
- If probe shows promise, evaluate immediately - Use remaining evals to explore diverse architectures
## Key Rules
- GENERATE NEW ARCHITECTURES, don't refine old ones - Use probes to filter: 5-8 probes before any full eval - Call design_step_architecture every iteration with varied parameters - Start from scratch: don't incrementally edit, fully redesign
