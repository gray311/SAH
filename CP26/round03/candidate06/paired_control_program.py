# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Three-layer hexagonal packing"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using a three-layer hexagonal packing pattern to maximize sum of radii.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_of_radii: Sum of all radii
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Strategy: Three-layer hexagonal packing
    # Layer 0: 1 center circle
    # Layer 1: 6 circles in hexagonal pattern
    # Layer 2: 19 circles in outer hexagonal pattern
    
    # Use hexagonal packing parameters
    # In hexagonal packing, circles in adjacent rows are offset by half the horizontal spacing
    # Vertical spacing = sqrt(3) * r, horizontal spacing = 2*r
    
    # Start with a base spacing that fits in the unit square
    base_spacing = 0.30
    
    # Layer 0: 1 center circle
    centers[0] = [0.5, 0.5]
    
    # Layer 1: 6 circles around center (hexagonal pattern)
    # These are placed at distance base_spacing from center
    for i in range(6):
        angle = i * np.pi / 3  # 60 degree spacing
        centers[i + 1] = [0.5 + base_spacing * np.cos(angle), 0.5 + base_spacing * np.sin(angle)]
    
    # Layer 2: 19 circles in outer layer
    # Use a larger spacing for the outer layer
    outer_spacing = 0.53
    for i in range(19):
        angle = i * 2 * np.pi / 19  # Equally spaced
        centers[i + 7] = [0.5 + outer_spacing * np.cos(angle), 0.5 + outer_spacing * np.sin(angle)]
    
    # Clip to ensure everything is inside the unit square
    centers = np.clip(centers, 0.05, 0.95)
    
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
    # Use a more efficient iterative approach
    for _ in range(10):  # Multiple passes for better convergence
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
