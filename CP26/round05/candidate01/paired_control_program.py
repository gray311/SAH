# EVOLVE-BLOCK-START
"""Hexagonal close-packing for n=26 circles - optimized ring placement"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.
    
    Uses a hexagonal packing pattern with optimized ring placement.
    """
    n = 26
    
    centers = np.zeros((n, 2))
    
    # Use a hexagonal ring-based approach with optimized positioning
    # Central circle
    centers[0] = [0.5, 0.5]
    
    # First ring: 8 circles at radius 0.3
    r1 = 0.3
    for i in range(8):
        angle = 2 * np.pi * i / 8
        x = 0.5 + r1 * np.cos(angle)
        y = 0.5 + r1 * np.sin(angle)
        # Clamp to valid range
        x = max(0.05, min(0.95, x))
        y = max(0.05, min(0.95, y))
        centers[1 + i] = [x, y]
    
    # Second ring: 16 circles at radius 0.58
    r2 = 0.58
    for i in range(16):
        angle = 2 * np.pi * i / 16
        x = 0.5 + r2 * np.cos(angle)
        y = 0.5 + r2 * np.sin(angle)
        # Clamp to valid range
        x = max(0.05, min(0.95, x))
        y = max(0.05, min(0.95, y))
        centers[9 + i] = [x, y]
    
    # Compute maximum valid radii
    radii = compute_max_radii(centers)
    
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.
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