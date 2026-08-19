---
name: discovery-optimization
description: "Step-function space exploration: systematically explore diverse step patterns, use probes to rank before full eval. Stay in step-function space - it's the current champion."
---

# Step-Function C2 Optimizer Protocol

## Core Principle
Step functions are the current champion (0.89628). Don't abandon them. Systematically explore the step-function space with diverse patterns and probe-based filtering.

## Phase 1: Diverse Step Discovery (iterations 1-12)

Step 1: Analyze Current Best
- Note: peak positions (as fraction of [0,1]), height values, number of levels, support width
- Question: What structural feature might be limiting it?

Step 2: Generate Diverse Step Variants
Create 3-5 completely different step functions:

Variation A - Different Peak Position:
  Move the high step to different positions: [0.25, 0.30, 0.35] × [0.65, 0.75, 0.85]

Variation B - Different Height Configurations:
  Try heights in range [1.3, 2.5]. Example: [0.7, 1.5, 2.0, 1.5, 0.7]

Variation C - Different Number of Levels:
  2-level, 3-level, 4-level, 5-level, 6-level functions
  Example 4-level: [0.1, 0.3, 0.5, 0.7, 0.9] with heights [0.6, 1.3, 2.0, 1.3, 0.6]

Variation D - Asymmetric Support:
  Shift support to left or right: [0.05-0.8] or [0.2-0.95]

Variation E - Multi-Peak Structure:
  Two high regions separated by valley: [0.0-0.3]=a, [0.3-0.4]=high, [0.4-0.6]=low, [0.6-0.9]=high, [0.9-1.0]=a

Step 3: Probe-Based Filtering
- Call probe_solution on ALL generated variants (use your 30 probe budget)
- Record probe scores relative to seed (1.0 = seed score)
- Skip any with probe < 0.95 (too weak to warrant full eval)

Step 4: Full Evaluation
- Evaluate TOP 2 by probe score
- If either beats 0.89628: proceed to Phase 2
- If neither beats: generate FRESH variants (not mutations) and repeat

## Phase 2: Precision Tuning (iterations 13-30)

Only if a variant beat the record:
1. Analyze the winning architecture
2. Generate 3 variants with SMALL mutations:
   - Height: +/-0.05 per level
   - Positions: +/-2% of num_intervals
   - Add ONE level or remove ONE level
3. Probe all, evaluate TOP 1
4. If no improvement after 3 iterations: restart Phase 1 with new random seeds

## Critical Rules
- STAY IN STEP-FUNCTION SPACE - proven it works
- PROBE BEFORE FULL EVAL - 30 probes, use them to explore 15-20 variants
- If probe < 1.0, SKIP full eval
- After iteration 10 with no improvement: generate COMPLETELY NEW patterns
- Maximum 2 full evals per iteration cycle
