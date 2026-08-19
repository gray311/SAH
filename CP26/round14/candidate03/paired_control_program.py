# EVOLVE-BLOCK-START
"""Multi-start greedy circle packing with local optimization for n=26 circles"""
import numpy as np


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Uses SINGLE-PASS constraint solver: scale only the larger radius
    when pairs overlap to avoid compounding losses.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    
    # Initialize radii from border distances only
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    
    # SINGLE-PASS: For each pair, if they overlap, scale ONLY the larger radius down
    # This avoids the compounding losses from scaling both radii
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            
            # If radii would cause overlap, scale the larger one
            if radii[i] + radii[j] > dist:
                # Scale only the larger radius
                # The new radius must be non-negative and at most dist - other_radius
                if radii[i] >= radii[j]:
                    new_radius_i = dist - radii[j]
                    radii[i] = max(0.001, new_radius_i)  # Ensure minimum positive radius
                else:
                    new_radius_j = dist - radii[i]
                    radii[j] = max(0.001, new_radius_j)  # Ensure minimum positive radius
    
    return radii


def optimize_centers(centers, max_iterations=80):
    """
    Local optimization: try small perturbations to improve the sum of radii.
    Uses multi-resolution optimization.
    """
    best_centers = centers.copy()
    best_score = compute_max_radii(best_centers).sum()
    
    # Multi-resolution optimization
    for step in [0.025, 0.012, 0.005]:
        for iteration in range(max_iterations):
            improved = False
            for i in range(len(centers)):
                for dx in [-step, 0, step]:
                    for dy in [-step, 0, step]:
                        if dx == 0 and dy == 0:
                            continue
                        new_centers = centers.copy()
                        new_centers[i] = [max(0.01, min(0.99, new_centers[i][0] + dx)),
                                          max(0.01, min(0.99, new_centers[i][1] + dy))]
                        new_score = compute_max_radii(new_centers).sum()
                        if new_score > best_score:
                            best_score = new_score
                            best_centers = new_centers.copy()
                            improved = True
            centers = best_centers
            if not improved:
                break
    
    return best_centers


def construct_packing():
    """
    Deterministic geometric circle packing for n=26 circles
    - Start with well-separated positions to ensure valid packing
    """
    n = 26
    
    # Start with a simple grid-like arrangement that's well-separated
    centers = np.zeros((n, 2))
    
    # Place circles in a roughly hexagonal pattern with good separation
    # Row 0: 4 circles
    centers[0] = [0.1, 0.1]
    centers[1] = [0.3, 0.1]
    centers[2] = [0.5, 0.1]
    centers[3] = [0.7, 0.1]
    centers[4] = [0.9, 0.1]
    
    # Row 1: 5 circles (staggered)
    centers[5] = [0.2, 0.3]
    centers[6] = [0.4, 0.3]
    centers[7] = [0.5, 0.3]
    centers[8] = [0.6, 0.3]
    centers[9] = [0.8, 0.3]
    
    # Row 2: 5 circles
    centers[10] = [0.15, 0.5]
    centers[11] = [0.35, 0.5]
    centers[12] = [0.5, 0.5]  # Center
    centers[13] = [0.65, 0.5]
    centers[14] = [0.85, 0.5]
    
    # Row 3: 5 circles
    centers[15] = [0.2, 0.7]
    centers[16] = [0.4, 0.7]
    centers[17] = [0.5, 0.7]
    centers[18] = [0.6, 0.7]
    centers[19] = [0.8, 0.7]
    
    # Row 4: 4 circles
    centers[20] = [0.1, 0.9]
    centers[21] = [0.3, 0.9]
    centers[22] = [0.5, 0.9]
    centers[23] = [0.7, 0.9]
    centers[24] = [0.9, 0.9]
    
    # 26th circle - add in a gap
    centers[25] = [0.55, 0.55]
    
    # Clip to ensure inside unit square
    centers = np.clip(centers, 0.001, 0.999)
    
    # Phase 2: Compute maximum valid radii using SINGLE-PASS solver
    radii = compute_max_radii(centers)
    
    # Ensure no negative radii
    radii = np.maximum(radii, 0.001)
    
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii
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