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
        sum_of_radii: Sum of all radii
    """
    # Initialize arrays for 26 circles
    n = 26
    centers = np.zeros((n, 2))

    # Strategy: Use a hexagonal-inspired layered packing
    # Layer 1: Place large circles at corners and edges
    # Layer 2: Fill gaps with smaller circles
    
    # Corner circles (4)
    # Large circles in corners
    centers[0] = [0.1, 0.1]
    centers[1] = [0.9, 0.1]
    centers[2] = [0.1, 0.9]
    centers[3] = [0.9, 0.9]
    
    # Edge circles along bottom and top (2 more to reach 6)
    centers[4] = [0.5, 0.05]
    centers[5] = [0.5, 0.95]
    
    # Edge circles along left and right (2 more to reach 8)
    centers[6] = [0.05, 0.5]
    centers[7] = [0.95, 0.5]
    
    # Center region - pack remaining 18 circles
    # Use hexagonal packing pattern in the center
    # Start with a large central circle
    centers[8] = [0.5, 0.5]
    
    # Hexagonal layer around center (6 circles)
    layer_radius = 0.18
    for i in range(1, 7):
        angle = 2 * np.pi * i / 6
        centers[8 + i] = [0.5 + layer_radius * np.cos(angle), 
                          0.5 + layer_radius * np.sin(angle)]
    
    # Second hexagonal layer (12 circles would be too many, use remaining)
    # We have 26 - 9 = 17 circles left
    # Place 10 more in a pattern around the first layer
    layer2_radius = 0.35
    # Place 10 circles in a modified pattern
    for i in range(10):
        angle = 2 * np.pi * i / 10
        centers[8 + 7 + i] = [0.5 + layer2_radius * np.cos(angle), 
                              0.5 + layer2_radius * np.sin(angle)]
    
    # Additional positioning adjustment to make sure all circles
    # are inside the square and don't overlap
    # Clip to ensure everything is inside the unit square
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