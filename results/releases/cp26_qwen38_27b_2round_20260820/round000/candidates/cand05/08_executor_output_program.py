# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.

    Strategy:
      1. Dense hexagonal lattice (6 cols x 5 rows = 30 positions, drop the
         4 corner circles to keep a dense 26-circle core).
      2. Water-filling radius optimization (exact, monotone, always valid).
      3. Mild center refinement (separate too-close pairs, keep in bounds).

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = _initial_hex_grid(n)
    centers = _refine_centers(centers)
    radii = _optimize_radii(centers)
    sum_radii = float(np.sum(radii))
    return centers, radii, sum_radii


def _initial_hex_grid(n):
    """Dense hexagonal (triangular) lattice, drop 4 corners to keep 26."""
    s = 0.185  # horizontal spacing (center-to-center)
    vy = s * np.sqrt(3) / 2
    cols = 6
    rows = 5
    pts = []
    for r in range(rows):
        for c in range(cols):
            x = 0.08 + c * s + (s / 2 if r % 2 else 0)
            y = 0.08 + r * vy
            pts.append([x, y])
    pts = np.array(pts)
    # Center the cluster in the square
    cx = (pts[:, 0].min() + pts[:, 0].max()) / 2
    cy = (pts[:, 1].min() + pts[:, 1].max()) / 2
    pts[:, 0] += 0.5 - cx
    pts[:, 1] += 0.5 - cy
    # Drop the 4 true corner circles (least valuable) to keep a dense 26-core
    if len(pts) > n:
        corners = [0, cols - 1, (rows - 1) * cols, rows * cols - 1]
        keep = [i for i in range(len(pts)) if i not in corners][:n]
        pts = pts[keep]
    return pts[:n]


def _refine_centers(centers):
    """Separate too-close pairs and keep all centers safely inside the square."""
    n = centers.shape[0]
    min_dist = 0.13
    for _ in range(300):
        moved = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                d = centers[i] - centers[j]
                dist = np.linalg.norm(d)
                if dist < min_dist and dist > 1e-9:
                    push = (min_dist - dist) / dist * 0.5
                    centers[i] += d * push
                    centers[j] -= d * push
                    moved += (min_dist - dist)
        # Keep in bounds with a small margin
        centers = np.clip(centers, 0.06, 0.94)
        if moved < 1e-8:
            break
    return centers


def _optimize_radii(centers):
    """
    Water-filling radius optimization (exact, monotone, always valid).

    Radii are r_i = lambda * u_i where u_i = min over all other centers j of
    dist(i, j), capped by the wall clearance of circle i. For a fixed lambda,
    all pair constraints r_i + r_j <= dist(i, j) hold iff
        lambda <= dist(i, j) / (u_i + u_j)   for every pair.
    So the optimal lambda is the minimum of that ratio over all pairs (and 1.0).
    This is the largest common scale factor that keeps the packing valid.
    """
    n = centers.shape[0]
    # u_i = min distance to any other center, capped by wall clearance
    u = np.empty(n)
    for i in range(n):
        dmin = 1e9
        for j in range(n):
            if i == j:
                continue
            d = np.linalg.norm(centers[i] - centers[j])
            if d < dmin:
                dmin = d
        wall = min(centers[i, 0], centers[i, 1], 1 - centers[i, 0], 1 - centers[i, 1])
        u[i] = min(dmin, wall)
    # Optimal common scale factor
    lam = 1.0
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(centers[i] - centers[j])
            denom = u[i] + u[j]
            if denom > 1e-12:
                cand = d / denom
                if cand < lam:
                    lam = cand
    radii = lam * u
    # Tiny safety margin to guard against floating-point overlap
    radii *= 0.999
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