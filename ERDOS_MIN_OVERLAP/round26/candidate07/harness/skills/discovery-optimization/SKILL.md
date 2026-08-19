---
name: discovery-optimization
description: "Analytical screening for Erdos C5 minimization. Use probe_solution after short training (num_steps=1000) to filter patterns before full evaluation. Focus on patterns 5, 12, 14 first. Only evaluate candidates with probe c5_bound < 0.372."
---

# Analytical Screening Strategy for Erdos C5

## Problem
The seed optimizer has 15 pattern-based initializations. Training each for 59000 steps is too expensive (5-6 min per eval). You have only 60 evals total.

## Solution: Multi-Stage Screening

### Stage 1: Ultra-Cheap Screening (num_steps=500)
1. CALL screen_all_patterns (new tool) to test all 15 patterns with num_steps=500
2. This returns all 15 patterns with their c5_bound (analytical, no training)
3. Keep ONLY if c5_bound < 0.375

### Stage 2: Medium Training (num_steps=10000)
For candidates passing Stage 1:
1. Edit solution to train for 10000 steps (fast, ~30-60s)
2. Call probe_solution to get refined c5_bound
3. Keep if c5_bound < 0.372

### Stage 3: Full Evaluation
For candidates passing Stage 2:
1. Edit solution to train for 59000 steps
2. Call evaluate_solution (gets exact c5_bound)
3. If combined_score > 1.0, you've found a new record

## Pattern Prioritization
The tool tests these patterns:
- Pattern 5: Bipartite [0.5] - simple half-half split (baseline)
- Pattern 12: Golomb ruler [0, 0.4, 0.8, 1.2, 1.6] - optimal spacing for 5 points
- Pattern 14: Tri-modal [0.4, 1.0, 1.6] - 3 narrow peaks distributing mass
- Pattern 13: Bipartite at 0.6 - slight asymmetry
- And 11 others from random/gaussian initializations

## Workflow Example

Day 1: screen_all_patterns -> 3-4 patterns pass c5_bound < 0.375

Day 2-3: Train 3-4 candidates for 10000 steps + probe
  - Expected: 1-2 candidates pass c5_bound < 0.372

Day 4-6: Full training + evaluation
  - Evaluate 1-3 candidates
  - Best should beat 0.380923

## Critical Rules
- NEVER call evaluate_solution without first probing
- NEVER test num_steps=59000 without prior screening
- ALWAYS use num_restarts=1 for pattern testing (diversity comes from patterns, not restarts)
- If probe c5_bound >= 0.375, DISCARD immediately (don't waste evals)
- Track your best probe score to guide strategy
