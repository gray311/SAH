# EVOLVE-BLOCK-START
"""Circle packing for n=26 circles - improved concentric approach"""
import numpy as np


def construct_packing():
    """
    Construct an improved concentric ring arrangement of 26 circles in a unit square.
    
    The original concentric ring approach achieved 0.364. We improve upon it by:
    1. Using better spacing in the rings
    2. Optimizing the radius computation
    
    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))

    # Place a large circle in the center
    centers[0] = [0.5, 0.5]

    # Place circles in rings with better spacing
    # Ring 1: 8 circles around the center
    # Ring 2: 16 circles around ring 1
    
    # Ring 1: 8 circles at radius 0.25 from center
    r1 = 0.25
    for i in range(8):
        angle = 2 * np.pi * i / 8
        centers[i + 1] = [0.5 + r1 * np.cos(angle), 0.5 + r1 * np.sin(angle)]

    # Ring 2: 16 circles at radius 0.5 from center
    r2 = 0.5
    for i in range(16):
        angle = 2 * np.pi * i / 16
        centers[i + 9] = [0.5 + r2 * np.cos(angle), 0.5 + r2 * np.sin(angle)]

    # Compute maximum valid radii for this configuration
    radii = compute_max_radii(centers)

    # Calculate the sum of radii
    sum_radii = np.sum(radii)

    return centers, radii, sum_radii


def compute_max_radii(centers):
    """
    Compute maximum radii for circle packing using a more sophisticated approach.
    
    Uses sequential maximum independent set-like relaxation to find better radii.
    """
    n = centers.shape[0]
    
    # Initialize radii based on distance to borders
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # Iterative refinement with more passes
    for iteration in range(200):
        for i in range(n):
            # Constraint from borders
            x, y = centers[i]
            border_limit = min(x, y, 1 - x, 1 - y)
            
            # Constraint from all other circles
            for j in range(n):
                if i == j:
                    continue
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                # The limiting factor for circle i given circle j's radius
                limit_from_j = dist - radii[j]
                if limit_from_j < border_limit:
                    border_limit = limit_from_j
            
            radii[i] = border_limit
    
    # Final pass: ensure all constraints are satisfied
    for _ in range(20):
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                if radii[i] + radii[j] > dist:
                    # Scale both to satisfy constraint
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