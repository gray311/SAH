# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Corner-heavy pattern"""
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
    n = 26
    centers = np.zeros((n, 2))

    # Place circles in corners and along edges for larger radii
    # 4 large circles in corners
    centers[0] = [0.1, 0.1]
    centers[1] = [0.9, 0.1]
    centers[2] = [0.1, 0.9]
    centers[3] = [0.9, 0.9]
    
    # 4 circles along each edge (12 total)
    centers[4] = [0.3, 0.1]
    centers[5] = [0.7, 0.1]
    centers[6] = [0.1, 0.3]
    centers[7] = [0.1, 0.7]
    centers[8] = [0.3, 0.9]
    centers[9] = [0.7, 0.9]
    centers[10] = [0.9, 0.3]
    centers[11] = [0.9, 0.7]
    
    # 4 edge-mid circles
    centers[12] = [0.5, 0.15]
    centers[13] = [0.5, 0.85]
    centers[14] = [0.15, 0.5]
    centers[15] = [0.85, 0.5]
    
    # 4 center-region circles
    centers[16] = [0.35, 0.35]
    centers[17] = [0.65, 0.35]
    centers[18] = [0.35, 0.65]
    centers[19] = [0.65, 0.65]
    
    # 4 more center circles
    centers[20] = [0.5, 0.4]
    centers[21] = [0.5, 0.6]
    centers[22] = [0.4, 0.5]
    centers[23] = [0.6, 0.5]
    
    # 3 more
    centers[24] = [0.55, 0.55]
    centers[25] = [0.45, 0.55]
    
    centers = np.clip(centers, 0.02, 0.98)
    radii = compute_max_radii(centers)
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


def compute_max_radii(centers):
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