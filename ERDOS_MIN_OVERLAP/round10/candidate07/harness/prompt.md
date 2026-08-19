You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx
for a step function h: [0,2] -> [0,1] with integral(h)=1.

Current best bound: C5 <= 0.38092303510845016
Goal: Find h with c5_bound < 0.380923 (combined_score > 1.0).

KEY INSIGHT: The seed optimizer uses gradient descent on latent space, which may get stuck in local minima. 
Instead of just tuning its hyperparameters, you should DIRECTLY CONSTRUCT diverse candidate step functions
and test them. The optimal h is likely a specific step-function shape, not a smooth sigmoid transformation.

STRATEGY:
1. FIRST: Call construct_structured_init to generate 5-10 diverse step function candidates
2. Use probe_solution to quickly screen each candidate (check constraint satisfaction and approximate score)
3. Evaluate the top 3 candidates with evaluate_solution (this costs real eval budget)
4. If none improve, try editing the seed's _get_best_initialization() to add NEW structural patterns
5. If still no improvement, consider editing num_intervals (try 400, 1600, 3200) for coarser/finer discretization
6. Use ALL 30 evals strategically: probe many variants cheaply, evaluate only the best few

DO NOT just tune hyperparameters - the seed optimizer is already configured. Focus on FINDING BETTER INITIAL SHAPES.

Focus: Direct structural search with probe screening.
