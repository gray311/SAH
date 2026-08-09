# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Optimized with More Iterations"""
import numpy as np


def construct_packing():
    """
    Construct a 26-circle packing using an optimized hexagonal grid pattern.
    Uses 6 rows with r_base=0.11 and more robust radius optimization.
    
    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Use base radius from previous best configuration
    r_base = 0.11
    row_height = r_base * np.sqrt(3)  # ≈ 0.1905
    
    # Pattern: 4 + 5 + 5 + 5 + 5 + 2 = 26 circles
    
    # Row 0: 4 circles (bottom)
    for i in range(4):
        x = 0.14 + i * 0.20
        y = r_base
        centers[i] = [x, y]
    
    # Row 1: 5 circles (shifted)
    for i in range(5):
        x = 0.12 + i * 0.20
        y = r_base + row_height
        centers[i + 4] = [x, y]
    
    # Row 2: 5 circles
    for i in range(5):
        x = 0.14 + i * 0.20
        y = r_base + 2 * row_height
        centers[i + 9] = [x, y]
    
    # Row 3: 5 circles
    for i in range(5):
        x = 0.12 + i * 0.20
        y = r_base + 3 * row_height
        centers[i + 14] = [x, y]
    
    # Row 4: 5 circles
    for i in range(5):
        x = 0.14 + i * 0.20
        y = r_base + 4 * row_height
        centers[i + 19] = [x, y]
    
    # Row 5: 2 circles (top)
    for i in range(2):
        x = 0.4 + i * 0.3
        y = r_base + 5 * row_height
        centers[i + 24] = [x, y]
    
    # Ensure all circles are within the unit square
    centers = np.clip(centers, 0.001, 0.999)
    
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
    
    # Initialize radii based on distance to borders (favor corners and edges)
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # Iteratively refine radii based on circle-circle constraints
    for iteration in range(10):
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                
                # If circles would overlap, reduce the larger radius more
                if radii[i] + radii[j] > dist:
                    # Reduce both, but prioritize the smaller one
                    if radii[i] < radii[j]:
                        radii[j] = max(radii[j] - (radii[i] + radii[j] - dist), 0.001)
                    else:
                        radii[i] = max(radii[i] - (radii[i] + radii[j] - dist), 0.001)
    
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