# EVOLVE-BLOCK-START
"""Improved random search with corner bias for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct an optimized arrangement of 26 circles in a unit square
    that maximizes the sum of their radii.
    
    Uses multi-start random search with corner bias:
    - Prioritize corner regions where smaller circles can fit
    - Use greedy placement with many samples per position
    """
    n = 26
    
    best_centers = None
    best_sum_radii = 0
    
    for start in range(100):  # More restarts
        centers = np.zeros((n, 2))
        
        # Greedy placement: for each circle, find best position
        for i in range(n):
            best_pos = None
            best_radius = 0
            
            # Sample positions with bias toward corners for early circles
            for _ in range(200):
                if i < 4:
                    # First 4 circles: try corners
                    corner = np.random.randint(0, 4)
                    if corner == 0:
                        x, y = np.random.uniform(0.03, 0.12), np.random.uniform(0.03, 0.12)
                    elif corner == 1:
                        x, y = np.random.uniform(0.88, 0.97), np.random.uniform(0.03, 0.12)
                    elif corner == 2:
                        x, y = np.random.uniform(0.03, 0.12), np.random.uniform(0.88, 0.97)
                    else:
                        x, y = np.random.uniform(0.88, 0.97), np.random.uniform(0.88, 0.97)
                elif i < 8:
                    # Next 4 circles: try edge centers
                    side = np.random.randint(0, 4)
                    if side == 0:
                        x, y = np.random.uniform(0.3, 0.7), np.random.uniform(0.03, 0.12)
                    elif side == 1:
                        x, y = np.random.uniform(0.3, 0.7), np.random.uniform(0.88, 0.97)
                    elif side == 2:
                        x, y = np.random.uniform(0.03, 0.12), np.random.uniform(0.3, 0.7)
                    else:
                        x, y = np.random.uniform(0.88, 0.97), np.random.uniform(0.3, 0.7)
                else:
                    # Remaining circles: random interior
                    x = np.random.uniform(0.05, 0.95)
                    y = np.random.uniform(0.05, 0.95)
                
                # Compute feasible radius at this position
                r = compute_feasible_radius(x, y, i, centers[:i])
                
                if r > best_radius:
                    best_radius = r
                    best_pos = (x, y)
            
            if best_pos is not None:
                centers[i] = best_pos
        
        # Compute sum of radii using consistent method
        radii = compute_max_radii(centers)
        radii = np.maximum(radii, 0.001)
        sum_radii = np.sum(radii)
        
        if sum_radii > best_sum_radii:
            best_sum_radii = sum_radii
            best_centers = centers.copy()
    
    centers = best_centers
    centers = np.clip(centers, 0.001, 0.999)
    radii = compute_max_radii(centers)
    radii = np.maximum(radii, 0.001)
    
    return centers, radii, np.sum(radii)


def compute_feasible_radius(x, y, idx, existing_centers):
    """
    Compute the maximum feasible radius for a circle at (x, y).
    Uses the same logic as compute_max_radii for consistency.
    """
    # Distance to borders
    r = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Use the same logic as compute_max_radii: 
        # each circle's radius is constrained by borders and other circles
        # At placement, we estimate the max possible radius
        # Since we don't know existing radii yet, use dist/2 as conservative
        r = min(r, dist / 2)
    
    return max(r, 0.001)


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position.
    """
    n = centers.shape[0]
    radii = np.ones(n)

    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)

    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            if radii[i] + radii[j] > dist:
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii
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