---
name: pattern-explorer
description: Systematic exploration of circle packing patterns to escape local optima. Use when stuck at same score for 2+ evaluations.
---

# Pattern Explorer Skill

## When to Use
- You are stuck at the same score for 2+ consecutive evaluations
- The current pattern (hexagonal shell) is not improving
- You need to systematically explore different geometric arrangements

## Strategy: Try 5 Distinct Patterns

### Pattern 1: Tight Hexagonal Lattice
Generate a triangular grid with spacing = 0.38
- Row 0: y=0.12, positions at x=0.06, 0.44, 0.82
- Row 1: y=0.33, positions at x=0.19, 0.57, 0.95
- Row 2: y=0.54, positions at x=0.06, 0.44, 0.82
- Row 3: y=0.75, positions at x=0.19, 0.57, 0.95
- Row 4: y=0.96, positions at x=0.06, 0.44, 0.82
Fill 26 positions, compute radii

### Pattern 2: Four-Corner Heavy
Place 8 circles in corners and near corners:
- 4 corners at (0.05,0.05), (0.95,0.05), (0.05,0.95), (0.95,0.95)
- 4 near corners at (0.15,0.15), (0.85,0.15), (0.15,0.85), (0.85,0.85)
- 18 circles in interior using hexagonal packing

### Pattern 3: Asymmetric Perturbation
Start with hexagonal shell (6 + 12 + 8)
Perturb each center by random +/-0.015 in x and y
This breaks symmetry and may allow larger radii

### Pattern 4: Layered Concentric with Variable Spacing
Layer 0 (1 circle): center at (0.5, 0.5)
Layer 1 (6 circles): radius 0.22, hexagonal angles
Layer 2 (9 circles): radius 0.38, hexagonal angles
Layer 3 (10 circles): mix of edge and interior positions

### Pattern 5: Edge-Optimized
Place 12 circles along edges (3 per side, slightly inset)
Place 14 circles in interior using dense hexagonal packing
Allow edge circles to be smaller for better fit

## Implementation Steps

1. Choose one pattern from the 5 above
2. Generate exact coordinates for 26 circles
3. Compute maximum valid radii using the constraint solver
4. Probe the configuration with probe_solution
5. If probe score > current best, evaluate with evaluate_solution
6. If evaluation improves score, adopt the new pattern
7. If stuck, move to next pattern

## Key Parameters to Tune

- Hexagonal spacing: try 0.35, 0.38, 0.40, 0.42
- Shell radii: try 0.20, 0.22, 0.25, 0.28
- Corner inset: try 0.05, 0.08, 0.10
- Perturbation magnitude: try 0.01, 0.015, 0.02

## Expected Outcomes

- Pattern 1 should achieve 0.75-0.80 if lattice is well-tuned
- Pattern 2 should exploit corner space for 0.73-0.78
- Pattern 3 may find 0.74-0.77 by breaking symmetry
- Pattern 4 provides balanced approach, target 0.76-0.82
- Pattern 5 optimizes edge usage, target 0.74-0.79

## Success Criteria

- Any pattern that beats 0.710003 is worth pursuing
- Target is to reach 2.635 sum_radii (which normalizes to ~0.85+)
- If no pattern improves after 3 attempts, try a completely different approach
