---
name: construction-search-playbook
description: Use diverse direct constructions instead of gradient optimization. Generate many different step function shapes and screen with probes.
---

# Construction-Based Search for Erdos Minimum Overlap

## Core Idea
Skip gradient optimization entirely. Generate diverse step function CONSTRUCTIONS directly and evaluate them.

## Step 1: Generate Constructions
Call `generate_construction_library` to get 10-12 different construction families.
Each family is fundamentally different (binary, periodic, Golomb, asymmetric, etc.).

## Step 2: Screen with Probe
For each construction, call `probe_solution` to check:
- Approximate integral (should be ~1)
- Approximate c5_bound (target: < 0.39, ideally < 0.38)

Keep constructions that pass: integral ~1 AND c5_bound < 0.39

## Step 3: Full Evaluation
Call `evaluate_solution` on the top 3-5 constructions that pass probe screening.
Record the exact c5_bound and combined_score.

## Step 4: Iterate with New Families
If no improvement:
- Try constructions with MORE peaks (4, 5, 6 peaks)
- Try CONFINED peaks (narrower width, e.g., sigma=0.08 instead of 0.15)
- Try DIFFERENT mathematical forms:
  * h(x) = sum of |sin(2*pi*k*(x-m))|^alpha
  * h(x) = product of Gaussians
  * h(x) = raised cosine windows
  * h(x) = truncated exponential
- Try SHIFTING known constructions by small amounts (m +/- delta)

## Step 5: Refine
If close but not quite there (c5 ~ 0.382):
- Use NARROWER peaks (width reduced by 20%)
- Adjust peak POSITIONS to better distribute overlap
- Try mixing construction families (e.g., binary + small Gaussian noise)

## Success Metrics
- combined_score > 1.0 (c5_bound < 0.38092303510845016)
- Report the construction that achieved this and its parameters
