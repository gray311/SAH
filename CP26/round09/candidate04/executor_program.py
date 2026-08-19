# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Optimized hexagonal grid"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using an optimized hexagonal grid pattern.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Use a hexagonal grid with carefully tuned parameters
    # The key is to use positions that allow for larger radii
    
    # Use a smaller scale to spread circles more evenly
    base = 0.10
    h = base * np.sqrt(3)
    
    # Row 0: 5 circles
    y0 = base
    centers[0] = [base, y0]
    centers[1] = [3*base, y0]
    centers[2] = [5*base, y0]
    centers[3] = [7*base, y0]
    centers[4] = [9*base, y0]
    
    # Row 1: 5 circles (offset)
    y1 = y0 + h
    centers[5] = [2*base, y1]
    centers[6] = [4*base, y1]
    centers[7] = [6*base, y1]
    centers[8] = [8*base, y1]
    centers[9] = [10*base, y1]
    
    # Row 2: 5 circles
    y2 = y0 + 2*h
    centers[10] = [base, y2]
    centers[11] = [3*base, y2]
    centers[12] = [5*base, y2]
    centers[13] = [7*base, y2]
    centers[14] = [9*base, y2]
    
    # Row 3: 5 circles (offset)
    y3 = y0 + 3*h
    centers[15] = [2*base, y3]
    centers[16] = [4*base, y3]
    centers[17] = [6*base, y3]
    centers[18] = [8*base, y3]
    centers[19] = [10*base, y3]
    
    # Row 4: 6 circles
    y4 = y0 + 4*h
    centers[20] = [base, y4]
    centers[21] = [2*base, y4]
    centers[22] = [3*base, y4]
    centers[23] = [4*base, y4]
    centers[24] = [5*base, y4]
    centers[25] = [6*base, y4]
    
    # Clip to unit square
    centers = np.clip(centers, 0.01, 0.99)
    
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
    
    # Iteratively enforce all constraints until convergence
    for iteration in range(200):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                if radii[i] + radii[j] > dists[i, j]:
                    if radii[i] > radii[j]:
                        new_r_i = dists[i, j] - radii[j]
                        if new_r_i < radii[i]:
                            radii[i] = new_r_i
                            changed = True
                    else:
                        new_r_j = dists[i, j] - radii[i]
                        if new_r_j < radii[j]:
                            radii[j] = new_r_j
                            changed = True
        
        if changed:
            radii = np.maximum(radii, 0)
    
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