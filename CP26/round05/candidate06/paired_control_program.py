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

    # Greedy placement strategy: place each circle to maximize available space
    # Start with a large central circle, then place others in gaps
    
    # Circle 0: Large central circle
    centers[0] = [0.5, 0.5]
    
    # Circle 1-6: Place in hexagonal pattern around center
    # Use larger radius positions for better coverage
    for i in range(6):
        angle = 2 * np.pi * i / 6
        # Position at distance 0.35 from center
        centers[i + 1] = [0.5 + 0.35 * np.cos(angle), 
                         0.5 + 0.35 * np.sin(angle)]
    
    # Circle 7-25: Place remaining 19 circles in optimized positions
    # Use positions that maximize distance from existing circles
    remaining = 19
    idx = 7
    
    # Try to place circles in a way that leaves room for large radii
    # Use a sparse grid pattern
    positions = []
    
    # Add corner positions
    for corner in [[0.1, 0.1], [0.9, 0.1], [0.1, 0.9], [0.9, 0.9]]:
        positions.append(corner)
    
    # Add mid-edge positions
    for pos in [[0.5, 0.05], [0.5, 0.95], [0.05, 0.5], [0.95, 0.5]]:
        positions.append(pos)
    
    # Add positions between corners
    for pos in [[0.3, 0.3], [0.7, 0.7], [0.7, 0.3], [0.3, 0.7]]:
        positions.append(pos)
    
    # Add more positions to fill remaining
    for pos in [[0.45, 0.45], [0.55, 0.55], [0.4, 0.6], [0.6, 0.4],
                [0.4, 0.4], [0.6, 0.6], [0.5, 0.3], [0.5, 0.7]]:
        positions.append(pos)
    
    # Add a few more for the remaining 19 - 12 = 7
    for pos in [[0.25, 0.25], [0.75, 0.75], [0.25, 0.75], [0.75, 0.25],
                [0.35, 0.35], [0.65, 0.65], [0.45, 0.55]]:
        positions.append(pos)
    
    for i, pos in enumerate(positions):
        if idx + i < n:
            centers[idx + i] = pos
    
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