---
name: discovery-optimization
description: "Analyze correlation structure to guide iterative construction improvement for Erdos minimum overlap"
---

# Erdos Minimum Overlap - Correlation-Guided Iteration
## Core Principle The maximum overlap occurs at specific lags k. You must IDENTIFY which lags and THEN target them.
## Workflow: 1. Start with any valid h (two peaks, integral=1) 2. Call analyze_correlation_structure(h) to get: - Which k values achieve the maximum - The overlap magnitude at each k - Recommendations for adjusting peak positions/widths 3. Edit h based on recommendations: - Reduce peak height to spread mass - Shift peaks to reduce overlap at dominant lags - Add counter-peaks if gaps are too wide 4. Probe the edit to check improvement 5. If still dominated by bad lags, loop back to step 2 6. When correlation looks balanced, run full evaluation
## What analyze_correlation_structure does: - Computes h * (1-h) correlation at all lags - Identifies the top 3-5 lags that contribute to max - Estimates how much to adjust peak positions/widths - Returns actionable edit suggestions
## Key Adjustments: - Peak height: Lower peaks = more spread = lower max correlation - Peak separation: Optimal for 2 peaks is 1/3 to 1/2 of domain width - Peak width: Wider peaks help distribute mass, but too wide increases overlap - Transitions: Use sigmoid scaling, not hard steps - Number of peaks: 2-3 peaks often better than 4+ (simpler, more balanced)
