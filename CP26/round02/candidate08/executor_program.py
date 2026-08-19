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
    # Initialize arrays for 26 circles
    n = 26
    centers = np.zeros((n, 2))

    # Corner-heavy strategy: place large circles in corners and along edges
    # This allows for larger individual radii
    
    # Place 4 large circles in corners
    # These can have radius up to ~0.2-0.25 if properly spaced
    centers[0] = [0.2, 0.2]  # Bottom-left
    centers[1] = [0.8, 0.2]  # Bottom-right
    centers[2] = [0.2, 0.8]  # Top-left
    centers[3] = [0.8, 0.8]  # Top-right
    
    # Place circles along each edge (between corners)
    # Bottom edge: 3 circles between corners
    centers[4] = [0.4, 0.2]
    centers[5] = [0.5, 0.2]
    centers[6] = [0.6, 0.2]
    
    # Top edge: 3 circles between corners
    centers[7] = [0.4, 0.8]
    centers[8] = [0.5, 0.8]
    centers[9] = [0.6, 0.8]
    
    # Left edge: 2 circles between corners
    centers[10] = [0.2, 0.4]
    centers[11] = [0.2, 0.6]
    
    # Right edge: 2 circles between corners
    centers[12] = [0.8, 0.4]
    centers[13] = [0.8, 0.6]
    
    # Fill the center with 6 circles
    # Arrange them in a 2x3 grid in the center region
    centers[14] = [0.35, 0.45]
    centers[15] = [0.45, 0.45]
    centers[16] = [0.55, 0.45]
    centers[17] = [0.35, 0.55]
    centers[18] = [0.45, 0.55]
    centers[19] = [0.55, 0.55]
    
    # Add 6 more circles to reach 26
    # Place them in the gaps between existing circles
    centers[20] = [0.5, 0.35]
    centers[21] = [0.5, 0.65]
    centers[22] = [0.35, 0.35]
    centers[23] = [0.65, 0.35]
    centers[24] = [0.35, 0.65]
    centers[25] = [0.65, 0.65]
    
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