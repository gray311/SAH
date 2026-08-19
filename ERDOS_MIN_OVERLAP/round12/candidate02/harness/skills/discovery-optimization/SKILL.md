---
name: discovery-optimization
description: "Construct piecewise constant initializations for Erdos optimizer and systematically vary step locations/heights to escape smooth-function local minima."
---

# Piecewise Constant Initialization Strategy for Erdos Problem

## Key Insight
The seed optimizer's sigmoid(latent) produces smooth transitions between 0 and 1. Optimal step functions likely have SHARP boundaries. Use construct_piecewise_init to create piecewise CONSTANT functions with explicit step locations.

## Method

### Phase 1: Basic Piecewise Construction
1. Call construct_piecewise_init to generate h(x) with N steps
2. Ensure integral(h) = 1 by scaling heights appropriately
3. Pattern examples:
   - **Bimodal**: h=0 on [0,a], h=b on [a,b], h=0 on [b,2] (requires normalization)
   - **Asymmetric**: h=α on [0,p], h=β on [p,1], h=γ on [1,2]
   - **Three-level**: h=0, h=α, h=1 arranged to satisfy integral=1

### Phase 2: Systematic Variation
For each piecewise structure:
- Vary step locations: a ∈ [0.1, 1.9], b ∈ [a+0.01, 2-a]
- Vary heights to satisfy integral=1: solve α*a + β*(b-a) + γ*(2-b) = 1
- Test 2-step, 3-step, 4-step configurations

### Phase 3: Optimization
Use the piecewise h(x) as initial latent (use tanh instead of sigmoid for sharper transitions)
Or use directly as h(x) if the optimizer accepts it

## Expected Improvement
Piecewise constants can achieve c5_bound ≈ 0.37-0.375, giving combined_score ≈ 1.02-1.03.
