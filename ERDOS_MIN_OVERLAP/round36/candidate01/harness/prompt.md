Erdos minimum overlap C5: Optimize h: [0,2]->[0,1] to minimize max_k integral h(x)(1-h(x+k))dx.
Constraints: integral(h)=1, h in [0,1]. Current best C5=0.38092303510845016.
GOAL: Achieve c5_bound < 0.38092303510845016 (combined_score > 1.0).

METHOD: Use probe_solution AGGRESSIVELY. The seed has 800 intervals + 120k steps (slow).
Strategy: 
1) Generate 5-10 sparse step functions (5-10 non-zero intervals) - SIMPLER than seed.
2) Probe EACH with probe_solution (fast, 500 intervals).
3) Keep only candidates with c5_bound < 0.381.
4) Evaluate best 1-2 with evaluate_solution.

Sparse patterns to try:
- 2 narrow peaks separated by >=1.0
- 3 narrow peaks
- Alternating pulses with long gaps
- Single wide peak

Always probe BEFORE evaluating. Seed is overcomplicated; simpler is better.
