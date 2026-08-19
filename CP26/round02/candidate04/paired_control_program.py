# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.
    
    Uses a sparse-inner, dense-outer strategy.
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Inner region: 3 circles (1 center + 2 close to center)
    centers[0] = [0.5, 0.5]
    centers[1] = [0.5 + 0.2, 0.5]
    centers[2] = [0.5 - 0.2, 0.5]
    
    # Middle ring: 8 circles
    r_mid = 0.3
    for i in range(8):
        angle = 2 * np.pi * i / 8
        centers[i + 3] = [0.5 + r_mid * np.cos(angle), 0.5 + r_mid * np.sin(angle)]
    
    # Outer ring: 15 circles spread around
    r_outer = 0.45
    for i in range(15):
        angle = 2 * np.pi * i / 15
        centers[i + 11] = [0.5 + r_outer * np.cos(angle), 0.5 + r_outer * np.sin(angle)]
    
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
    
    # Initialize radii based on distance to square borders
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Iteratively refine radii based on circle-circle constraints
    max_iterations = 50
    for iteration in range(max_iterations):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                
                # If circles would overlap, reduce both radii
                if radii[i] + radii[j] > dist:
                    scale = dist / (radii[i] + radii[j])
                    radii[i] *= scale
                    radii[j] *= scale
                    changed = True
        
        if not changed:
            break
    
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
