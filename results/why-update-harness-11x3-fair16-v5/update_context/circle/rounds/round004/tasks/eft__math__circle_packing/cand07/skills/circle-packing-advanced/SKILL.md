---
name: circle-packing-advanced
description: Advanced skill for circle packing n=26. Provides concrete construction patterns with specific spacing parameters and refinement strategies. AUTO-ENACTED.
---

# Advanced Circle Packing for n=26

## Critical Insight
The seed hexagonal arrangement (0.25, 0.45) is stuck at 0.711. Escape requires **fundamental pattern changes**, not small tweaks.

## Pattern 1: Triangular Grid Selection (Most Promising)
Generate a triangular grid and select 26 closest-to-center positions:

```python
import numpy as np

def triangular_grid_selection(n=26, spacing=0.38):
    """Generate triangular grid, select n closest to center (0.5, 0.5)"""
    centers = []
    # Grid bounds: extend enough to capture 26 points
    max_coord = 0.5 + 2 * spacing
    for i in range(int(max_coord / (spacing * np.sqrt(3)/2)) + 5):
        for j in range(int(max_coord / spacing) + 5):
            x = 0.5 + j * spacing + i * (spacing / 2)
            y = 0.5 + i * (spacing * np.sqrt(3) / 2)
            if 0 <= x <= 1 and 0 <= y <= 1:
                dist = np.sqrt((x - 0.5)**2 + **(y - 0.5)2)
                centers.append((x, y, dist))
    
    # Sort by distance to center and select n closest
    centers.sort(key=lambda c: c[2])
    return np.array([[c[0], c[1]] for c in centers[:n]])
```

**Recommended spacing values to try**: 0.35, 0.36, 0.37, 0.38, 0.39, 0.40, 0.41, 0.42

## Pattern 2: Asymmetric Layered Construction
Instead of perfect hexagonal symmetry, break it slightly:

```python
def asymmetric_layered(n=26):
    """Central circle + asymmetric shells"""
    centers = np.zeros((n, 2))
    centers[0] = [0.5, 0.5]  # Central
    
    # Shell 1: 6 circles, slightly perturbed
    r1 = 0.30
    for k in range(6):
        angle = 2 * np.pi * k / 6 + 0.05 * np.sin(k)  # Small perturbation
        x = 0.5 + r1 * np.cos(angle)
        y = 0.5 + r1 * np.sin(angle)
        centers[k + 1] = [x, y]
    
    # Shell 2: 12 circles, perturbed
    r2 = 0.52
    for k in range(12):
        angle = 2 * np.pi * k / 12 + 0.03 * np.cos(k * 0.5)
        x = 0.5 + r2 * np.cos(angle)
        y = 0.5 + r2 * np.sin(angle)
        centers[k + 7] = [x, y]
    
    # Shell 3: 7 circles - corners + edge midpoints
    # Corners with perturbation
    corners = [(0.1, 0.1), (0.9, 0.1), (0.1, 0.9), (0.9, 0.9)]
    for i, (cx, cy) in enumerate(corners):
        pert = 0.02 * np.sin(i)
        centers[19 + i] = [cx + pert, cy + pert]
    
    # Edge midpoints
    centers[23] = [0.5, 0.15]
    centers[24] = [0.15, 0.5]
    centers[25] = [0.85, 0.5]
    
    return centers
```

## Pattern 3: Corner-Optimized with Variable Radii
Explicitly optimize for corner utilization:

```python
def corner_optimized(n=26):
    """4 corners + edge circles + interior hexagonal core"""
    centers = np.zeros((n, 2))
    
    # 4 corners (smaller circles to fit)
    centers[0] = [0.12, 0.12]
    centers[1] = [0.88, 0.12]
    centers[2] = [0.12, 0.88]
    centers[3] = [0.88, 0.88]
    
    # Edge circles (medium)
    centers[4] = [0.5, 0.15]
    centers[5] = [0.5, 0.85]
    centers[6] = [0.15, 0.5]
    centers[7] = [0.85, 0.5]
    
    # Interior: 18 circles in hexagonal-like pattern
    # Use tighter packing in center
    interior_spacing = 0.32
    for i in range(18):
        # Hexagonal arrangement with perturbation
        row = i // 6
        pos_in_row = i % 6
        x = 0.5 + (pos_in_row - 2.5) * interior_spacing
        y = 0.5 + row * (interior_spacing * np.sqrt(3) / 2) + 0.01 * np.sin(i * 0.7)
        centers[8 + i] = [x, y]
    
    return centers
```

