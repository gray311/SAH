# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - optimized"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.

    Uses a sparse grid pattern with compute_max_radii.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Place circles very sparsely to ensure compute_max_radii works
    # Using a 5x5 grid minus corners to get 26 positions
    
    # Row 0: 5 circles
    centers[0] = [0.1, 0.1]
    centers[1] = [0.3, 0.1]
    centers[2] = [0.5, 0.1]
    centers[3] = [0.7, 0.1]
    centers[4] = [0.9, 0.1]
    
    # Row 1: 5 circles
    centers[5] = [0.1, 0.3]
    centers[6] = [0.3, 0.3]
    centers[7] = [0.5, 0.3]
    centers[8] = [0.7, 0.3]
    centers[9] = [0.9, 0.3]
    
    # Row 2: 5 circles
    centers[10] = [0.1, 0.5]
    centers[11] = [0.3, 0.5]
    centers[12] = [0.5, 0.5]
    centers[13] = [0.7, 0.5]
    centers[14] = [0.9, 0.5]
    
    # Row 3: 5 circles
    centers[15] = [0.1, 0.7]
    centers[16] = [0.3, 0.7]
    centers[17] = [0.5, 0.7]
    centers[18] = [0.7, 0.7]
    centers[19] = [0.9, 0.7]
    
    # Row 4: 6 circles (one extra)
    centers[20] = [0.1, 0.9]
    centers[21] = [0.3, 0.9]
    centers[22] = [0.5, 0.9]
    centers[23] = [0.7, 0.9]
    centers[24] = [0.9, 0.9]
    centers[25] = [0.5, 0.5]  # Duplicate - let me fix
    
    # Actually I have 26 but one is duplicate. Let me redo:
    # 5+5+5+5+4 = 24, need 2 more
    # Let me use: 5+5+5+5+6 = 26 but that's 26 unique positions
    # Actually 5*5=25, so I need 26 unique positions
    
    centers = np.zeros((n, 2))
    idx = 0
    
    # 5x5 grid = 25 positions, plus 1 more
    for row in range(5):
        for col in range(5):
            x = 0.1 + col * 0.2
            y = 0.1 + row * 0.2
            centers[idx] = [x, y]
            idx += 1
    
    # Add one more circle in a gap
    centers[idx] = [0.55, 0.55]
    
    # Compute maximum valid radii
    radii = compute_max_radii(centers)
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
