def run(ctx, args):
    """Construct hexagonal shell packing for circle packing."""
    import numpy as np
    
    # Get parameters from context or args
    target_sum = args.get("target_sum", 2.6)
    max_shells = args.get("max_shells", 3)
    
    # Start with central circle
    centers = np.array([[0.5, 0.5]])
    radii = np.array([0.25])
    
    shell_r = 0.25
    remaining = 26 - 1  # 25 more circles
    
    # Add shell 1: 6 circles
    if remaining >= 6:
        shell_r = shell_r / 2
        d = 2 * 0.25  # distance from center
        for j in range(6):
            theta = j * np.pi / 3
            cx = 0.5 + d * np.cos(theta)
            cy = 0.5 + d * np.sin(theta)
            centers = np.vstack([centers, [cx, cy]])
            radii = np.append(radii, shell_r)
        remaining -= 6
    
    # Add shell 2: 12 circles
    if remaining >= 12:
        shell_r = shell_r / 2
        d = 2 * 0.25 * 2
        for j in range(12):
            theta = j * np.pi / 6
            cx = 0.5 + d * np.cos(theta)
            cy = 0.5 + d * np.sin(theta)
            centers = np.vstack([centers, [cx, cy]])
            radii = np.append(radii, shell_r)
        remaining -= 12
    
    # Add shell 3: 18 circles (if needed)
    if remaining >= 18:
        shell_r = shell_r / 2
        d = 2 * 0.25 * 3
        for j in range(18):
            theta = j * np.pi / 18
            cx = 0.5 + d * np.cos(theta)
            cy = 0.5 + d * np.sin(theta)
            centers = np.vstack([centers, [cx, cy]])
            radii = np.append(radii, shell_r)
        remaining -= 18
    
    # Add edge circles if still needed
    if remaining > 0:
        # Simple edge placement in corners and along edges
        edge_positions = [
            (0.1, 0.1), (0.9, 0.1), (0.1, 0.9), (0.9, 0.9),
            (0.5, 0.05), (0.5, 0.95), (0.05, 0.5), (0.95, 0.5)
        ]
        shell_r = 0.12
        for i in range(remaining):
            if i < len(edge_positions):
                cx, cy = edge_positions[i]
            else:
                cx = 0.5 + (i - 8) * 0.05
                cy = 0.5
            centers = np.vstack([centers, [cx, cy]])
            radii = np.append(radii, shell_r)
    
    # Clip to unit square
    centers = np.clip(centers, 0.01, 0.99)
    
    # Return result
    return {"centers": centers.tolist(), "radii": radii.tolist()}
