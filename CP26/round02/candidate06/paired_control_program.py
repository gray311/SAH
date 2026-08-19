# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - aggressive optimization"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.
    
    New strategy: Use a more aggressive packing with larger circles.
    Key insight: Allow circles to be larger by placing them more optimally.
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Strategy: Place circles to maximize their individual radii
    # Use a pattern that allows larger circles near boundaries
    
    # 4 corner circles - position them to be as large as possible
    # These can have radius ~0.1 (limited by corner)
    centers[0] = [0.1, 0.1]
    centers[1] = [0.9, 0.1]
    centers[2] = [0.1, 0.9]
    centers[3] = [0.9, 0.9]
    
    # 8 circles in a tighter inner ring
    # These can be medium-sized
    ring_radius = 0.18
    for i in range(8):
        angle = 2 * np.pi * i / 8
        centers[4 + i] = [0.5 + ring_radius * np.cos(angle), 0.5 + ring_radius * np.sin(angle)]
    
    # 14 circles in outer ring
    # These can be smaller but fill more space
    ring_radius2 = 0.38
    for i in range(14):
        angle = 2 * np.pi * i / 14
        centers[12 + i] = [0.5 + ring_radius2 * np.cos(angle), 0.5 + ring_radius2 * np.sin(angle)]
    
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
