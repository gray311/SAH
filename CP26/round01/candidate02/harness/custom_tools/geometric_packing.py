def run(ctx, args):
    """Generate a structured hexagonal-based circle packing for n=26."""
    import math
    import numpy as np
    
    n = 26
    centers = np.zeros((n, 2))
    radii = np.zeros(n)
    
    # Hexagonal layer-based construction
    # Layer 0: 1 circle at center
    centers[0] = [0.5, 0.5]
    
    # Layer 1: 6 circles in hexagon around center
    # Layer 2: 9 circles in hexagon
    # Layer 3: 10 circles (adjust to get 26 total)
    # 1 + 6 + 9 + 10 = 26
    
    # Layer 1 (6 circles)
    r1 = 0.25
    for i in range(6):
        angle = 2 * math.pi * i / 6
        centers[i + 1] = [0.5 + r1 * math.cos(angle), 0.5 + r1 * math.sin(angle)]
    
    # Layer 2 (9 circles) - offset hexagonal arrangement
    r2 = 0.433  # sqrt(3)/2 * r1 for hexagonal spacing
    for i in range(3):
        for j in range(3):
            angle = 2 * math.pi * i / 3 + math.pi / 6
            centers[i + 7 + j * 3] = [0.5 + r2 * math.cos(angle), 0.5 + r2 * math.sin(angle)]
    
    # Layer 3 (10 circles) - fill remaining space
    r3 = 0.55
    for i in range(10):
        angle = 2 * math.pi * i / 10
        centers[i + 16] = [0.5 + r3 * math.cos(angle), 0.5 + r3 * math.sin(angle)]
    
    # Compute max radii respecting non-overlap and boundaries
    for i in range(n):
        x, y = centers[i]
        # Boundary constraint
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # Pairwise constraints
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            if radii[i] + radii[j] > dist:
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale
    
    sum_radii = np.sum(radii)
    return {"sum_radii": sum_radii, "centers": centers.tolist(), "radii": radii.tolist()}
