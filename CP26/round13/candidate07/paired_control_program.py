# EVOLVE-BLOCK-START
"""Multi-start greedy circle packing with local optimization for n=26 circles"""
import numpy as np


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Uses iterative constraint satisfaction with gradual scaling.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    
    # Initialize radii from border distances only
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # Iterative constraint satisfaction: gradually scale down radii
    # until no pairs overlap
    max_iter = 100
    for iteration in range(max_iter):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                
                # If radii would cause overlap, scale both down proportionally
                if radii[i] + radii[j] > dist:
                    # Scale both radii down so they just touch
                    scale = dist / (radii[i] + radii[j] + 1e-10)
                    radii[i] *= scale
                    radii[j] *= scale
                    changed = True
        
        # Also ensure minimum radius constraint
        radii = np.maximum(radii, 0.001)
        
        if not changed:
            break
    
    return radii


def optimize_centers(centers, max_iterations=50):
    """
    Local optimization: try small perturbations to improve the sum of radii.
    """
    best_centers = centers.copy()
    best_score = compute_max_radii(best_centers).sum()
    
    for iteration in range(max_iterations):
        improved = False
        for i in range(len(centers)):
            for dx in [-0.01, 0, 0.01]:
                for dy in [-0.01, 0, 0.01]:
                    if dx == 0 and dy == 0:
                        continue
                    new_centers = centers.copy()
                    new_centers[i] = [max(0.01, min(0.99, new_centers[i][0] + dx)),
                                      max(0.01, min(0.99, new_centers[i][1] + dy))]
                    new_score = compute_max_radii(new_centers).sum()
                    if new_score > best_score:
                        best_score = new_score
                        best_centers = new_centers.copy()
                        improved = True
        centers = best_centers
        if not improved:
            break
    
    return centers


def construct_packing():
    """
    Construct an optimized arrangement of 26 circles in a unit square
    that maximizes the sum of their radii.
    
    Uses a greedy placement algorithm with local optimization.
    """
    n = 26
    
    # Initialize with empty positions
    centers = np.zeros((n, 2))
    
    # Try multiple starting configurations
    best_centers = None
    best_sum_radii = 0
    
    for start in range(10):
        centers = np.zeros((n, 2))
        
        # Greedy placement: place each circle at the best position
        for i in range(n):
            best_pos = None
            best_radius = 0
            
            # Sample positions
            for _ in range(500):
                # Focus on different regions
                if start < 3:
                    # Center region
                    x = np.random.uniform(0.2, 0.8)
                    y = np.random.uniform(0.2, 0.8)
                elif start < 6:
                    # Edge regions
                    x = np.random.uniform(0.05, 0.95)
                    y = np.random.uniform(0.05, 0.15)
                else:
                    # Random
                    x = np.random.uniform(0.05, 0.95)
                    y = np.random.uniform(0.05, 0.95)
                
                radius = compute_radius_at_position(x, y, i, centers[:i])
                
                if radius > best_radius:
                    best_radius = radius
                    best_pos = (x, y)
            
            if best_pos is not None:
                centers[i] = best_pos
        
        # Compute sum of radii for this configuration
        radii = compute_max_radii(centers)
        radii = np.maximum(radii, 0.001)
        sum_radii = np.sum(radii)
        
        if sum_radii > best_sum_radii:
            best_sum_radii = sum_radii
            best_centers = centers.copy()
    
    # Use the best configuration
    centers = best_centers
    
    # Clip to ensure inside unit square
    centers = np.clip(centers, 0.01, 0.99)
    
    # Compute maximum valid radii
    radii = compute_max_radii(centers)
    radii = np.maximum(radii, 0.001)
    
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii
# EVOLVE-BLOCK-END
# This part remains fixed (not evolved)
def run_packing():
    """Run the circle packing constructor for n=26"""
    centers, radii, sum_radii = construct_packing()
    return centers, radii, sum_radii


def visualize(centers, radii):
    """
    Visualize the circle packing

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates
        radii: np.array of shape (n) with radius of each circle
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw unit square
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.grid(True)

    # Draw circles
    for i, (center, radius) in enumerate(zip(centers, radii)):
        circle = Circle(center, radius, alpha=0.5)
        ax.add_patch(circle)
        ax.text(center[0], center[1], str(i), ha="center", va="center")

    plt.title(f"Circle Packing (n={len(centers)}, sum={sum(radii):.6f})")
    plt.show()


if __name__ == "__main__":
    centers, radii, sum_radii = run_packing()
    print(f"Sum of radii: {sum_radii}")
    # AlphaEvolve improved this to 2.635

    # Uncomment to visualize:
    visualize(centers, radii)