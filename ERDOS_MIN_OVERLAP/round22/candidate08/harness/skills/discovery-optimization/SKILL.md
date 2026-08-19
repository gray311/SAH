---
name: discovery-optimization
description: "Direct pattern-editing for Erdos C5 optimization. Generate structural edits to the seed's pattern section and screen with probe_evaluation."
---

# Direct Pattern Editing Protocol

## Objective
Create edits that generate new step-function patterns h: [0,2]->[0,1] with integral=1 and lower C5 overlap.

## Method

### Step 1: Generate Candidate Edits
Edit the seed's EVOLVE-BLOCK pattern section to try new structural approaches:
- Two-peak patterns with separation in [0.3, 1.7]
- Three-peak patterns with spacing 0.3-0.6 between centers
- Bi-modal with one peak near 0 and one near 2
- Single broad peak (width 0.4-1.2)
- Clustered peaks (2-3 within [0.5, 1.5])

For each candidate, ensure:
- The Gaussian peak formula is used: h += A * exp(-(x - center)^2 / (2*sigma^2))
- Values are clipped and normalized: h = clip(h, 0, 10), then normalize to integral=1
- The integral constraint is satisfied via normalization (seed does this)

### Step 2: Probe Evaluation
CALL probe_solution on ALL candidate edits to get quick c5_bound estimates.
Skip any with c5_bound >= 0.38 (can't beat seed).

### Step 3: Full Evaluation
CALL evaluate_solution on the 1-2 best candidates (lowest probe c5_bound).

### Step 4: Iterate
If an edit succeeds (combined_score > 1.0), STOP and call finish.
Otherwise, generate NEW edits based on what worked:
- If 2-peak worked, try different separations
- If 3-peak worked, try different spacings
- Vary peak widths (sigma) from 0.08 to 0.25

## Why This Works
- Direct edits target the actual constraint (pattern structure)
- Probe screening filters out bad candidates quickly
- Only ~5-10 evaluations needed if probe signal is strong
- Seed's optimizer will train each candidate - we just need better seeds

## Example Edits

Edit 1 (two-peak, separation=1.0):
Find: "marks = jnp.array([0.0, 0.4, 0.8, 1.2, 1.6])"
Replace with: "peaks = [0.35, 1.35]; for p in peaks: latent = latent.at[...].set(5.0)"

Edit 2 (three-peak, spacing=0.5):
Replace Golomb pattern with: "centers = [0.5, 1.0, 1.5]; for c in centers: mask = abs(x-c)<0.1; latent = latent.at[mask].set(4.0)"

## Warning
Do NOT change hyperparameters (num_intervals, penalty_strength, num_steps).
The seed's optimizer configuration is already tuned - only change the INITIAL PATTERN.
