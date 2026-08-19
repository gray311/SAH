---
name: systematic-exploration
description: Use systematic_scan to explore multi-peak configurations. Call once with temperature=0.5, then evaluate top candidates.
---

# Systematic Exploration Strategy
## Problem The seed optimizer needs diverse initializations that minimize overlap. Current harness only tries 3 fixed patterns.
## Solution: systematic_scan Tool Generates 6 candidates with systematically varied peak configurations, all with integral=1.0 and precomputed c5_bound.
## Workflow 1. CALL systematic_scan(temperature=0.5, num_peaks=3, peak_spacing="equal") 2. Sort candidates by c5_bound (ascending) 3. CALL evaluate_solution on TOP 2 candidates (lowest c5_bound) 4. If combined_score < 1.0, try: systematic_scan(temperature=0.7, num_peaks=2) 5. Maximum 4-5 full evaluations
## Key Patterns - Equal spacing: peaks at [0.6, 1.0, 1.4] for 3 peaks - Optimized spacing: [0.35, 0.8, 1.3, 1.75] for 4 peaks - Narrow peaks: higher amplitude, smaller width to concentrate mass
## Expected Results With systematic_scan, you should find c5_bound < 0.35 candidates, leading to combined_score > 1.1.
