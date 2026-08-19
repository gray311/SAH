---
name: escape-local-optima
description: Escape the seed's local optimum by exploring new function architectures. The seed is at 1.03492; small tweaks won't improve. Try ultra-narrow spikes, bi-modal peaks, cascades, plateaus, tri-modal patterns.
---

Escape Local Optima: Architecture Exploration

## Why the Seed is Stuck

The seed achieves 1.03492 with heights 1.40-2.30. These are carefully optimized local optima. Small parameter changes cannot escape. You must try ENTIRELY DIFFERENT FUNCTION ARCHITECTURES.

## Architecture Escape Plan

### Phase 1: Diagnosis
1. Call suggest_architecture tool
2. Check current_heights output
3. If heights in 0.8-2.8 range - FORCE architecture change
4. If heights outside range - continue with current approach

### Architecture Classes

A. Ultra-Narrow High Spikes
f = jnp.zeros(n)
f = f.at[int(0.42*n):int(0.58*n)].set(4.0)
Width: 15-25%, Height: 3.0-5.0
Why: Sharp peaks can increase L2 norm relative to denominator

B. Bi-Modal Dual Peaks
f = jnp.zeros(n)
f = f.at[int(0.18*n):int(0.32*n)].set(2.2)
f = f.at[int(0.68*n):int(0.82*n)].set(2.2)
Two 16-20% peaks, 40% gap, Height: 2.0-3.0
Why: Separated mass can favor L2 norm

C. Asymmetric Cascade
f = f.at[int(0.0*n):int(0.25*n)].set(1.0)
f = f.at[int(0.25*n):int(0.35*n)].set(3.5)
f = f.at[int(0.35*n):int(0.5*n)].set(2.0)
25% rise, 10% peak (3.5), 15% decay
Why: Asymmetric shapes can exploit convolution

D. Plateau with Shoulders
f = f.at[int(0.0*n):int(0.15*n)].set(1.5)
f = f.at[int(0.15*n):int(0.85*n)].set(2.5)
f = f.at[int(0.85*n):int(1.0*n)].set(1.5)
15% shoulder, 50% plateau, 15% shoulder
Why: Broad mass increases L2 relative to Linf

## Execution Protocol

When to Use
- suggest_architecture returns FORCE architecture change
- Score stalled at 1.03492 for 2+ iterations
- probe_solution shows no improvement
- Budget > 15 evals remaining

Testing Procedure
Per Architecture Class:
1. Use suggest_architecture for blueprint
2. Delete entire EVOLVE-BLOCK
3. Insert new architecture code
4. Call probe_solution to get approximate score
5. Repeat for 3-5 DIFFERENT architecture classes
6. Pick best probe result
7. Call evaluate_solution ONCE on best architecture

Architecture Rotation
- Iteration 0-2: Try class A
- Iteration 3-5: Try class B
- Iteration 6-8: Try class C
- Continue rotating

## Key Rules

1. NEVER tweak parameters of seed architecture - DELETE and rewrite entirely
2. Test architectures in parallel - don't exhaust one before trying another
3. Use probes to compare architectures - not parameters within one architecture
4. One full eval per best architecture - budget is limited (30 evals)
5. If no improvement after 2 architecture classes, FORCE next class immediately
6. Track which architecture class you last tried - don't repeat failed classes
