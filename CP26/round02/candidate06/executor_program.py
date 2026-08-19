# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Centered hexagonal pattern"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii using centered hexagonal packing.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_of_radii: Sum of all radii
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Use a centered hexagonal lattice pattern
    # Start with a larger radius and let the optimizer adjust
    
    # For n=26, a good pattern is:
    # Layer 0: 1 circle at center
    # Layer 1: 6 circles
    # Layer 2: 12 circles
    # Layer 3: 7 circles
    # Total: 26
    
    # Estimate radius for this pattern
    # The outermost layer should be within the square with margin
    # For hexagonal packing, the diameter is roughly: 2r + 2*sqrt(3)*r + 3*r ≈ 8.46r
    # So r ≈ 0.118 for tight packing, but we need margin
    
    r = 0.10
    
    # Layer 0: 1 circle at center
    centers[0] = [0.5, 0.5]
    
    # Layer 1: 6 circles at distance 2r from center
    for i in range(6):
        angle = 2 * np.pi * i / 6
        centers[i + 1] = [0.5 + 2 * r * np.cos(angle), 0.5 + 2 * r * np.sin(angle)]
    
    # Layer 2: 12 circles
    # 6 circles at distance 4r (same angles as layer 1)
    for i in range(6):
        angle = 2 * np.pi * i / 6
        centers[i + 7] = [0.5 + 4 * r * np.cos(angle), 0.5 + 4 * r * np.sin(angle)]
    
    # 6 circles at distance 4r but offset by 30°
    for i in range(6):
        angle = 2 * np.pi * (i + 0.5) / 6
        centers[i + 13] = [0.5 + 4 * r * np.cos(angle), 0.5 + 4 * r * np.sin(angle)]
    
    # Layer 3: 7 circles
    # Place them in a ring at larger radius
    r_outer = 0.55
    for i in range(7):
        angle = 2 * np.pi * i / 7
        centers[i + 19] = [0.5 + r_outer * np.cos(angle), 0.5 + r_outer * np.sin(angle)]
    
    # Clip to ensure all centers are within the unit square with margin
    centers = np.clip(centers, 0.01, 0.99)
    
    # Now compute maximum valid radii
    radii = compute_max_radii(centers)
    
    # Ensure no zero or negative radii
    radii = np.maximum(radii, 0.001)
    
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