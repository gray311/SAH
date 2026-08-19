Erdos minimum overlap problem: find h: [0,2]->[0,1] with integral(h)=1 minimizing max_k integral h(x)(1-h(x+k))dx.

Current best bound: C5 <= 0.38092303510845016
Goal: combined_score > 1.0 (c5_bound < 0.380923)

CRITICAL: 8 previous harness attempts all FAILED at seed. The seed program uses 12 random patterns with Gaussian noise - this approach is broken for improvement.

YOUR TASK: Replace ALL random initialization with DETERMINISTIC mathematical constructions.

Step 1: Delete the loop over 12 random patterns in _get_best_initialization
Step 2: Delete all jax.random.normal calls adding noise
Step 3: Add exactly 4-5 deterministic constructions (no random, no noise)
Step 4: Scale each to ensure integral(h)=1: h = sigmoid(latent); scale = 1.0/(sum(h)*dx); h = h*scale
Step 5: Set num_steps=120000, num_restarts=2, base_learning_rate=0.01
Step 6: Implement phased optimization: (0-40000): lr=0.01, penalty=5000; (40000-80000): lr=0.003, penalty=15000; (80000-120000): lr=0.001, penalty=50000
Step 7: Use probe_solution to rank constructions, evaluate top 2

Five constructions to implement:
- BIMODAL_TIGHT: Two peaks at x=0.25 and x=0.75 with bw=0.12, using exp(-(x-a)/bw)^2 * 25
- TRIANGULAR_3STEP: Three levels [10,0,-5] at phases [0,1/3,2/3] using step functions
- GOLOMB_5: Five peaks at marks [0,0.5,1.5,2.5,2.0] with widths [0.08,0.12,0.08,0.10,0.10], using exp(-(x-m)/w)^2 * 20
- BIQUADRATIC_4PEAK: Four peaks at [0.2,0.4,1.0,1.6] with bw=0.08, using exp(-(x-p)/bw)^2 * 25
- PERIODIC_ALTERNATING: Alternating pattern using 2*(x<0.5)-1 times 3.0

WORKFLOW: Generate 4-5 deterministic constructions, run 30000 steps each, probe_rank them, evaluate top 2, submit best.
