---
name: discovery-optimization
description: "Structure-space exploration for step-function optimization. Test different pattern_idx topologies, vary support ratios and peak arrangements. Avoid parameter extraction - patterns are hard-coded in seed."
---

# C2 Maximizer: Structure-Space Exploration Protocol
## Core Principle
The seed's _create_step_initializer has 12+ pattern_idx values with COMPLETELY DIFFERENT structures. Do NOT try to extract parameters from source code - patterns are hard-coded as method bodies. EXPLORE DIFFERENT pattern_idx VALUES to find better topologies.
## Phase 1: Pattern Index Exploration (iterations 1-12)
Step 1: Try New Pattern Indices
- Try pattern_idx values: 0-11 (seed supports at least these, possibly more) - For each NEW pattern_idx: call probe_new_pattern to test it - You have 30 probes - test 2-5 different patterns per iteration
Step 2: Probe and Rank
- Call probe_new_pattern on 2-5 different pattern_idx values - Rank by probe score - Call evaluate_solution on TOP 1 only (if probe >= 1.0)
Step 3: If Beats Record
- Continue with new pattern as baseline - Try to refine: add/remove peaks, adjust support ratios
Step 4: If No Improvement After 12 Iterations
- Switch to Phase 3 (aggressive restructuring)
## Phase 2: Structure Refinement (iterations 13-22)
Step 1: Structural Mutations
If you have a good baseline, try:
- Mutation A: Split highest peak into 2 peaks (double the height at midpoint) - Mutation B: Merge adjacent peaks (average their heights) - Mutation C: Change support ratio (wider/narrower than current pattern) - Mutation D: Add symmetric wings to a central peak
Step 2: Probe Variants
- Probe 2-3 variants - Evaluate best
Step 3: Continue or Switch
- If gradient is flat or no improvement: switch to Phase 3
## Phase 3: Aggressive Restructuring (iterations 23-30)
Step 1: Radical Topology Changes
- Try 3-peak patterns (e.g., low-high-low-high-low with varying heights) - Try asymmetric patterns (e.g., left-weighted vs right-weighted) - Try wide-base narrow-peak (e.g., support 0.1-0.9, peak at 0.4-0.5) - Try bimodal patterns (two distinct high peaks with valley between)
Step 2: Final Evaluation
- Probe 3 variants - Evaluate best - Submit if c2 > 0.8962799441554086
## Key Rules
- NEVER extract parameters from source code - patterns are hard-coded - ALWAYS explore new pattern_idx values - Use probes to test 5-8 structures before full eval - Vary support ratios: 0.15-0.85 (wider may help) - Vary heights: try 1.0-3.0 range - If stuck at iteration 12+: jump to new topology families immediately
