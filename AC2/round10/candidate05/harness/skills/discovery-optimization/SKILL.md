---
name: discovery-optimization
description: "Discover new step function architectures for C\u2082 optimization. Prioritize structural mutations (new patterns, different step counts, new symmetries) over small parameter tweaks."
---

# C₂ Optimization: Structural Discovery Method

Goal: Beat 1.03492 by finding NEW step function architectures, not just tweaking existing ones.

## Phase 1: Structural Exploration (Evals 1-10)
- Try completely new pattern classes:
  * **2-step functions**: Single plateau at different positions/heights
  * **4-step functions**: Asymmetric multi-level with 4 height levels
  * **6-step functions**: Triangular + tails structure
  * **Wide-plateau functions**: Narrow peak with extended wings
  * **Bimodal functions**: Two distinct high regions separated by valley
- Vary step counts: 200, 300, 400, 500, 600 intervals
- Test different symmetries: perfect even, asymmetric left-heavy, asymmetric right-heavy
- For each structural variant, run 3-5 probes before full evaluation

## Phase 2: Focused Refinement (Evals 11+)
- Once you find a score > 1.03492, enter refinement mode
- Now do small mutations (±5% heights, ±3% positions) around the BEST structural variant
- Continue using probes to screen, then single eval to confirm
- If still stuck, backtrack to Phase 1 and try a different archetype

## Phase 3: Archetype Rotation (When Fully Stalled)
- List all 3 seed archetypes: "narrow-tall", "wide-moderate", "multi-level"
- Systematically switch to the next archetype you haven't tried well
- Within each archetype, try 5+ structural variants before moving on

## Probing Strategy
- Each probe batch: Generate 3-5 variants from DIFFERENT structural families
- Compare probe scores and pick winner for full evaluation
- Never just probe 3 minor tweaks of the same pattern

## Recovery Rules
- After 5 evals with no improvement > 1%, switch to new archetype
- If best score stagnates for 3 iterations, restart from completely new random seed with 5 different pattern structures
- Budget ending (< 5 evals): Make ONE structural change to current best, probe it, then eval if promising
