Erdos minimum overlap: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
Constraint: integral(h) = 1 exactly.
Current best: C5 <= 0.38092303510845016.

CRITICAL: The optimizer trains for 59000 steps per candidate. Use diverse INITIALizations.

Strategy:
1. CALL generate_diverse_initializations to get 3 structurally different latent vectors (values in [-5,5], pre-sigmoid needed by optimizer)
2. Each candidate should have DIFFERENT support structure (not just amplitude variations)
3. CALL evaluate_solution on ALL 3 candidates (the optimizer will handle integral constraint and training)
4. Never filter candidates before evaluation - the optimizer finds valid h from any latent
5. If no improvement, use generate_diverse_initializations with higher temperature for more variety

Key: The seed optimizer already has pattern generation and training. Give it diverse seeds, let it find the winner.
