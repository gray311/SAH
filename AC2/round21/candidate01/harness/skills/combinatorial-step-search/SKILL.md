---
name: combinatorial-step-search
description: Structural search for step function topologies. Explore different piece counts and configurations.
---

# Combinatorial Step Function Search
## Core Strategy
Step functions are COMBINATORIAL objects. The seed has ~11 intervals. Small parameter tweaks fail - you must explore different TOPOLOGIES.
## Phase 1: Topology Exploration (iterations 1-12)
1. Call generate_structural_mutations to get available topology options 2. Generate 5-7 structural variants: - Change piece count (try 4, 6, 8, 10, 12 pieces) - Merge adjacent intervals - Split intervals - Reassign heights (permute or scale) - Create asymmetric patterns 3. Probe 4-6 variants 4. Evaluate best, continue if improvement
## Phase 2: Aggressive Reconfiguration (iterations 13-22)
1. Try piece counts opposite to current (if 11 pieces, try 6-8) 2. Try novel asymmetric patterns (left/right peak differences) 3. Probe 5 variants, evaluate best 4. If gradient norm < 0.001: reinitialize with std=0.15
## Phase 3: Diversification (iterations 23-30)
1. Try 4-6 new topologies with varied patterns 2. Probe 3 variants, evaluate best 3. Submit if c2 > 0.8962799441554086
## Key Rules
- NEVER tiny parameter tweaks - change STRUCTURE (piece count, widths) - ALWAYS probe 4-6 variants before full eval - If stuck: try DIFFERENT topology via generate_structural_mutations
