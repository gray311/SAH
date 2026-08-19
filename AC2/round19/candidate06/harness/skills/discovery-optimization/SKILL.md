---
name: discovery-optimization
description: "Systematic step-function mutation with probe-heavy exploration. Build on seed's 12 diverse patterns,\ngenerate controlled mutations, use probes to filter, and refine winners. Escape local optima through\nparameter diversity, not architecture jumping."
---

# C2 Maximizer: Systematic Step-Function Mutation Protocol

## Core Principle
The seed already has 12 diverse step patterns. Don't discard them! Systematically mutate:
- Heights: +/-0.05-0.2
- Positions: shift boundaries by +/-5%
- Combos: merge adjacent levels, create new asymmetric patterns
- Expansions: add new levels between existing ones

## Phase 1: Mutation Exploration (iterations 1-20)

Step 1: Baseline
- Call probe_solution on seed to confirm baseline score (~1.042)

Step 2: Generate Mutations
- Use the new tool mutate_seed_patterns to get 3-5 mutations
- Each mutation should change: height, position, or add/remove a level
- Ensure MUTUAL EXCLUSIVITY: don't just nudge seed; make distinct changes

Step 3: Probe-Heavy Filtering
- Call probe_solution on ALL mutations (target: 15-20 probes)
- Skip full eval if probe score < seed's probe score

Step 4: Evaluate Winners
- Call evaluate_solution on TOP 2 by probe score
- If either beats seed (combined_score > 1.042): switch to Phase 2
- If not: generate MORE mutations, probe, evaluate

Step 5: Iterate
- Continue until iteration 20 or breakthrough

## Phase 2: Refinement (iterations 21-40)

Only if a mutation beat seed:
1. Take best mutation
2. Call mutate_seed_patterns with small mutations (+/-2% parameters)
3. Probe all, evaluate top 1
4. If no improvement after 5 iterations: return to Phase 1 with fresh mutations

## Mutation Types to Try
1. Height Perturbation: change peak heights by +/-0.05-0.2
2. Position Shift: shift boundaries by +/-5%
3. Level Merging: combine adjacent levels into one
4. Level Splitting: add new level between existing ones
5. Asymmetry: make left/right sides different heights
6. Width Adjustment: widen/narrow support regions

## Key Rules
- Use probes for ALL but 1-2 variants per cycle
- Try variations of ALL 12 seed patterns
- Ensure f >= 0 everywhere
- Track best combined_score throughout
- If stuck at iteration 15: generate completely new mutation types
