---
name: pulse-pattern-search
description: Use generate_structural_variants to propose mathematically-informed pulse patterns. Focus on 4-6 narrow triangular pulses with centers spaced ~0.5 apart. Filter for c5_bound < 0.375 before full evaluation.
---

# Pulse Pattern Search for Erdos C5

## Mathematical Basis
The C5 bound measures maximum overlap between h(x) and its shifts.
Narrow, well-separated triangular pulses minimize this overlap.

Key parameter: pulse width w. Smaller w = less overlap, but too narrow = discretization errors.

Optimal regime: w = 0.12-0.20 for domain=2, N=800.

## Strategy
1. CALL generate_structural_variants with config="narrow_4pulse" (best balance)

2. EXAMINE each candidate's c5_bound (FFT-computed)

3. FILTER: keep only c5_bound < 0.375
   - Candidates with c5_bound >= 0.380 won't beat current best
   - FFT scores are reliable proxies

4. EVALUATE fully: CALL evaluate_solution on filtered candidates

5. ITERATE: If no improvement, try other configs or different topologies

## Why This Works
- Triangular pulses reduce sidelobes
- Regular spacing maximizes distance between mass concentrations
- FFT-based c5 is exact (up to discretization)
- No training needed
