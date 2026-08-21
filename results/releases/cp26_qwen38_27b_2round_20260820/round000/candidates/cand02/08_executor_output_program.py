# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
    """
    n = 26
    centers = np.zeros((n, 2))

    # Hexagonal (triangular) lattice, rows of 3,4,5,5,4,5 (26 points).
    s = 0.175
    dy = s * np.sqrt(3.0) / 2.0
    row_counts = [3, 4, 5, 5, 4, 5]
    ys = [(r - (len(row_counts) - 1) / 2.0) * dy for r in range(len(row_counts))]
    pts = []
    for r, cnt in enumerate(row_counts):
        y = ys[r]
        offset = (r % 2) * 0.5
        for k in range(cnt):
            x = (k - (cnt - 1) / 2.0 + offset) * s
            pts.append([x, y])
    centers = np.array(pts[:n], dtype=float)

    # center the whole set in the square
    centers[:, 0] += 0.5 - centers[:, 0].mean()
    centers[:, 1] += 0.5 - centers[:, 1].mean()

    # Compute maximum valid radii (proven-valid method).
    radii = compute_max_radii(centers)
    best_sum = float(np.sum(radii))

    # ---- Fast local optimization over center positions ----
    # The LP gives the optimal radii for fixed centers; we now nudge centers
    # (keeping them strictly inside the square) and keep any move that raises
    # the LP objective. Deterministic, bounded, and fast.
    rng = np.random.RandomState(0)
    step = 0.010
    n = centers.shape[0]
    for it in range(3000):
        improved = False
        for i in range(n):
            x, y = centers[i]
            # candidate directions: toward square center + 4 random
            dirs = np.array([[0.5 - x, 0.5 - y]])
            dirs = np.vstack([dirs, rng.uniform(-1, 1, size=(4, 2))])
            for d in dirs:
                nd = np.hypot(d[0], d[1])
                if nd < 1e-9:
                    continue
                d = d / nd
                nx = x + step * d[0]
                ny = y + step * d[1]
                if nx < 0.02 or nx > 0.98 or ny < 0.02 or ny > 0.98:
                    continue
                trial = centers.copy()
                trial[i, 0] = nx
                trial[i, 1] = ny
                rt = compute_max_radii(trial)
                st = float(np.sum(rt))
                if st > best_sum + 1e-7:
                    centers = trial
                    best_sum = st
                    improved = True
                    break
        if not improved:
            step *= 0.9
            if step < 1e-4:
                break

    radii = compute_max_radii(centers)
    sum_radii = float(np.sum(radii))
    return centers, radii, sum_radii


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    This solves the LP:  max sum(r_i)  s.t.  0 <= r_i <= border_i
    and r_i + r_j <= d_ij for every pair. The LP optimum is the globally
    maximum sum of radii for fixed centers (the seed's greedy pairwise
    scaling is only a lossy approximation of this).
    """
    n = centers.shape[0]
    centers = np.asarray(centers, dtype=float)
    border = np.minimum(np.minimum(centers[:, 0], 1.0 - centers[:, 0]),
                        np.minimum(centers[:, 1], 1.0 - centers[:, 1]))
    border = np.maximum(border, 0.0)

    try:
        from scipy.optimize import linprog
    except Exception:
        # Fallback: the proven-valid greedy method (interior priority).
        radii = border.copy()
        idx = list(range(n))
        idx.sort(key=lambda i: -border[i])
        for a in idx:
            for b in idx:
                if b <= a:
                    continue
                dist = np.hypot(centers[a, 0] - centers[b, 0],
                                centers[a, 1] - centers[b, 1])
                if radii[a] + radii[b] > dist:
                    scale = dist / (radii[a] + radii[b])
                    radii[a] *= scale
                    radii[b] *= scale
        return radii

    # objective: minimize -sum(r)
    c = -np.ones(n)

    # inequality constraints: r_i + r_j <= d_ij  for all pairs
    A_rows = []
    b_rows = []
    for i in range(n):
        for j in range(i + 1, n):
            d = np.hypot(centers[i, 0] - centers[j, 0],
                         centers[i, 1] - centers[j, 1])
            row = np.zeros(n)
            row[i] = 1.0
            row[j] = 1.0
            A_rows.append(row)
            b_rows.append(d)
    A_ub = np.array(A_rows) if A_rows else None
    b_ub = np.array(b_rows) if b_rows else None

    # bounds: 0 <= r_i <= border_i
    bounds = [(0.0, border[i]) for i in range(n)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if res.status == 0 and res.x is not None:
        radii = np.maximum(res.x, 0.0)
    else:
        # Fallback if the LP failed.
        radii = border.copy()
        idx = list(range(n))
        idx.sort(key=lambda i: -border[i])
        for a in idx:
            for b in idx:
                if b <= a:
                    continue
                dist = np.hypot(centers[a, 0] - centers[b, 0],
                                centers[a, 1] - centers[b, 1])
                if radii[a] + radii[b] > dist:
                    scale = dist / (radii[a] + radii[b])
                    radii[a] *= scale
                    radii[b] *= scale

    # enforce strict feasibility (tiny epsilon below the LP bound)
    radii = np.maximum(radii, 0.0)
    for i in range(n):
        for j in range(i + 1, n):
            d = np.hypot(centers[i, 0] - centers[j, 0],
                         centers[i, 1] - centers[j, 1])
            if radii[i] + radii[j] > d - 1e-9:
                shrink = (d - 1e-9) / (radii[i] + radii[j])
                radii[i] *= shrink
                radii[j] *= shrink
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