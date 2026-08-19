# EVOLVE-BLOCK-START
def construct_packing():
    """Multi-start greedy circle packing with local optimization for n=26 circles"""
    import numpy as np

    def compute_radius_at_position(x, y, idx, existing_centers):
        radius = min(x, y, 1 - x, 1 - y)
        for j in range(len(existing_centers)):
            cx, cy = existing_centers[j]
            dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            radius = min(radius, dist / 2)
        return radius

    def compute_max_radii(centers):
        n = centers.shape[0]
        radii = np.zeros(n)
        for i in range(n):
            x, y = centers[i]
            radii[i] = min(x, y, 1 - x, 1 - y)
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                if radii[i] + radii[j] > dist:
                    if radii[i] >= radii[j]:
                        radii[i] = max(0.001, dist - radii[j])
                    else:
                        radii[j] = max(0.001, dist - radii[i])
        return radii

    def optimize_centers(centers, max_iterations=100):
        best_centers = centers.copy()
        best_score = compute_max_radii(best_centers).sum()
        for step in [0.025, 0.015, 0.008, 0.003]:
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

    n = 26
    best_centers = None
    best_sum_radii = 0

    for start in range(25):
        centers = np.zeros((n, 2))
        for i in range(n):
            best_pos = None
            best_radius = 0
            for _ in range(100):
                for gx in [0.1, 0.3, 0.5, 0.7, 0.9]:
                    for gy in [0.1, 0.3, 0.5, 0.7, 0.9]:
                        x = gx + np.random.uniform(-0.025, 0.025)
                        y = gy + np.random.uniform(-0.025, 0.025)
                        x = max(0.005, min(0.995, x))
                        y = max(0.005, min(0.995, y))
                        radius = compute_radius_at_position(x, y, i, centers[:i])
                        if radius > best_radius:
                            best_radius = radius
                            best_pos = (x, y)
            if best_pos is not None:
                centers[i] = best_pos
        centers = optimize_centers(centers, max_iterations=100)
        radii = compute_max_radii(centers)
        radii = np.maximum(radii, 0.001)
        sum_radii = np.sum(radii)
        if sum_radii > best_sum_radii:
            best_sum_radii = sum_radii
            best_centers = centers.copy()

    centers = best_centers
    centers = np.clip(centers, 0.001, 0.999)
    radii = compute_max_radii(centers)
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