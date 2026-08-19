---
name: discovery-optimization
description: "Multi-phase Hadamard optimizer for n=29. Phase 1: generate 4 variants (Paley SA, random SA, perturbed Paley, Paley+high-T). Phase 2: probe all, rank. Phase 3: evaluate winner. Phase 4: refine or pivot. Use probes exhaustively, 1 eval per iteration max."
---

# Hadamard n=29 Multi-Phase Optimizer

## Task
Maximize |det(H)| for 29x29 +-1 matrix. Seed score: 0.545692.

## CORE STRATEGY: PROBE-BEFORE-EVALUATE
You have 20 full evals and 30 probes. Use probes for variant ranking, NEVER evaluate more than once per iteration unless score improves by >10%.

## Phase 1: Generate 4 Variant Programs
Each variant is a COMPLETE program implementing ONE construction+search strategy:

### Variant A: Paley + Standard SA
- Build from residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- SA: 5000 iterations, T=3.0, cool=0.995, 3 seeds [42,123,456]
- Uses numpy.linalg.det for all determinants

### Variant B: Random Matrix + SA
- Start with random +-1 matrix
- SA: 5000 iterations, T=4.0, cool=0.995, 3 seeds [789,2024,2025]
- Uses numpy.linalg.det

### Variant C: Perturbed Paley + SA
- Build Paley base, then flip 5% of entries randomly
- SA: 5000 iterations, T=2.5, cool=0.995, 3 seeds [2026,2027,4000]
- Uses numpy.linalg.det

### Variant D: Paley + Aggressive High-T SA
- Build Paley base
- SA: 4000 iterations, T=5.0, cool=0.992, 5 seeds [42,123,456,789,2024]
- Uses numpy.linalg.det

## Phase 2: Probe All Variants
Call probe_solution with each variant code. Collect all 4 probe scores. Rank: highest probe score = best variant.

## Phase 3: Evaluate Winner
Call evaluate_solution ONLY on the #1 probe-ranked variant. Record full score.

## Phase 4: Decision
- If full_score > 0.545692: IMPROVEMENT! Refine this variant: (a) double iterations to 10k, (b) tweak T to 3.5, (c) add 2 more seeds. Generate refined variant, probe, evaluate.
- If full_score <= 0.545692: NO IMPROVEMENT. Pivot to completely different strategy: random start with more seeds, or use Bareiss for final candidate verification, or try different cooling schedule.

## Phase 5: Repeat
Max 30 iterations total. Each iteration: gen -> probe 4 -> eval 1 -> decide -> repeat.

## Tool Usage Cheat Sheet
- construct_paley_variants: Call ONCE at start to get 3 matrices
- fast_rank: Call on any matrix for quick det check (within same run)
- probe_solution: Call ONCE per variant (4 calls = Phase 2). Pick top 1.
- evaluate_solution: Call ONCE per iteration (Phase 3). Wait for result.
- edit_solution: Submit full program code each iteration.

## CRITICAL RULES
1. NEVER evaluate without probing first
2. NEVER use >4 probe calls before evaluate
3. NEVER run >4000 iterations per variant (time budget)
4. ALWAYS use numpy.linalg.det, NEVER Bareiss during search
5. TOTAL RUNTIME MUST BE < 200 seconds
6. REPORT combined_score at end
