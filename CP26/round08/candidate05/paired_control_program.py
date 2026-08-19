# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using optimized hexagonal packing with corner placement.
    
    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Optimized multi-shell hexagonal packing
    # Shell 0: 1 center circle
    # Shell 1: 6 circles in hexagonal pattern
    # Shell 2: 12 circles in expanded hexagonal ring
    # Shell 3: 7 corner/edge circles
    # Total: 1 + 6 + 12 + 7 = 26
    
    # Center circle at exact center
    centers[0] = [0.5, 0.5]
    
    # Shell 1: 6 circles in hexagonal pattern around center
    # Distance from center optimized for density
    r1 = 0.28
    for i in range(6):
        angle = 2 * np.pi * i / 6
        centers[i + 1] = [0.5 + r1 * np.cos(angle), 0.5 + r1 * np.sin(angle)]
    
    # Shell 2: 12 circles in expanded hexagonal ring
    # More spread out to accommodate more circles
    r2 = 0.45
    for i in range(12):
        angle = 2 * np.pi * i / 12
        centers[i + 7] = [0.5 + r2 * np.cos(angle), 0.5 + r2 * np.sin(angle)]
    
    # Shell 3: 7 circles in corners and strategic edge positions
    # Corner circles (4) - keep positions that work well
    centers[19] = [0.08, 0.08]
    centers[20] = [0.92, 0.08]
    centers[21] = [0.08, 0.92]
    centers[22] = [0.92, 0.92]
    
    # Edge midpoints (2) - adjust for better spacing
    centers[23] = [0.5, 0.13]
    centers[24] = [0.5, 0.87]
    
    # One additional circle - adjust for better spacing
    centers[25] = [0.13, 0.5]
    
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