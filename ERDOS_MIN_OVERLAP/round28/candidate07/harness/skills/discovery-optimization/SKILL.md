---
name: discovery-optimization
description: "Find better C5 bounds by exploring diverse pattern initializations. Use generate_ready_candidates for cheap screening, evaluate promising candidates fully, then explore new pattern structures if needed. Focus on structural variety, not hyperparameter tuning."
---

# Finding Better C5 Bounds: Pattern Exploration Strategy

## Core Principle

The seed optimizer trains for 59000 steps from various pattern initializations. Our goal is to find INITIALIZATIONS that, when trained, achieve c5_bound < 0.380923.

The analytical tool generate_ready_candidates creates 3 integral-constrained candidates with precomputed c5_bound scores. These are READY TO TRAIN immediately - no hyperparameter search needed.

## Step 1: Analytical Screening (Do This FIRST)

1. CALL generate_ready_candidates(temperature=0.5) - this gives 3 ready-to-train candidates
2. CHECK their c5_bound values:
   - If ANY have c5_bound < 0.385, these are promising starts
   - Call evaluate_solution on ALL such candidates (up to 3 evals)
3. The analytical c5_bound is computed exactly (no training), so we can trust these values

## Step 2: Why Train These Candidates?

- generate_ready_candidates creates candidates that are:
  - Already sigmoid-scaled (h values in [0,1])
  - Already integral-normalized (sum(h)*dx = 1.0 exactly)
  - c5_bound computed via FFT (exact, no approximation)
- These candidates may have c5_bound slightly above 0.380923, but 59000 steps of training could push them below
- Example: c5_bound = 0.382 might train down to 0.379 - combined_score > 1.0!

## Step 3: If No Improvement - Create NEW PATTERNS

The tool generate_ready_candidates uses fixed patterns (Golomb, Bipartite, Tri-modal). We need to explore MORE:

### Pattern Variation 1: More Golomb Marks
Original has 4 marks at [0.0, 0.45, 1.2, 1.8]. Try:
- 5 marks: [0.0, 0.4, 0.8, 1.2, 1.6] (equally spaced)
- 6 marks: [0.0, 0.33, 0.67, 1.0, 1.33, 1.67]
- 7 marks: [0.0, 0.28, 0.57, 0.86, 1.14, 1.43, 1.72]

### Pattern Variation 2: Different Bipartite Splits
Try different split points a:
- a = 0.3: h=1 on [0,0.3), h=0 on [0.3,2)
- a = 0.4: h=1 on [0,0.4), h=0 on [0.4,2)
- a = 0.5: h=1 on [0,0.5), h=0 on [0.5,2)
- a = 0.6: h=1 on [0,0.6), h=0 on [0.6,2)
- a = 0.7: h=1 on [0,0.7), h=0 on [0.7,2)

Remember: integral must be 1, so adjust heights or normalize!

### Pattern Variation 3: 4-Modal (4 Peaks)
Instead of 3 peaks at [0.4, 1.0, 1.6], try 4 peaks:
- [0.3, 0.8, 1.2, 1.7] - spread evenly
- [0.2, 0.7, 1.2, 1.7] - slightly left-biased
- [0.0, 0.5, 1.0, 1.5] - left to right

### Pattern Variation 4: Block Patterns
- 2 blocks: h=1 on [0,a), h=0 on [a,2), then add a small block at the end
- 3 blocks: h=1 on [0,a), h=0 on [a,b), h=1 on [b,2)

## Step 4: Hyperparameters (Last Resort)

Only vary hyperparameters if all pattern exploration fails:
- num_intervals: 400, 800, 1600 (coarser to finer)
- base_learning_rate: 0.001, 0.003, 0.006 (conservative to moderate)
- penalty_strength: 40, 60, 100 (weaker to stronger)
- num_steps: 30000, 59000, 100000 (short to long)

## Step 5: Temperature Variation

If stuck with generate_ready_candidates:
- CALL with temperature=0.8 to get more diverse candidates
- Then evaluate those with c5_bound < 0.385

## Expected Workflow

1. First iteration: generate_ready_candidates - evaluate top candidates
2. If no success: manually edit code to add new patterns (more marks, different modality)
3. Use generate_ready_candidates again with temp=0.8
4. Only then: try hyperparameter variations
5. Submit when combined_score > 1.0

## Why This Works

- Analytical screening finds candidates we would otherwise miss
- Structural pattern diversity explores different regions of the function space
- Lenient threshold (0.385) catches candidates that can improve with training
- Training (59000 steps) can refine a good initialization to beat the current best