## Pattern 4: Mixed Hex-Edge Strategy
Combine dense hexagonal core with edge-adapted circles:

```python
def mixed_hex_edge(n=26):
    """Dense hexagonal core (19 circles) + edge circles (7)"""
    centers = np.zeros((n, 2))
    
    # Dense hexagonal core: 19 circles (1 + 6 + 12)
    core_spacing = 0.30
    for shell in range(3):
        num_circles = 1 if shell == 0 else 6 * (shell + 1)
        start_idx = 1 + 6 * shell * (shell + 1) // 2
        for k in range(num_circles):
            if shell == 0:
                centers[start_idx] = [0.5, 0.5]
            else:
                angle = 2 * np.pi * k / (6 * (shell + 1))
                r = core_spacing * (shell + 1)
                x = 0.5 + r * np.cos(angle)
                y = 0.5 + r * np.sin(angle)
                centers[start_idx + k] = [x, y]
    
    # Edge circles: 7 circles in corners and edge midpoints
    edge_positions = [
        [0.1, 0.1], [0.9, 0.1], [0.1, 0.9], [0.9, 0.9],
        [0.5, 0.15], [0.5, 0.85], [0.15, 0.5], [0.85, 0.5]
    ][:7]
    for i, (ex, ey) in enumerate(edge_positions):
        centers[19 + i] = [ex + 0.01 * np.sin(i), ey + 0.01 * np.cos(i)]
    
    return centers
```

## Execution Strategy

### Step 1: Try Pattern 1 (Triangular Grid) with Multiple Spacings
- Test spacing: 0.35, 0.36, 0.37, 0.38, 0.39, 0.40
- Use `probe_solution` to quickly rank by position validity
- Evaluate top 2-3 spacing values with `evaluate_solution`

### Step 2: If Pattern 1 Fails, Try Pattern 2 (Asymmetric Layered)
- Add perturbation to break symmetry
- Test different perturbation magnitudes: 0.02, 0.03, 0.04, 0.05

### Step 3: Try Pattern 3 (Corner-Optimized)
- Explicit corner placement with smaller radii
- May allow larger interior circles

### Step 4: Try Pattern 4 (Mixed Strategy)
- Dense core + edge adaptation
- Often beats pure hexagonal

### Step 5: Iterative Refinement
After selecting a promising pattern:
1. Compute initial radii
2. Calculate gradient of sum_radii w.r.t. positions
3. Move positions by 0.005-0.01 in improvement direction
4. Re-compute radii
5. Repeat 3-5 times before final evaluation

## Key Parameters to Tune

| Parameter | Range | Effect |
|-----------|-------|--------|
| Triangular grid spacing | 0.35-0.42 | Controls density |
| Shell radius multiplier | 0.45-0.55 | Controls shell spacing |
| Perturbation magnitude | 0.01-0.05 | Breaks symmetry |
| Corner offset | 0.10-0.15 | Fits corners |
| Interior spacing | 0.28-0.35 | Core density |

## Common Mistakes to Avoid

1. **Don't start with the seed hexagonal pattern** - it's a local optimum
2. **Don't evaluate every variant** - use probe_solution first
3. **Don't assume perfect symmetry** - asymmetry often helps
4. **Don't forget edge circles** - they can be smaller but add to sum
5. **Don't exceed 5-7 evaluations per pattern type** - stay within budget

## Success Criteria

- Beat 0.711 (current best)
- Target: 0.85+ (approaching theoretical limits)
- Must be valid (no overlaps, all circles in square)
