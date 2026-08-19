Erdos minimum overlap: minimize C5 = max_k integral h(x)(1-h(x+k))dx over h:[0,2]->[0,1] with integral(h)=1.

Seed optimizer: 59k steps gradient descent with 15 init patterns.

FAILURE MODE: Current harness wastes evals on analytical screening of patterns the seed already tries.

NEW STRATEGY: Do NOT generate new candidates. Instead, TUNE the seed optimizer itself by varying hyperparameters (lr, penalty, intervals) and re-running the full optimizer.

Workflow:
1. CALL hyperparameter_sweep to test varied (num_intervals, base_learning_rate, penalty_strength, num_restarts)
2. Pick the best configuration from the sweep results
3. CALL edit_solution to apply the winning config
4. CALL evaluate_solution ONCE with the tuned config
5. If no improvement, try different sweep ranges or search directions

KEY: The seed already generates good candidates. We need to find BETTER hyperparameters for the optimizer.
