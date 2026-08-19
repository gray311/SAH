---
name: discovery-optimization
description: "Combinatorial search for step-function topologies. Explore different piece counts, widths, and height assignments. Avoid tiny parameter tweaks - change structure."
---

# C2 Maximizer: Combinatorial Search Protocol
## Core Principle
Step functions are discrete combinatorial objects. Small parameter tweaks (expand peak by 5%, adjust height by 0.1) fail because the landscape is rugged and discrete. You must explore different TOPOLOGIES: number of pieces, their widths and heights.
## Phase 1: Topology Exploration (iterations 1-12)
Step 1: Generate Structural Mutations - Call generate_structural_mutations to get available topology options - Note the TOTAL number of pieces in each variant
Step 2: Select and Probe Variants (4-7 variants)
Mutation types: A. Change piece count: Try 4, 6, 8, 10, 12 pieces (vary from current) B. Recombine: Merge adjacent intervals, then split one wider interval C. Swap heights: Take current heights, permute them among pieces D. Asymmetric split: Keep same piece count but make left/right peaks different E. Staircase: Create monotonic increase/decrease then plateau
Step 3: Probe and Evaluate - Call probe_solution on 4-6 variants - Rank by probe score - Evaluate top 1-2 variants - If beats record: continue with structural refinement - If no improvement after 3 iterations: switch to Phase 2
## Phase 2: Aggressive Reconfiguration (iterations 13-22)
Step 1: Try Different Piece Counts - Keep record best c2 - Generate variants with 4, 5, 6, 7, 8 pieces (opposite direction from current) - Probe 5 variants
Step 2: Asymmetric and Novel Patterns - Try left/right peak height differences (1.0 vs 2.0, 0.8 vs 2.5) - Try 3-peak configurations - Probe 5 variants, evaluate best
Step 3: Gradient Reinitialization (if gradient norm < 0.001) - Reinitialize 50% of parameters with std=0.15 (larger noise) - Probe 2 variants, evaluate best
## Phase 3: Diversification (iterations 23-30)
Step 1: Novel Topologies - Try 4-6 new configurations with varied patterns - Examples: 4-level function, 3-level asymmetric, wide base + narrow peak - Probe 3 variants, evaluate best
Step 2: Final Submission - If c2 > 0.8962799441554086: submit - Report best combined_score and winning configuration
## Key Rules
- NEVER make tiny parameter tweaks - change STRUCTURE (piece count, widths) - ALWAYS probe 4-6 variants before any full eval (budget: 30 probes + evals) - If stuck: try DIFFERENT topology via generate_structural_mutations (not same mutation type) - Use structural mutations: merge/split intervals, permute heights, vary piece counts
