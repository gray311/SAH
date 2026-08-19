# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
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
    # Sophisticated hexagonal packing with optimized parameters
    # Based on densest packing in square container
    
    centers = np.zeros((26, 2))
    
    # Central circle
    centers[0] = [0.5, 0.5]
    
    # Ring 1: 6 circles - optimized distance
    r1 = 0.40
    for i in range(6):
        angle = 2 * np.pi * i / 6
        centers[i + 1] = [0.5 + r1 * np.cos(angle), 0.5 + r1 * np.sin(angle)]
    
    # Ring 2: 12 circles - optimized distance
    r2 = 0.70
    for i in range(12):
        angle = 2 * np.pi * i / 6 + np.pi / 6
        centers[i + 7] = [0.5 + r2 * np.cos(angle), 0.5 + r2 * np.sin(angle)]
    
    # Ring 3: 7 circles in corners and edges
    # Optimized corner positions
    centers[19] = [0.06, 0.06]
    centers[20] = [0.94, 0.06]
    centers[21] = [0.06, 0.94]
    centers[22] = [0.94, 0.94]
    
    # Edge circles
    centers[23] = [0.5, 0.09]
    centers[24] = [0.5, 0.91]
    centers[25] = [0.09, 0.5]
    # Total: 1 + 6 + 12 + 7 = 26 ✓
    
    # Clip to ensure all centers are within (0, 1)
    centers = np.clip(centers, 0.01, 0.99)

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
    n = len(centers)
    radii = np.zeros(n)
    
    # Initialize with edge constraints (larger initial radii)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x - 0.005, y - 0.005, 1 - x - 0.005, 1 - y - 0.005)
        radii[i] = max(radii[i], 0.001)
    
    # Iteratively refine radii based on circle-circle constraints
    for _ in range(200):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
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