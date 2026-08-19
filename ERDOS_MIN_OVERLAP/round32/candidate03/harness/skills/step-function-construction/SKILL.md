---
name: step-function-construction
description: Construct step functions with separated narrow peaks to minimize C5. Focus on harmonic separation - place peaks so they don't overlap at problematic shifts.
---

# Step Function Construction for Erdos C5

## Core Strategy
Design h(x) as a sum of narrow rectangular pulses with total width = 1.0.
Place pulses at positions that minimize maximum overlap across all shifts k.

## Design Principles

1. **Narrow Peaks**: Use widths 0.1-0.3 to minimize self-overlap
2. **Harmonic Separation**: Place peaks at distances that avoid problematic k values
3. **Symmetry**: Symmetric placements often yield lower C5

## Example Constructions

### Two-Peak Design (width=0.25 each)
Peaks at x=0.5, x=1.5
- Separation: 1.0 unit (400 intervals at 800 intervals total)
- Good for minimizing overlap at small k

### Three-Peak Design (width=0.2 each)
Peaks at x=0.33, x=1.0, x=1.67
- Separation: 0.67 and 0.67 units
- Check overlap at k=1, k=2, k=0.67

## Implementation Template

For N=800 intervals (dx=0.0025):
- Peak at position p (0-indexed): h[p-w//2:p+w//2] = 1.0
- Total sum of widths must be N/800 = 1.0

## Verification Steps
1. Sum(h) = 1.0 (integral constraint)
2. All h[i] in [0,1]
3. Use compute_overlap_profile to check max overlap
4. Target: max_overlap < 0.38092303510845016
