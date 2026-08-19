---
name: convolution-aware-mutation
description: Use convolution analysis to guide mutations. Analyze spectral gaps and peak concentration, then generate mutations targeting weak frequencies or reducing peak sharpness. Combine with probe-based filtering.
---

# Convolution-Aware Mutation Protocol for C2 Maximization

## Understanding Step-Function Optima

Step functions achieve C2 approximately 0.8963 because their convolutions have:
- Sharp, concentrated peaks which increase the infinity norm
- Energy concentrated in low frequencies
- Symmetric structure creating constructive interference

To beat this, target:
1. Spectral gaps: Add oscillatory components at frequencies with low energy
2. Peak concentration: Broaden the convolution's main lobe
3. Symmetry breaking: Introduce asymmetric features

## Mutation Generation from analyze_convolution Output

After calling analyze_convolution on your best solution:

If spectral_gaps detected (low-energy frequencies):
- Add oscillatory component: multiply base by one plus a cosine term
- Use amplitude 0.1 to 0.3 for subtle but effective modification
- Try 2-3 different gap frequencies from the list

If peak_width less than N over 4 (sharp peak):
- Expand the core region by 15-25%
- Change interval boundaries
- Smooth transitions with linear ramps

If symmetry_ratio approximately 1.0 (too symmetric):
- Make heights asymmetric
- Shift one side by 2-3% of domain

## Probe-First Workflow

1. Call analyze_convolution once early
2. Generate 3-5 mutations based on analysis insights
3. Call probe_solution for each mutation
4. Keep only mutations with probe greater than current best
5. Call evaluate_solution once per remaining candidate
6. If no improvement after 5 evals, re-analyze and try different mutation types

## Key Insights

Small targeted mutations beat random exploration.
Probes are your advantage: 30 probes to filter before 30 evaluations.
Analyze early to understand convolution structure.
Iterate by re-analyzing when stuck.
