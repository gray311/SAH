# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Grid layout"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using a grid-based layout.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Use a simple grid with spacing
    # 6 rows of varying sizes
    centers[0] = [0.1, 0.1]
    centers[1] = [0.3, 0.1]
    centers[2] = [0.5, 0.1]
    centers[3] = [0.7, 0.1]
    centers[4] = [0.9, 0.1]
    
    centers[5] = [0.1, 0.3]
    centers[6] = [0.3, 0.3]
    centers[7] = [0.5, 0.3]
    centers[8] = [0.7, 0.3]
    centers[9] = [0.9, 0.3]
    
    centers[10] = [0.1, 0.5]
    centers[11] = [0.3, 0.5]
    centers[12] = [0.5, 0.5]
    centers[13] = [0.7, 0.5]
    centers[14] = [0.9, 0.5]
    
    centers[15] = [0.1, 0.7]
    centers[16] = [0.3, 0.7]
    centers[17] = [0.5, 0.7]
    centers[18] = [0.7, 0.7]
    centers[19] = [0.9, 0.7]
    
    centers[20] = [0.1, 0.9]
    centers[21] = [0.3, 0.9]
    centers[22] = [0.5, 0.9]
    centers[23] = [0.7, 0.9]
    centers[24] = [0.9, 0.9]
    
    # 26th circle - place it near an edge
    centers[25] = [0.5, 0.05]
    
    # Compute maximum valid radii
    radii = compute_max_radii(centers)
    
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    
    # Initialize radii with border constraints
    radii = np.ones(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(radii[i], x, y, 1 - x, 1 - y)
    
    # Build distance matrix
    dists = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            dists[i, j] = dist
            dists[j, i] = dist
    
    # Iteratively enforce all constraints
    for _ in range(200):
        for i in range(n):
            for j in range(i + 1, n):
                dist = dists[i, j]
                if radii[i] + radii[j] > dist:
                    if radii[i] > radii[j]:
                        radii[i] = dist - radii[j]
                    else:
                        radii[j] = dist - radii[i]
    
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