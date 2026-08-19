# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Hexagonal packing with gradient optimization"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using hexagonal packing with gradient-based radius optimization.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Use smaller r for denser packing
    r = 0.10
    h = r * np.sqrt(3)  # Row height ~0.1732
    
    # Row 0: y = r, 5 circles
    centers[0] = [r, r]
    centers[1] = [3*r, r]
    centers[2] = [5*r, r]
    centers[3] = [7*r, r]
    centers[4] = [9*r, r]
    
    # Row 1: y = r + h, 5 circles (offset)
    centers[5] = [2*r, r + h]
    centers[6] = [4*r, r + h]
    centers[7] = [6*r, r + h]
    centers[8] = [8*r, r + h]
    centers[9] = [10*r, r + h]
    
    # Row 2: y = r + 2h, 5 circles
    centers[10] = [r, r + 2*h]
    centers[11] = [3*r, r + 2*h]
    centers[12] = [5*r, r + 2*h]
    centers[13] = [7*r, r + 2*h]
    centers[14] = [9*r, r + 2*h]
    
    # Row 3: y = r + 3h, 5 circles (offset)
    centers[15] = [2*r, r + 3*h]
    centers[16] = [4*r, r + 3*h]
    centers[17] = [6*r, r + 3*h]
    centers[18] = [8*r, r + 3*h]
    centers[19] = [10*r, r + 3*h]
    
    # Row 4: y = r + 4h, 6 circles
    centers[20] = [r, r + 4*h]
    centers[21] = [2*r, r + 4*h]
    centers[22] = [3*r, r + 4*h]
    centers[23] = [4*r, r + 4*h]
    centers[24] = [5*r, r + 4*h]
    centers[25] = [6*r, r + 4*h]
    
    # Clip to unit square
    centers = np.clip(centers, 0.01, 0.99)
    
    # Compute maximum valid radii using gradient-based optimization
    radii = compute_max_radii_gradient(centers)
    
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
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    for _ in range(5):
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                if radii[i] + radii[j] > dist:
                    scale = dist / (radii[i] + radii[j])
                    radii[i] *= scale
                    radii[j] *= scale

    return radii


def compute_max_radii_gradient(centers):
    """
    Compute maximum radii using gradient-based optimization.
    """
    n = centers.shape[0]
    
    # Start with border-constrained radii
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # Build distance matrix
    dists = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            dists[i, j] = dist
            dists[j, i] = dist
    
    # Use gradient descent to maximize sum of radii subject to constraints
    # Objective: maximize sum(radii)
    # Constraints: radii[i] + radii[j] <= dist[i,j] for all i,j
    #             radii[i] >= 0 for all i
    
    radii = radii.copy()  # Start with border constraints
    
    # Multiple passes of constraint enforcement
    for _ in range(30):
        for i in range(n):
            for j in range(i + 1, n):
                if radii[i] + radii[j] > dists[i, j]:
                    # Reduce the larger radius more
                    if radii[i] > radii[j]:
                        # Reduce i to satisfy constraint
                        radii[i] = dists[i, j] - radii[j]
                    else:
                        # Reduce j to satisfy constraint
                        radii[j] = dists[i, j] - radii[i]
    
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