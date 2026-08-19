---
name: discovery-optimization
description: "Step-function C\u2082 optimizer. The seed already found high-quality multi-level step functions.\nYour job: systematically perturb heights and positions, use probes to rank variants,\ncommit promising ones to full eval. Preserve working structures - don't rewrite templates."
---

# Step-function C₂ Optimization Skill

## Objective
Maximize C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞) starting from seed's multi-level step functions.

## Core Strategy: Parameter Perturbation
The seed program has optimized step-function templates with specific heights (0.62, 0.72, 0.82, 0.92, 1.02, 1.12, 1.32, 1.42, 1.52, 1.62, 1.66, 1.72, 1.92, 2.02, 2.12).
These are NOT random - they represent discovered optima. Your job is to PERTURB THEM systematically.

## Method
1. IDENTIFY THE BASE PARAMETERS: Locate the heights and positions in the seed code.
   Example: f = f.at[int(0.1*n):int(0.2*n)].set(1.12) means position [0.1n, 0.2n) has height 1.12.

2. USE probe_solution BEFORE evaluate_solution:
   - Create 5-10 variants with small perturbations (±0.02 to ±0.05 to heights)
   - Score them all with probe_solution (cheap, ~10s each)
   - Pick the top 2-3 for full evaluation

3. PERTURBATION TYPES:
   - Height perturbation: h → h × (1 ± 0.05)
   - Position perturbation: shift interval boundaries by ±2 intervals
   - Width perturbation: narrow or widen intervals by ±5%

4. SEARCH/REPLACE YOUR EDITS:
   Find exact lines like `f = f.at[int(0.1*n):int(0.2*n)].set(1.12)`
   Replace ONLY the numeric value: `f = f.at[int(0.1*n):int(0.2*n)].set(1.17)`

5. MONITOR AND ADAPT:
   - If probe_score improves → full eval → decide whether to iterate or try new direction
   - If probe_score degrades → discard, try different perturbation
   - If full eval degrades → reset to seed's best, try a different template (pattern_idx 0-12 in seed)

## Tool Usage
- probe_solution: Your PRIMARY exploration tool. Use for all variant ranking.
- evaluate_solution: Confirm promising variants from probe screening.
- parameter_scanner (NEW TOOL): Generate and score multiple perturbations at once.
- edit_solution: Make targeted SEARCH/REPLACE diffs on numeric parameters only.

## Golden Rules
- NEVER rewrite a whole step-function template - only perturb its parameters
- ALWAYS probe before full eval (30 evals = budget; 30 probes = free exploration)
- If stuck at same score, try a DIFFERENT template (pattern_idx 0-12 in seed)
- Budget warning: when evals < 5, only pursue your single best probe variant
