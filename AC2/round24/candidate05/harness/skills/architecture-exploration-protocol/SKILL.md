---
name: architecture-exploration-protocol
description: Step function architectural exploration. Generate different interval counts, symmetries, and multi-level structures. Don''t refine - explore new designs.
---

# C2 Maximizer: Architectural Exploration Protocol
## Core Principle
Don't refine the current best step patterns - generate NEW architectures with different structures.
## Phase 1: Architecture Generation (iterations 1-10)
Step 1: Call design_step_architecture with varied parameters
- Variant A: num_intervals=800, symmetry=even, num_levels=5, target_peak_height=2.0 - Variant B: num_intervals=400, symmetry=asymmetric, num_levels=3, target_peak_height=2.5 - Variant C: num_intervals=600, symmetry=asymmetric, num_levels=4, target_peak_height=2.2
Step 2: Generate 3-4 architectural variants total
Step 3: Probe ALL variants (3-4 probes)
Step 4: Evaluate TOP 1 only
## Phase 2: Iteration (iterations 11-20)
Step 1: If Phase 1 found improvement: refine with small perturbations
Step 2: If no improvement: generate new architecture with different params
## Phase 3: Aggressive Search (iterations 21-30)
Step 1: Try odd-symmetry, wide-base narrow-spine, multi-peak structures
Step 2: Evaluate aggressively on promising probes
## Key Rules
- GENERATE NEW ARCHITECTURES from design_step_architecture - Use probes to filter: 5-8 probes before any full eval - Vary num_intervals [400, 600, 800, 1200], symmetry, num_levels [3-5] - Start from scratch: don't incrementally edit
