---
name: discovery-optimization
description: "Generate diverse step functions with sharp, well-separated peaks to minimize overlap at problematic shifts."
---

# Sharp Peak Generation for Erdos C5

## Core Strategy: Generate Complete Step Functions

Do NOT optimize existing functions. Generate COMPLETELY NEW step function candidates with SHARP, DISTINCT peaks.

## Step Function Construction

A step function h: [0,2]->[0,1] with integral=1 consists of regions where h(x)=1 and h(x)=0.

### Pattern 1: Two Peaks
- Create TWO narrow peaks of width w each
- Separate them by distance d
- Total width: 2*w = 1.0 (so w=0.5)
- Place peaks at positions p1, p2 such that they avoid overlap at problematic shifts
- Example: peaks at [0.25, 0.25+0.5] and [1.0, 1.0+0.5] (but adjust for total width=1)

### Pattern 2: Three Peaks  
- Three narrow peaks of width w each
- Total width: 3*w = 1.0 (so w≈0.333)
- Example positions: [0.1, 0.1+0.333], [0.8, 0.8+0.333], [1.5, 1.5+0.333]

### Pattern 3: Four Peaks
- Four narrow peaks of width w each
- Total width: 4*w = 1.0 (so w=0.25)
- Example: [0.0, 0.25], [0.5, 0.75], [1.0, 1.25], [1.5, 1.75]

### Pattern 4: Non-Uniform Spacing
- Use IRRATIONAL-like or unusual rational spacing
- Peaks at [0.1, 0.1+0.333], [0.7, 0.7+0.333], [1.3, 1.3+0.333], [1.9, 1.9+0.333]
- The key is that peak separations should NOT match the problematic shift k values

## Critical Rules

1. TOTAL WIDTH OF "1" REGIONS MUST BE EXACTLY 1.0
   - If you have N peaks of width w, then N*w = 1.0
   
2. PEAKS SHOULD BE SHARP (step-like), not gradual transitions
   - Use threshold functions: h(x) = 1 where x in [a, b], h(x) = 0 otherwise
   
3. PEAK SEPARATIONS SHOULD AVOID PROBLEMATIC SHIFTS
   - If correlation_analyzer says k=1 is problematic, DON'T place peaks 1.0 apart
   - If k=0.5 is problematic, DON'T use symmetric patterns
   
4. GENERATE FROM SCRATCH, DON'T OPTIMIZE
   - Each evaluation should be a completely new step function candidate
   - Use different peak counts, positions, and widths

## Evaluation Workflow

1. Design a new step function with sharp peaks
2. Verify: integral = 1, all values in [0,1]
3. Call probe_solution to check c5_bound < 0.375
4. If promising, call evaluate_solution
5. If combined_score > 1.0, finish with summary

## Common Mistakes to Avoid

- GRADUAL transitions (use sharp steps, not sigmoid curves)
- TOTAL WIDTH != 1.0 (count your peak widths!)
- Overlapping peaks (separate them well)
- SYMMETRIC patterns that create bad overlaps at shift k=1
