# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_of_radii: Sum of all radii
    """
    n = 26
    centers = np.zeros((n, 2))

    # Strategy: Optimized concentric rings with better spacing
    # Layer 0: 1 center circle (largest)
    # Layer 1: 8 circles in octagon
    # Layer 2: 17 circles in outer ring (filling more space)
    
    # Layer 0: Center circle
    centers[0] = [0.5, 0.5]
    
    # Layer 1: 8 circles at 45° intervals
    # Fine-tuned radius for better packing
    ring1_radius = 0.29
    for i in range(8):
        angle = 2 * np.pi * i / 8
        centers[i + 1] = [0.5 + ring1_radius * np.cos(angle), 0.5 + ring1_radius * np.sin(angle)]
    
    # Layer 2: 16 circles in outer ring
    # Adjusted to optimize space usage
    ring2_radius = 0.54
    for i in range(16):
        angle = 2 * np.pi * i / 16
        centers[i + 9] = [0.5 + ring2_radius * np.cos(angle), 0.5 + ring2_radius * np.sin(angle)]
    
    # Clip to ensure everything is inside the unit square with margin
    centers = np.clip(centers, 0.05, 0.95)
    
    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers)
    
    # Calculate the sum of radii
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Uses a more efficient iterative approach that converges to optimal radii.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    
    # Initial radii: distance to borders
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # Iteratively refine radii based on pairwise constraints
    # This converges to a better solution than single-pass scaling
    for _ in range(10):
        for i in range(n):
            # Start with border constraint
            max_r = min(centers[i][0], centers[i][1], 1 - centers[i][0], 1 - centers[i][1])
            
            # Check against all other circles
            for j in range(n):
                if i == j:
                    continue
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                # The constraint: radii[i] + radii[j] <= dist
                # So radii[i] <= dist - radii[j]
                max_r = min(max_r, dist - radii[j])
            
            radii[i] = max_r
    
    # Final pass: ensure all constraints are satisfied
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            if radii[i] + radii[j] > dist:
                # Reduce the larger radius
                if radii[i] >= radii[j]:
                    radii[i] = dist - radii[j]
                else:
                    radii[j] = dist - radii[i]
    
    # Ensure no negative radii
    radii = np.maximum(radii, 1e-6)
    
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
