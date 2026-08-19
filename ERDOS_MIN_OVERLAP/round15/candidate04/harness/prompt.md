Task: Minimize max_k integral h(x)(1-h(x+k)) dx for step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016

STRATEGY: The seed's _get_best_initialization has 12 pattern variations. 
Most fail constraints or give high c5_bound. 

KEY INSIGHT: Don't invent new patterns - OPTIMIZE the existing 12 patterns by:
1. Editing each pattern's latent to SATISFY integral(h)=1 constraint BEFORE optimization
2. Running FULL optimization (not just single-step) on promising initializations
3. Using probe_solution to quickly filter constraint violations

Steps:
1. CALL generate_diverse_init to get 4 baseline patterns
2. For each pattern, EDIT the seed's _get_best_initialization to return ONLY that pattern's latent
3. Edit _objective_fn to use h = sigmoid(latent_scaled) where latent_scaled = latent / sum(latent) to enforce integral=1
4. Call evaluate_solution on EACH pattern (use all evals - we have 30, and 12 patterns is manageable)
5. If one pattern works, ADD another optimization run with tuned hyperparameters

Focus: Make each of the 12 existing patterns work better, not create new patterns.


Tool usage:
- edit_solution: Change _get_best_initialization to use single pattern, add constraint enforcement
- evaluate_solution: Run full optimization on a single pattern (up to 59000 steps)
- probe_solution: Check constraint satisfaction before full eval (save evals for promising patterns)
