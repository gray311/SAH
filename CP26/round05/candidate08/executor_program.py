# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using a more spread-out configuration for larger radii.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))
    
    idx = 0
    
    # Use a hexagonal lattice with optimal spacing
    # Place circles with distance ~1.0 apart to allow larger radii
    
    # Row 0: 5 circles
    row0_y = 0.15
    for i in range(5):
        x = 0.08 + i * 0.20
        centers[idx] = [x, row0_y]
        idx += 1
    
    # Row 1: 5 circles (staggered by half spacing)
    row1_y = 0.40
    for i in range(5):
        x = 0.14 + i * 0.20
        centers[idx] = [x, row1_y]
        idx += 1
    
    # Row 2: 5 circles
    row2_y = 0.65
    for i in range(5):
        x = 0.08 + i * 0.20
        centers[idx] = [x, row2_y]
        idx += 1
    
    # Row 3: 5 circles (staggered)
    row3_y = 0.90
    for i in range(5):
        x = 0.14 + i * 0.20
        centers[idx] = [x, row3_y]
        idx += 1
    
    # Total: 20 circles, need 6 more
    # Add 6 circles in strategic gaps
    gap_positions = [
        [0.16, 0.27], [0.28, 0.27],  # Between row 0-1
        [0.16, 0.52], [0.28, 0.52],  # Between row 1-2
        [0.16, 0.77], [0.28, 0.77],  # Between row 2-3
    ]
    for i, pos in enumerate(gap_positions):
        centers[idx] = pos
        idx += 1
    
    # Clip to ensure everything is inside bounds
    centers = np.clip(centers, 0.01, 0.99)

    # Compute maximum valid radii
    radii = compute_max_radii(centers)

    # Calculate sum of radii
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
    # Only scale the pair that overlaps, not all circles
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Only scale the larger radius down to avoid overlap
                # This preserves more total radius sum
                if radii[i] >= radii[j]:
                    radii[i] = dist - radii[j]
                else:
                    radii[j] = dist - radii[i]

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
