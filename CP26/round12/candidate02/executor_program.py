# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - large center + small corners"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using Template 3: large center + small corners.
    
    This template:
    - Places a large circle at the center (0.5, 0.5)
    - Places 4 medium circles at the corners (0.3,0.3), (0.7,0.3), (0.3,0.7), (0.7,0.7)
    - Fills remaining 21 circles in a grid pattern
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Large center circle
    centers[0] = [0.5, 0.5]
    
    # 4 medium circles at corners
    medium_positions = [[0.3, 0.3], [0.7, 0.3], [0.3, 0.7], [0.7, 0.7]]
    for i, pos in enumerate(medium_positions):
        centers[1 + i] = pos
    
    # 21 small circles in a 5x5 grid, skipping the 6 already placed
    row_y = [0.1, 0.3, 0.5, 0.7, 0.9]
    col_x = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    idx = 6
    for y in row_y:
        for x in col_x:
            if idx >= n:
                break
            # Skip if this position is already taken
            if np.isclose(x, 0.3) and np.isclose(y, 0.3):
                continue
            if np.isclose(x, 0.7) and np.isclose(y, 0.3):
                continue
            if np.isclose(x, 0.3) and np.isclose(y, 0.7):
                continue
            if np.isclose(x, 0.7) and np.isclose(y, 0.7):
                continue
            if np.isclose(x, 0.5) and np.isclose(y, 0.5):
                continue
            
            centers[idx] = [x, y]
            idx += 1
    
    # Clip to ensure within bounds [0.01, 0.99]
    centers = np.clip(centers, 0.01, 0.99)
    
    # Compute maximum valid radii for this configuration
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