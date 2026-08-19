You are building EXPLICIT step-function candidates for the Erdős C₅ bound problem.

**THE TASK**: Find a step function h: [0,2]→[0,1] minimizing max_k ∫ h(x)(1-h(x+k))dx.
Constraint: ∫h = 1 over [0,2].
Target: combined_score > 1.0 (i.e., c5_bound < 0.38092303510845016).

**DO NOT use gradient descent or Adam optimization**. The seed's optimizer fails because this is a DISCRETE STRUCTURAL problem.

**YOUR APPROACH - Build explicit candidates**:

1. **Define h as piecewise constant with few intervals** (e.g., 2-10 intervals, not 800)
2. **Manually construct h values** that satisfy ∫h=1 and h∈[0,1]
3. **Try different combinatorial patterns**:
   - Single interval: h=1 on [0,1], 0 elsewhere
   - Two intervals: h=0.5 on two regions totaling measure 2
   - Symmetric wave: sin-based patterns centered at x=1
   - Concentrated mass near boundaries or center

4. **Use probe_solution to quickly score ~10-20 variants** before picking best for full eval

5. **Only call evaluate_solution on your best 1-3 candidates**

6. **If no progress after 10 attempts, try radically different structures** (different number of steps, different support regions)

**CONSTRAINT CHECKING**: Before finalizing h, verify:
- All h[i] ∈ [0,1]
- Sum of h[i] × dx = 1.0 (where dx = 2/num_intervals)

**NEW TOOL**: Use pattern_construction to generate explicit step-function candidates with guaranteed constraints.

**BUDGET**: You have ~30 full evaluations. Spend them wisely - test many cheap variants with probes first.
