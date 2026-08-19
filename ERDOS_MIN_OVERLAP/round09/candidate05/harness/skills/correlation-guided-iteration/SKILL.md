---
name: correlation-guided-iteration
description: Iteratively improve h by analyzing correlation structure and targeting dominant lags. Each iteration - analyze -> edit -> probe -> repeat until balanced.
---

# Correlation-Guided Iteration for Erdos Problem

## Iteration Loop:

1. Start: Create initial h (2-3 peaks, integral=1, sigmoid-scaled)

2. Analyze: Call analyze_correlation_structure(h)

3. Identify dominant lags: Look at which k values give highest overlap

4. Edit strategy based on dominant lag:
   - k=0 dominates: Lower peak heights, spread mass wider
   - k=1 dominates: Shift peaks apart, add counter-peaks
   - k=2,3 dominate: Widen peaks, reduce peak separation
   - Multiple lags: Balance by adjusting all parameters

5. Apply edit: Modify peak positions, widths, or heights
   - Keep integral(h)=1 by adjusting heights proportionally
   - Use sigmoid: h = sigmoid(latent), latent in [-3,3]

6. Probe: Check if max overlap decreased with probe_solution

7. Repeat steps 2-6 until probe shows improvement or 5 iterations

8. Final eval: Run evaluate_solution on best candidate

## Key Parameters:
- num_intervals: 800 (matches seed)
- peak_count: 2-3 (start simple)
- peak_separation: 0.35-0.5 (optimal for C5)
- peak_width: 0.15-0.25 (wide enough to spread, narrow enough to separate)
- peak_height: Adjust to satisfy integral=1 (typically 0.5-0.8 after sigmoid)
- transitions: Smooth with sigmoid, not hard steps
