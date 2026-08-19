---
name: discovery-optimization
description: "Use compute_overlap_profile to identify the maximum-overlap shift k, then design step functions\nwith narrow separated peaks that minimize overlap at that k. Start with simple 2-peak or 3-peak\nconfigurations before adding complexity."
---

# Erdos C5 - Step Function Design

## Phase 1: Profile Analysis
1. CALL compute_overlap_profile to see the full overlap landscape
2. Identify k_max where overlap is maximum
3. Note: For step functions, overlap at shift k comes from peaks overlapping with themselves shifted by k

## Phase 2: Design Separated Peaks
For a function with n peaks at positions p1, p2, ..., pn with widths w1, w2, ..., wn:

- The overlap at shift k occurs when peak i overlaps with peak j shifted by k
- To minimize max overlap: place peaks so NO peak overlaps with another at the problematic k
- Simple strategy: if k_max ≈ 1, place peaks separated by >1.5 units
- If k_max ≈ 2, place peaks separated by >2.5 units

## Phase 3: Concrete Designs to Try

### Design A: Two Narrow Peaks (symmetric)
- Peak 1 centered at x=0.5, width 0.2 (height 1.0, contributes 0.1 to integral)
- Peak 2 centered at x=1.5, width 0.2 (height 1.0, contributes 0.1 to integral)
- Add three more peaks of width 0.133 at x=0.35, 0.7, 1.1, 1.45 to reach integral=1
- Separation: 0.2, 0.45, 0.7, 0.75, 0.95 - carefully chosen

### Design B: Three Peaks Equidistant
- Peak 1 at x=0.33, width 0.15 (integral 0.15)
- Peak 2 at x=1.0, width 0.2 (integral 0.2)  
- Peak 3 at x=1.67, width 0.15 (integral 0.15)
- Need 0.5 more: add two small peaks at x=0.7, x=1.35 (width 0.25 each)

### Design C: Four Peaks Quarter-Distributed
- Peaks at x=0.5, 1.0, 1.5 with equal width 0.167 (integral 0.167 each = 0.5)
- Add peaks at boundaries x=0.0, x=2.0 with width 0.25 each (integral 0.25 each = 0.5)
- Separation between adjacent: 0.5 - check overlap at various k

## Phase 4: Verification
1. Compute integral(h) - must equal 1.0 exactly
2. Verify all h(x) in [0,1]
3. Use probe_solution to check c5_bound < 0.382
4. If successful, use evaluate_solution to confirm

## Key Principle
Reducing C5 requires MINIMIZING the maximum overlap across ALL shifts k.
Think: "If I place my peaks here, what shift k causes the worst overlap?"
Then redesign to reduce that specific overlap.
