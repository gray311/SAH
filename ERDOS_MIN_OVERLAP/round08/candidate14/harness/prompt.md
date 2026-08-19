You are an expert in mathematical optimization for the Erdős minimum overlap problem.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound
Find a step function h: [0,2]→[0,1] with ∫h=1 that minimizes max_k ∫ h(x)(1-h(x+k))dx.

**CONSTRAINTS**: h∈[0,1], ∫_0^2 h(x)dx = 1

**PROVEN STRATEGIES** (USE THESE CONCRETE APPROACHES):

1. **Direct Construction with probe_solution**: 
   - Build piecewise constant functions analytically
   - Single step: h=1 on [0,1], 0 elsewhere (integral=1 ✓)
   - Double step: h=0.5 on [0,0.5]∪[1.5,2], 0 elsewhere
   - Symmetric 3-step: h=1/3 on [0,0.5]∪[1,1.5], 0 elsewhere
   - Call probe_solution to score before full evaluation

2. **Coarse-to-fine refinement**:
   - Start with num_intervals=50, optimize briefly
   - Then 200, 500, 800 intervals
   - Use momentum/adaptive learning rates

3. **Hybrid approach**: 
   - Manually design candidate breakpoints, optimize only the step heights
   - Keep num_intervals low (100-200) but optimize step values thoroughly

**SEARCH PROCESS**:
- First, construct 3-5 diverse candidates using direct construction
- Probe each to rank them cheaply
- Evaluate the top 2-3 candidates fully
- If no improvement, try coarse-to-fine refinement
- Stay within budget (~30 evals total)

**KEY INSIGHT**: The seed's gradient descent gets stuck in local optima. 
Direct construction of mathematically informed candidates + cheap probing = breakthrough.
