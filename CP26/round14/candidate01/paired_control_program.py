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
    
    # For each pair, if they overlap, adjust both radii
    for iteration in range(50):  # Multiple passes
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                
                # If radii would cause overlap
                if radii[i] + radii[j] > dist:
                    # Reduce both radii proportionally
                    total = radii[i] + radii[j]
                    if total > 0:
                        scale = dist / total
                        radii[i] = radii[i] * scale
                        radii[j] = radii[j] * scale
        
        # Re-check border constraints
        for i in range(n):
            x, y = centers[i]
            border_radius = min(x, y, 1 - x, 1 - y)
            if radii[i] > border_radius:
                radii[i] = border_radius
    
    # Ensure minimum positive radius
    radii = np.maximum(radii, 0.001)
    
    return radii

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
    Multi-start greedy circle packing with local optimization for n=26 circles
    """
    n = 26
    
    best_centers = None
    best_sum_radii = 0
    
    # Try multiple random starts
    for start in range(10):
        centers = np.zeros((n, 2))
        
        # Greedy placement with more samples
        for i in range(n):
            best_pos = None
            best_radius = 0
            
            # Sample many positions
            for _ in range(300):
                # Random position
                x = np.random.uniform(0.01, 0.99)
                y = np.random.uniform(0.01, 0.99)
                
                radius = compute_radius_at_position(x, y, i, centers[:i])
                
                if radius > best_radius:
                    best_radius = radius
                    best_pos = (x, y)
            
            if best_pos is not None:
                centers[i] = best_pos
        
        # Compute maximum valid radii
        radii = compute_max_radii(centers)
        
        # Ensure no negative radii
        radii = np.maximum(radii, 0.001)
        
        sum_radii = np.sum(radii)
        
        if sum_radii > best_sum_radii:
            best_sum_radii = sum_radii
            best_centers = centers.copy()
    
    centers = best_centers
    
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