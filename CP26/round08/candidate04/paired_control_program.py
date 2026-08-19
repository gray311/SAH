# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using a cluster-based approach to reduce pairwise constraints.
    
    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Strategy: Create clusters of circles that are well-separated
    # This reduces the impact of pairwise constraint scaling
    
    # Cluster 1: Center region (7 circles)
    # These can have larger radii due to central position
    centers[0] = [0.5, 0.5]
    r_center = 0.25
    for i in range(1, 7):
        angle = 2 * np.pi * i / 6
        centers[i] = [0.5 + r_center * np.cos(angle), 0.5 + r_center * np.sin(angle)]
    
    # Cluster 2: Corner regions (8 circles)
    # These are positioned to maximize corner space
    corners = [(0.07, 0.07), (0.93, 0.07), (0.07, 0.93), (0.93, 0.93)]
    for i, (x, y) in enumerate(corners):
        centers[7 + i] = [x, y]
    
    # Cluster 3: Edge regions (11 circles)
    # These are positioned along the edges
    # Bottom edge
    centers[11] = [0.5, 0.10]
    centers[12] = [0.25, 0.10]
    centers[13] = [0.75, 0.10]
    # Top edge
    centers[14] = [0.5, 0.90]
    centers[15] = [0.25, 0.90]
    centers[16] = [0.75, 0.90]
    # Left edge
    centers[17] = [0.10, 0.5]
    centers[18] = [0.10, 0.25]
    centers[19] = [0.10, 0.75]
    # Right edge
    centers[20] = [0.90, 0.5]
    centers[21] = [0.90, 0.25]
    centers[22] = [0.90, 0.75]
    # Additional circles in gaps
    centers[23] = [0.30, 0.30]
    centers[24] = [0.70, 0.70]
    centers[25] = [0.30, 0.70]
    
    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers)
    
    # Calculate the sum of radii
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


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