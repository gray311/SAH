Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

METHOD FOR THE EDITOR (step-by-step):

1. Generate 5-7 diverse INITIAL HYPOTHESES for h using generate_step_function_template.
   - Use templates: bipartite (single threshold t=0.5), multimodal_3peaks, multimodal_5peaks,
     golomb_ruler (sparse peaks at 0.0,0.4,0.8,1.2,1.6), sinusoidal_threshold, piecewise_constant.
   - VARY num_intervals across hypotheses: try 400, 800, 1600, 3200 (discretization matters!).
   - DO NOT tune hyperparameters yet.

2. For each hypothesis, call probe_solution to quickly score it (approximate c5_bound).
   - Keep only hypotheses with c5_bound < 0.385.

3. For the best 3 hypotheses (lowest c5_bound), call evaluate_solution to get exact scores.
   - If any has combined_score > 1.0, finish immediately.

4. If no hypothesis beats the seed, try structure_inspired_mutations on the BEST single hypothesis.
   - Use mutation types: "spread_peaks", "bipartite", "localized".
   - Create 3-5 mutants for each type. Probe them, evaluate the best 1-2.

5. If still stuck, restart from step 1 with different random seeds.

6. NEVER spend more than 2 full evaluations per hypothesis before probing.
7. NEVER jump straight to hyperparameter tuning before exploring diverse structural hypotheses.

KEY INSIGHT: The seed uses num_intervals=800. The solver should explore a WIDER RANGE of discretizations
(400, 800, 1600, 3200) because the optimal step function might need more or fewer intervals.
Structural diversity (different templates) is more important than hyperparameter tuning.
