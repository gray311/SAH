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
        sum_radii: Sum of all radii
    """
    # Initialize arrays for 26 circles
    n = 26
    centers = np.zeros((n, 2))

    # Use a hexagonal-inspired packing with optimized positions
    # Key insight: larger circles in center, smaller in corners/edges
    
    # Central large circle
    centers[0] = [0.5, 0.5]
    
    # First ring: 6 circles in hexagonal pattern, close to center
    # These allow the central circle to be quite large
    ring1_radius = 0.14
    for i in range(6):
        angle = 2 * np.pi * i / 6
        centers[i + 1] = [0.5 + ring1_radius * np.cos(angle), 0.5 + ring1_radius * np.sin(angle)]
    
    # Second ring: 8 circles at larger radius, forming a square-like pattern
    # This leaves room for corner circles
    ring2_radius = 0.28
    for i in range(8):
        angle = 2 * np.pi * i / 8
        centers[i + 7] = [0.5 + ring2_radius * np.cos(angle), 0.5 + ring2_radius * np.sin(angle)]
    
    # Third ring: 11 circles filling corners and edges
    # 4 corner circles (smaller, optimized for corners)
    corner_radius = 0.06
    centers[15] = [0.06, 0.06]
    centers[16] = [0.94, 0.06]
    centers[17] = [0.06, 0.94]
    centers[18] = [0.94, 0.94]
    
    # 4 edge circles
    edge_radius = 0.07
    centers[19] = [0.5, 0.05]
    centers[20] = [0.5, 0.95]
    centers[21] = [0.05, 0.5]
    centers[22] = [0.95, 0.5]
    
    # 3 additional circles in optimal gap positions
    centers[23] = [0.2, 0.2]
    centers[24] = [0.8, 0.8]
    centers[25] = [0.2, 0.8]
    
    # Clip to ensure everything is inside the unit square with margin
    centers = np.clip(centers, 0.01, 0.99)

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
    
    # Initialize with generous starting radii
    radii = np.full(n, 0.15)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders - this is the maximum radius before hitting edge
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Use iterative refinement for better convergence
    for _ in range(20):  # More passes for better optimization
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