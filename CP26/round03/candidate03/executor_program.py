# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles - Better Radii"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    using hexagonal packing with optimized radii computation.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_of_radii: Sum of all radii
    """
    n = 26
    centers = np.zeros((n, 2))
    
    # Hexagonal packing with moderate spacing
    # Layer 0: 1 center
    centers[0] = [0.5, 0.5]
    
    # Layer 1: 6 circles
    layer1_dist = 0.20
    for i in range(6):
        angle = np.pi / 3 * i
        centers[i + 1] = [0.5 + layer1_dist * np.cos(angle), 0.5 + layer1_dist * np.sin(angle)]
    
    # Layer 2: 12 circles
    layer2_dist = 0.38
    for i in range(12):
        if i % 2 == 0:
            angle = np.pi / 3 * (i // 2)
        else:
            angle = np.pi / 3 * (i // 2) + np.pi / 6
        centers[i + 7] = [0.5 + layer2_dist * np.cos(angle), 0.5 + layer2_dist * np.sin(angle)]
    
    # Layer 3: 7 circles
    layer3_dist = 0.56
    for i in range(7):
        angle = 2 * np.pi * i / 7
        centers[i + 19] = [0.5 + layer3_dist * np.cos(angle), 0.5 + layer3_dist * np.sin(angle)]
    
    # Ensure all centers are within bounds
    centers = np.clip(centers, 0.01, 0.99)
    
    # Compute maximum valid radii with better algorithm
    radii = compute_better_radii(centers)
    
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


def compute_better_radii(centers):
    """
    Compute radii using a more sophisticated approach.
    """
    n = centers.shape[0]
    radii = np.ones(n) * 0.1  # Start with small radii
    
    # Step 1: Set initial radii based on distance to square borders
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(radii[i], x, y, 1 - x, 1 - y)
    
    # Step 2: Iteratively refine based on pairwise constraints
    # Use more passes for better convergence
    for iteration in range(200):
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                
                if radii[i] + radii[j] > dist:
                    # Scale down proportionally
                    new_sum = dist
                    old_sum = radii[i] + radii[j]
                    radii[i] = radii[i] * new_sum / old_sum
                    radii[j] = radii[j] * new_sum / old_sum
        
        # Re-apply border constraints
        for i in range(n):
            x, y = centers[i]
            radii[i] = min(radii[i], x, y, 1 - x, 1 - y)
    
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