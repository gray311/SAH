---
name: discovery-optimization
description: "Optimize C\u2082 inequality functions via structured parameter exploration. Analyze seed parameters, probe diverse pattern architectures (width, height, position variations), then evaluate only top candidates."
---

# C₂ Optimization Strategy

## Phase 1: Parameter Analysis
- Call analyze_step_params to extract current step heights/positions.
- Note the pattern class (e.g., "single-peak", "multi-level", "symmetric").

## Phase 2: Divergent Probe Exploration
Generate 5–10 variants that DIFFER FROM the seed's pattern architecture:

- Vary WIDTH: Central peak width from 0.20, 0.25, 0.30, 0.35, 0.40 fractions
- Vary HEIGHT: Try extreme heights (1.0, 1.5, 2.0, 2.5, 3.0) for peaks
- VARY POSITIONS: Shift peaks to 0.20, 0.22, 0.25, 0.27, 0.30, 0.70, 0.73, 0.75
- MULTI-LEVEL: Add 2–3 additional steps (e.g., heights 0.8, 1.5, 2.2, 1.5, 0.8)
- ASYMMETRIC: Non-centered peaks (0.22–0.28 position range)
- PLATEAUS: Long flat regions (height 1.4 from 0.25–0.75)

For each variant:
- Use probe_solution to get an approximate score
- Track the best probe score and its parameters
- If any probe score > 1.035 (beating seed), consider evaluating

## Phase 3: Strategic Evaluation
Evaluate only when:
- A probe variant has probe score > 1.035 (significantly beating seed)
- You have explored 3+ diverse pattern classes
- Budget has > 15 evals remaining (time to iterate more)

## Phase 4: Iteration and Recovery
- If eval score drops: revert to seed parameters, try a DIFFERENT pattern class
- If no improvement after 2 iterations of probe searches: fundamentally change pattern architecture
- As budget ends: make only 1–2 final edits before finishing

## Example Pattern Templates to Try
Pattern A (Ultra-narrow high peak):
  f.at[int(0.35*n):int(0.65*n)].set(2.5)

Pattern B (Triple plateau):
  f.at[int(0.1*n):int(0.3*n)].set(1.2)
  f.at[int(0.3*n):int(0.7*n)].set(1.8)
  f.at[int(0.7*n):int(0.9*n)].set(1.2)

Pattern C (Asymmetric twin peaks):
  f.at[int(0.18*n):int(0.35*n)].set(2.0)
  f.at[int(0.65*n):int(0.82*n)].set(1.5)

## Final Step
When no further improvement is possible, call finish() with a summary of the best function discovered.
