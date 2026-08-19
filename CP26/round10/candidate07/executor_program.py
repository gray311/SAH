# EVOLVE-BLOCK-START
"""Multi-start random search circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct an optimized arrangement of 26 circles in a unit square
    that maximizes the sum of their radii.
    
    Uses multi-start random search with improved sampling.
    """
    n = 26
    
    # Try multiple random configurations
    best_centers = None
    best_sum_radii = 0
    
    for start in range(50):  # Try 50 different random starts
        centers = np.zeros((n, 2))
        
        # Greedy placement with improved random sampling
        for i in range(n):
            best_pos = None
            best_radius = 0
            
            # Sample more positions, including corners and edges
            samples = []
            # Add corner regions
            samples.extend([
                (0.1, 0.1), (0.9, 0.1), (0.1, 0.9), (0.9, 0.9),
                (0.05, 0.5), (0.95, 0.5), (0.5, 0.05), (0.5, 0.95),
            ])
            # Add grid positions
            for y in np.linspace(0.1, 0.9, 7):
                for x in np.linspace(0.1, 0.9, 7):
                    samples.append((x, y))
            # Add random samples
            for _ in range(50):
                x = np.random.uniform(0.05, 0.95)
                y = np.random.uniform(0.05, 0.95)
                samples.append((x, y))
            
            for pos in samples:
                x, y = pos
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
    centers = np.clip(centers, 0.001, 0.999)
    
    # Compute maximum valid radii
    radii = compute_max_radii(centers)
    
    # Ensure no negative radii
    radii = np.maximum(radii, 0.001)
    
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


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

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
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