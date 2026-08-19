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
                if radii[i] >= radii[j]:
                    new_radius_i = dist - radii[j]
                    radii[i] = max(0.001, new_radius_i)
                else:
                    new_radius_j = dist - radii[i]
                    radii[j] = max(0.001, new_radius_j)
    
    return radii


def optimize_centers(centers, max_iterations=50):
    """
    Local optimization: try small perturbations to improve the sum of radii.
    """
    best_centers = centers.copy()
    best_score = compute_max_radii(best_centers).sum()
    
    for iteration in range(max_iterations):
        improved = False
        for i in range(len(centers)):
            for dx in [-0.01, 0, 0.01]:
                for dy in [-0.01, 0, 0.01]:
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
    
    return centers


def construct_packing():
    """
    Construct an optimized arrangement of 26 circles in a unit square
    that maximizes the sum of their radii.
    
    Uses multi-start greedy placement with local optimization.
    """
    n = 26
    
    # Try multiple random configurations
    best_centers = None
    best_sum_radii = 0
    
    for start in range(20):
        centers = np.zeros((n, 2))
        
        # Greedy placement with focused sampling
        for i in range(n):
            best_pos = None
            best_radius = 0
            
            # Focused sampling - targeting better regions
            for _ in range(200):
                # More balanced sampling
                if np.random.random() < 0.25:
                    # Center region
                    x = 0.5 + np.random.uniform(-0.12, 0.12)
                    y = 0.5 + np.random.uniform(-0.12, 0.12)
                elif np.random.random() < 0.5:
                    # Edge regions with more spread
                    edge = np.random.randint(0, 4)
                    if edge == 0:  # Bottom
                        x = np.random.uniform(0.15, 0.85)
                        y = np.random.uniform(0.01, 0.08)
                    elif edge == 1:  # Top
                        x = np.random.uniform(0.15, 0.85)
                        y = np.random.uniform(0.92, 0.99)
                    elif edge == 2:  # Left
                        x = np.random.uniform(0.01, 0.08)
                        y = np.random.uniform(0.15, 0.85)
                    else:  # Right
                        x = np.random.uniform(0.92, 0.99)
                        y = np.random.uniform(0.15, 0.85)
                else:
                    # Random anywhere
                    x = np.random.uniform(0.01, 0.99)
                    y = np.random.uniform(0.01, 0.99)
                
                radius = compute_radius_at_position(x, y, i, centers[:i])
                
                if radius > best_radius:
                    best_radius = radius
                    best_pos = (x, y)
            
            if best_pos is not None:
                centers[i] = best_pos
        
        # Apply local optimization with more iterations
        centers = optimize_centers(centers, max_iterations=35)
        
        # Compute sum of radii for this configuration
        radii = compute_max_radii(centers)
        radii = np.maximum(radii, 0.001)
        sum_radii = np.sum(radii)
        
        if sum_radii > best_sum_radii:
            best_sum_radii = sum_radii
            best_centers = centers.copy()
    
    # Use the best configuration
    centers = best_centers
    
    # Clip to ensure inside unit square
    centers = np.clip(centers, 0.001, 0.999)
    
    # Compute maximum valid radii
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