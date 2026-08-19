# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Optimized Hexagonal Pattern"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.

    Strategy: Use an optimized hexagonal packing pattern with proper spacing.
    The hexagonal pattern is denser than square packing.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Optimized hexagonal packing for square container
    # Row spacing = sqrt(3) * r for optimal hexagonal packing
    # Adjusted for square boundaries
    
    # Row 0: 6 circles at optimized y position
    y_row0 = 0.14
    centers[0] = [0.05, y_row0]
    centers[1] = [0.25, y_row0]
    centers[2] = [0.45, y_row0]
    centers[3] = [0.65, y_row0]
    centers[4] = [0.85, y_row0]
    centers[5] = [0.95, y_row0]
    
    # Row 1: 6 circles, staggered by 0.15 horizontally
    y_row1 = y_row0 + 0.26
    centers[6] = [0.15, y_row1]
    centers[7] = [0.35, y_row1]
    centers[8] = [0.55, y_row1]
    centers[9] = [0.75, y_row1]
    centers[10] = [0.95, y_row1]
    centers[11] = [0.05, y_row1]
    
    # Row 2: 6 circles, aligned with row 0
    y_row2 = y_row1 + 0.26
    centers[12] = [0.05, y_row2]
    centers[13] = [0.25, y_row2]
    centers[14] = [0.45, y_row2]
    centers[15] = [0.65, y_row2]
    centers[16] = [0.85, y_row2]
    centers[17] = [0.95, y_row2]
    
    # Row 3: 4 circles, staggered
    y_row3 = y_row2 + 0.26
    centers[18] = [0.15, y_row3]
    centers[19] = [0.35, y_row3]
    centers[20] = [0.55, y_row3]
    centers[21] = [0.75, y_row3]
    
    # Fill remaining 4 circles in center gaps - repositioned
    centers[22] = [0.35, 0.35]
    centers[23] = [0.5, 0.35]
    centers[24] = [0.65, 0.35]
    centers[25] = [0.5, 0.5]
    
    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers)
    
    # Calculate the sum of radii
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii
    
    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers)
    
    # Calculate the sum of radii
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii
    
    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers)
    
    # Calculate the sum of radii
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii
    
    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers)
    
    # Calculate the sum of radii
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii
    
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
