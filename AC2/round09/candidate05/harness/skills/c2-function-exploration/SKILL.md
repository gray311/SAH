---
name: c2-function-exploration
description: Strategy for discovering functions that beat the step-function benchmark. Use bounded internal search within function families (splines, mixtures, hybrids). Always probe new constructions before full evaluation.
---

# C₂ Function Exploration Strategy

## Objective
Maximize C₂ = ||f★f||₂² / (||f★f||₁ ||f★f||_∞)
Benchmark: 0.89628. Seed achieves ~0.926.

## Core Strategy: NEW FUNCTION FAMILIES
The seed uses multi-level step functions. To beat it:
1. Rewrite the function CONSTRUCTION (not just parameters)
2. Try SPLINES, MIXTURES, or HYBRID step+smooth
3. Use BOUNDED internal search (5-10 configs) within each family
4. PROBE before full evaluation

## Function Families

### B-Splines
- Smooth, flexible representation
- Search: knots (10-30), basis weights
- Expected C₂: 0.93-0.95

### Mixture Models
- f(x) = sum(w_i * basis_i(x))
- Bases: gaussian, exponential, step
- Search: n_comp (3-8), weights, base types
- Expected C₂: 0.94-0.97

### Hybrid Step+Smooth
- Steps with sigmoid/tanh transitions
- Search: step locations, transition widths
- Expected C₂: 0.92-0.96

## Workflow

1. PICK A FAMILY (e.g., "mixture")
2. WRITE FUNCTION CONSTRUCTOR with internal search (5-10 configs)
3. PROBE to validate feasibility and approximate score
4. If probe succeeds (score > 0.9, no errors), EVALUATE
5. If evaluation improves, ITERATE on CONSTRUCTION
6. If not, TRY A DIFFERENT FAMILY

## Code Template

def create_function(n, family="mixture"):
    best = None
    best_score = -float('inf')
    
    for i in range(random.randint(5, 10)):
        if family == "mixture":
            n_comp = random.randint(3, 6)
            weights = [random.random() for _ in range(n_comp)]
            weights = [w/sum(weights) for w in weights]
            bases = random.choices(["gaussian", "exponential"], k=n_comp)
            f = build_mixture(n, weights, bases)
            if validate_f(f) and compute_c2_approx(f) > best_score:
                best = f
                best_score = compute_c2_approx(f)
    
    return best

## Key Rules
- NEVER just change hyperparameters
- ALWAYS probe before evaluate
- CHANGE THE CONSTRUCTION, not parameters
- Use 5-10 internal configs, not 100+
