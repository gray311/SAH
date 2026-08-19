# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - 5x5 with optimized variable radii"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.
    
    Uses a 5x5 grid (25 circles) with optimized variable radii and the 26th circle in center.
    """
    n = 26
    centers = np.zeros((n, 2))
    radii_initial = np.zeros(n)
    
    # 5x5 grid with spacing of 0.2 (from 0.1 to 0.9)
    row_y = [0.1, 0.3, 0.5, 0.7, 0.9]
    col_x = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    idx = 0
    for y in row_y:
        for x in col_x:
            if idx >= n:
                break
            centers[idx] = [x, y]
            # Assign radii based on position - corners get largest, center gets medium
            if x in [0.1, 0.9] and y in [0.1, 0.9]:
                radii_initial[idx] = 0.18  # corners - largest
            elif x in [0.1, 0.9] or y in [0.1, 0.9]:
                radii_initial[idx] = 0.13  # edges
            else:
                radii_initial[idx] = 0.09  # inner circles
            idx += 1
        if idx >= n:
            break
    
    # Add 26th circle in the center gap
    centers[25] = [0.5, 0.5]
    radii_initial[25] = 0.16  # center circle can be quite large
    
    # Clip to ensure within bounds [0.01, 0.99]
    centers = np.clip(centers, 0.01, 0.99)

    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers, radii_initial)

    # Calculate the sum of radii
    sum_radii = np.sum(radii)

    return centers, radii, sum_radii


def compute_max_radii(centers, radii_initial):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates
        radii_initial: initial radii estimates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    
    # Start with initial radii estimates
    radii = radii_initial.copy()

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        border_limit = min(x, y, 1 - x, 1 - y)
        radii[i] = min(radii[i], border_limit)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally based on their initial ratio
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