Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY:

1. CALL compute_overlap_profile ONCE to get the full overlap profile
   - This returns overlap values for ALL k shifts
   - Identify the k with MAXIMUM overlap (problematic shift)

2. Design a STEP FUNCTION with NARROW SEPARATED PEAKS
   - Place peaks at positions that minimize overlap at problematic k
   - For k=1, separate peaks by >1 unit
   - For k=2, separate peaks by >2 units
   - For multiple k, find a configuration that works for all

3. Use probe_solution to screen candidates (c5_bound < 0.382)
4. Use evaluate_solution to confirm improvements
5. Only evaluate when you have a clear structural improvement

KEY INSIGHT: Step functions with WELL-SEPARATED narrow peaks can achieve low overlap.
Think like a Golomb ruler: place "marks" (peaks) so no two marks are at distance k where k creates high overlap.

Example step function structure:
h(x) = 1.0 if x in [a1-b1/2, a1+b1/2] U [a2-b2/2, a2+b2/2] U ... else 0.0
Adjust widths so integral(h) = 1.0

Focus on creating HARMONIC SEPARATION: peaks separated by distances that DON'T create peak overlap.
