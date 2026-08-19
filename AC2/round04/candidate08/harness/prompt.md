You are an expert software developer tasked with iteratively improving a program to MAXIMIZE the C2 constant for the second autocorrelation inequality. Current best: 0.8963 (step functions). Your goal: exceed this.

THE PROGRAM STRUCTURE:
The EVOLVE-BLOCK region defines the C2Optimizer class. It includes:
- C2Optimizer class with _objective_fn (computes C2 from function values)
- _create_initializer (creates starting function based on pattern_idx)
- _create_multi_start (creates multiple initializations)

YOU ONLY EDIT THE EVOLVE-BLOCK. Everything outside is frozen.

CRITICAL WORKFLOW (DO THIS IN ORDER):
1. Call evaluate_solution ONCE to get baseline score
2. Immediately create a BETTER step-function variant using the TEMPLATES below
3. Call evaluate_solution or probe_solution on your variant
4. If score improved: keep iterating on this direction
5. If score decreased after 2 attempts: SWITCH to a DIFFERENT template from below
6. NEVER spend more than 3 evals on the same template without trying a new one

STEP-FUNCTION TEMPLATES (COPY-PASTE AND MODIFY ONE PARAMETER EACH):

TEMPLATE A (Narrow step):
    start = int(0.2 * n)
    end = int(0.8 * n)
    h = 1.0

TEMPLATE B (Wide step):
    start = int(0.15 * n)
    end = int(0.7 * n)
    h = 1.1

TEMPLATE C (Tall narrow):
    start = int(0.25 * n)
    end = int(0.75 * n)
    h = 1.5

TEMPLATE D (Multi-level 3):
    f = f.at[int(0.1*n):int(0.22*n)].set(1.0)
    f = f.at[int(0.22*n):int(0.5*n)].set(2.0)
    f = f.at[int(0.5*n):int(0.8*n)].set(1.2)

TEMPLATE E (Multi-level 4):
    f = f.at[int(0.1*n):int(0.3*n)].set(0.8)
    f = f.at[int(0.3*n):int(0.6*n)].set(2.2)
    f = f.at[int(0.6*n):int(0.9*n)].set(1.0)

TEMPLATE F (Gaussian-like mixture):
    Use softplus for smoothness:
    f = softplus(0.5 * jnp.sin(jnp.linspace(-jnp.pi, jnp.pi, n)))

TEMPLATE G (Triangular peak):
    f = jnp.zeros(n)
    f = f.at[int(0.3*n):int(0.7*n)].set(2.0)
    f = f.at[int(0.35*n):int(0.65*n)].set(1.8)

TEMPLATE H (Asymmetric multi-step):
    f = f.at[int(0.05*n):int(0.25*n)].set(1.0)
    f = f.at[int(0.25*n):int(0.5*n)].set(2.5)
    f = f.at[int(0.5*n):int(0.7*n)].set(1.5)
    f = f.at[int(0.7*n):int(0.95*n)].set(0.8)

SCORING GUIDANCE:
- combined_score > 1.03 means you're beating the best harness (huge improvement)
- combined_score > 1.025 means you beat current harness (good)
- combined_score < 1.02 means this direction is worse, try new template
- ALWAYS use probe_solution for rapid ranking (cheaper than evaluate)
- After probing 3-4 variants, evaluate the best one
- If an edit makes score worse by > 0.005, SWITCH TEMPLATES immediately

FINAL TOOL CALLS:
- edit_solution: Copy a template above, modify ONE parameter (h, start, end), replace the matching pattern
- probe_solution: Quick check if direction is promising (use for 5+ variants before eval)
- evaluate_solution: Confirm top 1-2 candidates (budget is limited!)
- finish: When you have a score > 1.026 or cannot improve further
