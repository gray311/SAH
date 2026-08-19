You are an expert in harmonic analysis and the Erdos minimum overlap problem.

Goal: Beat C5 <= 0.38092303510845016 by finding h: [0,2]->[0,1] with integral(h)=1 minimizing max_k integral(h(x)(1-h(x+k))dx.

KEY INSIGHT: Known constructions beat random optimization. Don't replace the optimizer; ADD specific mathematical blueprints to test.

STRATEGY:
1. Don't delete existing optimizer code - keep the Adam optimizer intact
2. BEFORE optimizing, test 3-4 blueprint functions: bimodal_step, periodic_alternating, golomb_construction
3. For each blueprint: (a) compute c5_bound directly, (b) if promising (<0.3809), fine-tune with optimizer for 2000 steps
4. Use probe_solution to rank blueprints BEFORE full evaluation
5. Full evaluate only on top 2 fine-tuned candidates

BLUEPRINTS to add:
- bimodal_step: Two intervals at [0.25,0.375] and [1.25,1.625] with value 1.0
- periodic_alternating: h=1 on [0,0.5] and [1,1.5], h=0 elsewhere
- golomb_construction: Five narrow peaks at Golomb ruler positions scaled to [0,2]

Workflow:
- Generate 3 blueprint functions, compute exact c5_bound
- For blueprints with c5_bound < 0.3809, use optimizer for 2000 steps with lr=0.01, penalty=1000
- Probe all variants, evaluate top 2 with evaluate_solution
- Target: combined_score > 1.0 (c5_bound < 0.380923)
