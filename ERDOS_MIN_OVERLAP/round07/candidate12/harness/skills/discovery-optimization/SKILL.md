---
name: discovery-optimization
description: "C\u2085 bound optimization harness for finding step functions minimizing max overlap. Uses direct piecewise-constant construction with constraint validation. Avoids gradient descent traps."
---

# Finding Better C₅ Bounds via Direct Construction

## Problem
Minimize max_k ∫₀² h(x)(1-h(x+k)) dx subject to h:[0,2]→[0,1] and ∫h=1.

Current best: 0.380923. Target: < 0.380923.

## Why Seed Fails
The seed uses multi-restart Adam on a latent space through sigmoid. This gets trapped in poor local optima because:
- Random initializations rarely align with optimal support sets
- Gradient flow through sigmoid + sigmoid(·) creates vanishing gradients
- No structural guidance toward piecewise-constant solutions

## Direct Construction Strategy

### Step 1: Define Support Sets
Choose intervals where h(x) = c > 0. Common patterns:
- Single interval: h = 1 on [0,1], h = 0 elsewhere (∫h = 1 ✓)
- Two intervals: h = c on [a,b] and [d,e] with c*(b-a) + c*(e-d) = 1
- Symmetric pattern: h = c on [0,a] ∪ [2-a,2]

### Step 2: Choose Heights and Supports
For a support set S ⊆ [0,2]:
- If using constant height c, set c = 1/|S| where |S| = measure(S)
- Try symmetric, alternating, or clustered patterns

### Step 3: Compute C₅ Bound
- Pad h with zeros beyond [0,2]
- Compute correlation via FFT: corr = IFFT(FFT(h) * conj(FFT(1-h)))
- C₅ = max_k (corr[k] * dx) where dx = 2/num_intervals

### Concrete Examples to Try

**Example A: Single high plateau**
h = 1 on [0,1], h = 0 on (1,2]
Expected: Good baseline, check if beats seed

**Example B: Two narrow peaks**
h = 0.5 on [0, 0.5] ∪ [1.5, 2], h = 0 elsewhere
Expected: Reduces max overlap by spreading mass

**Example C: Concentrated at one point**
h = 2 on [0, 0.5], h = 0 elsewhere
Expected: May increase overlap, explore anyway

**Example D: Alternating pattern**
Divide [0,2] into n equal intervals, set h alternating between c₁ and c₂
Solve for c₁, c₂ such that average height gives ∫h = 1

**Example E: Tapered profile**
h decreases linearly from left to right, then 0
Use quadratic or cubic pieces for smoother transitions

## Implementation Guidance

1. **Start simple**: Begin with 2-3 intervals, optimize only their positions/heights
2. **Validate constraints first**: Before running optimizer, check if ∫h = 1
3. **Use FFT efficiently**: The seed's _compute_c5_bound is correct; focus on better h
4. **Multi-restart with smart seeds**: Instead of random, use 3-5 structurally different initial h vectors
5. **Consider fixing h directly**: Instead of optimizing latent → sigmoid, optimize h values with projection to [0,1] and constraint enforcement

## Using probe_solution
- probe_solution gives approximate score in ~10s (separate budget of 30)
- Use it to rapidly test many constructions
- Only call evaluate_solution when you have a promising candidate

## Using evaluate_solution  
- Consumes 1 of ~30 real evaluations
- Call only when probe confirms good performance or for final scoring
- Report combined_score immediately after

## Failure Recovery
If stuck:
- Change the support structure entirely (not just parameters)
- Try completely different h construction (piecewise constant vs smooth)
- Reduce num_intervals to 50-100 to escape local optima, then increase
