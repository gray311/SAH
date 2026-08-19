# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Grid pattern"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using grid pattern to maximize sum of radii.
    
    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_of_radii: Sum of all radii
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Grid pattern: 5 rows x 6 columns = 30, but we need 26
    # Let's do 4 rows x 7 = 28, or 5 rows x 5 = 25 + 1 extra
    # Or: 5 rows with 6, 5, 5, 5, 4 = 25, need 1 more
    
    # Try: 5 rows with 6, 5, 5, 5, 5 = 26 circles
    # Grid spacing: if r ~ 0.1, horizontal spacing ~ 0.2, vertical spacing ~ 0.2
    
    # 5 rows at y = 0.05, 0.25, 0.45, 0.65, 0.85
    # Row counts: 6, 5, 5, 5, 5 = 26
    
    y_positions = [0.05, 0.25, 0.45, 0.65, 0.85]
    row_counts = [6, 5, 5, 5, 5]
    
    idx = 0
    for row_idx, (y, count) in enumerate(zip(y_positions, row_counts)):
        # For odd rows, shift by 0.1
        shift = 0.1 if row_idx % 2 == 1 else 0
        
        # Distribute evenly
        x_start = shift
        x_end = 1 - shift
        span = x_end - x_start
        spacing = span / (count - 1) if count > 1 else 0.5
        
        for j in range(count):
            x = x_start + j * spacing
            centers[idx] = [x, y]
            idx += 1
    
    # Compute maximum valid radii
    radii = compute_max_radii(centers)
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
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
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