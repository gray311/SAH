---
name: discovery-optimization
description: "Systematic peak placement: use systematic_scan to generate integral-normalized candidates with controlled multi-peak configurations. Only evaluate promising candidates."
---

# Systematic Peak Placement for Erdos Optimization
## Why This Works The Erdős problem rewards functions with well-separated support regions to minimize h(x)(1-h(x+k)). Current harness only tried 3 fixed patterns. We need systematic exploration.
## Tool: systematic_scan Generates 6 candidates by varying: - Number of peaks: 2 or 3 - Peak positions: systematically spaced - Peak widths: narrow (to concentrate mass)
Each candidate is: - Integral-normalized (sum(h)*dx = 1.0) - Sigmoid-transformed latent (h in [0,1]) - Pre-computed c5_bound via FFT (no training needed)
## Workflow 1. CALL systematic_scan(temperature=0.5, num_peaks=3, peak_spacing="equal") 2. Sort candidates by c5_bound 3. CALL evaluate_solution on TOP 2 candidates (lowest c5_bound) 4. If both fail (combined_score < 1.0), try with num_peaks=2 and temperature=0.7 5. Maximum 4 full evaluations total
## Expected Patterns - Equal spacing: peaks at 0.67, 1.33 for 2 peaks; 0.6, 1.0, 1.33 for 3 peaks - These minimize self-overlap while maintaining integral=1
