# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii using hexagonal lattice.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_radii: Sum of all radii
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Hexagonal lattice-based packing
    # Start with a central circle and build hexagonal rings around it
    
    # Circle 0: Central circle
    centers[0] = [0.5, 0.5]
    
    # Build hexagonal rings with proper spacing
    # Ring 1: 6 circles, Ring 2: 12 circles, Ring 3: 7 circles
    
    # Ring 1: 6 circles at distance d1 from center
    d1 = 0.28
    for i in range(6):
        angle = 2 * np.pi * i / 6
        centers[i + 1] = [0.5 + d1 * np.cos(angle), 0.5 + d1 * np.sin(angle)]
    
    # Ring 2: 12 circles at distance d2 from center, staggered
    d2 = 0.50
    for i in range(12):
        # Staggered angles for hexagonal packing
        if i % 2 == 0:
            angle = 2 * np.pi * i / 12
        else:
            angle = 2 * np.pi * i / 12 + np.pi / 6
        centers[i + 7] = [0.5 + d2 * np.cos(angle), 0.5 + d2 * np.sin(angle)]
    
    # Ring 3: 7 circles in corners and edges
    corner_positions = [
        (0.12, 0.12), (0.88, 0.12), (0.12, 0.88), (0.88, 0.88),  # 4 corners
        (0.08, 0.5), (0.92, 0.5), (0.5, 0.08)  # 3 edge positions
    ]
    for i, (x, y) in enumerate(corner_positions):
        centers[i + 19] = [x, y]
    
    # Compute maximum valid radii
    radii = compute_max_radii(centers)
    
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position.
    
    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    
    # Start with border constraints
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # Iteratively reduce radii to avoid overlaps
    max_iterations = 200
    for _ in range(max_iterations):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                
                # If circles would overlap, reduce both
                if radii[i] + radii[j] > dist:
                    scale = dist / (radii[i] + radii[j])
                    radii[i] *= scale
                    radii[j] *= scale
                    changed = True
        
        if not changed:
            break
    
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