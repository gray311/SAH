# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.
    
    Uses a baseline-like 5x5 grid with one additional circle strategically placed.
    
    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_radii: Sum of all radii
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Start with a 5x5 grid (25 positions) - similar to baseline
    # Then add one more circle in a gap
    
    # 5x5 grid with spacing 0.2
    row_y = [0.1, 0.3, 0.5, 0.7, 0.9]
    col_x = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    idx = 0
    for y in row_y:
        for x in col_x:
            if idx >= n:
                break
            centers[idx] = [x, y]
            idx += 1
        if idx >= n:
            break
    
    # Add 26th circle in a gap - try multiple strategic locations
    # Place it at the center of the largest gap
    # Try placing it at (0.2, 0.4) - center of a 2x2 block of circles
    centers[25] = [0.2, 0.4]
    
    # Also try adding circles at multiple gap locations for better distribution
    # Actually, let's try placing the 26th circle at a different gap
    # Try (0.4, 0.4) - another gap location
    # centers[25] = [0.4, 0.4]
    # 
    # Or try (0.6, 0.6)
    # centers[25] = [0.6, 0.6]
    #
    # Or try placing it in a corner gap like (0.05, 0.05)
    # centers[25] = [0.05, 0.05]
    #
    # Let's try a different approach: place it at the edge of the grid
    # centers[25] = [0.95, 0.95]
    
    # Add 26th circle in a gap - try different strategic locations
    # The position (0.2, 0.4) worked well
    # Try (0.2, 0.4) again to confirm, or try other locations
    
    # Add 26th circle in a gap - try different strategic locations
    # Try placing at (0.4, 0.2) - symmetric to (0.2, 0.4)
    centers[25] = [0.4, 0.2]
    
    # Clip to ensure within bounds
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
    
    # Initialize radii to 1 (will be reduced based on constraints)
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