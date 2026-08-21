# EVOLVE-BLOCK-START
"""Hex-lattice circle packing constructor for n=26 circles"""
import numpy as np


def _compute_radii(centers):
    """Compute valid radii for given centers using iterative relaxation.
    Start with border-limited radii, then repeatedly reduce any circle whose
    pair sum exceeds distance, distributing the reduction. Iterate until stable
    or max iterations."""
    n = centers.shape[0]
    radii = np.array([min(x, y, 1.0 - x, 1.0 - y)
                      for x, y in centers])
    radii = np.maximum(radii, 0.0)

    # Precompute distances
    d = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d[i, j] = d[j, i] = np.hypot(centers[i, 0] - centers[j, 0],
                                         centers[i, 1] - centers[j, 1])

    # Iterative: for each overlapping pair, reduce the smaller-radius one
    # (or split) so r_i + r_j <= d_ij.
    for _ in range(40):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                s = radii[i] + radii[j]
                if s > d[i, j] + 1e-12:
                    excess = s - d[i, j]
                    # Reduce proportionally to current radii (smaller gets more cut)
                    if s > 0:
                        cut_i = excess * (radii[i] / s)
                        cut_j = excess * (radii[j] / s)
                    else:
                        cut_i = excess / 2
                        cut_j = excess / 2
                    radii[i] = max(0.0, radii[i] - cut_i)
                    radii[j] = max(0.0, radii[j] - cut_j)
                    changed = True
        if not changed:
            break
    return radii


def _make_grid_layout():
    """Dense 4-column layout: 4 full rows of 4 (16 circles) plus 2 extra rows
    of 5 each (10 circles) = 26. Spaced as a near-square grid so circles are
    close together and radii can be large."""
    centers = []
    # 6 rows: counts 5,4,4,4,4,5 -> 26
    row_counts = [5, 4, 4, 4, 4, 5]
    total = sum(row_counts)
    assert total == 26

    # Horizontal spacing: for a row of 5, centers at x = 0.5 + k*gx
    # For rows of 4, offset by half spacing to interleave.
    gx = 1.0 / 5.0  # spacing for 5-wide rows: centers at 0,0.2,0.4,0.6,0.8
    gy = 1.0 / 6.0  # vertical spacing for 6 rows

    for r, cnt in enumerate(row_counts):
        y = gy * (r + 0.5)
        if cnt == 5:
            for k in range(5):
                x = gx * (k + 0.5)
                centers.append([x, y])
        else:
            # 4 circles, offset to sit between the 5-wide row gaps
            for k in range(4):
                x = gx * (k + 1.0)
                centers.append([x, y])
    centers = np.array(centers, dtype=float)
    return centers


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.

    Returns:
        Tuple of (centers, radii, sum_of_radii)
        centers: np.array of shape (26, 2) with (x, y) coordinates
        radii: np.array of shape (26) with radius of each circle
        sum_of_radii: Sum of all radii
    """
    centers = _make_grid_layout()
    radii = _compute_radii(centers)
    best_sum = float(np.sum(radii))
    best_centers = centers.copy()

    # Bounded deterministic local relaxation: nudge each center along the
    # direction that increases its minimum slack (to border and to nearest
    # neighbors), recompute radii, keep only if the sum increases.
    def _min_slack(c, r):
        # slack_i = min(border_i - r_i, min_j (d_ij - r_i - r_j))
        n = c.shape[0]
        slacks = []
        for i in range(n):
            b = min(c[i, 0], c[i, 1], 1 - c[i, 0], 1 - c[i, 1])
            s = b - r[i]
            for j in range(n):
                if i != j:
                    d = np.hypot(c[i, 0] - c[j, 0], c[i, 1] - c[j, 1])
                    s = min(s, d - r[i] - r[j])
            slacks.append(s)
        return np.array(slacks)

    step = 0.03
    for _sweep in range(12):
        improved = False
        r = _compute_radii(centers)
        base_sum = float(np.sum(r))
        for i in range(26):
            for dx, dy in [(step, 0), (-step, 0), (0, step), (0, -step),
                           (step, step), (-step, -step), (step, -step), (-step, step)]:
                nx = centers[i, 0] + dx
                ny = centers[i, 1] + dy
                if nx < 1e-6 or nx > 1 - 1e-6:
                    continue
                if ny < 1e-6 or ny > 1 - 1e-6:
                    continue
                # Only modify this center
                centers[i, 0] = nx
                centers[i, 1] = ny
                tr = _compute_radii(centers)
                ts = float(np.sum(tr))
                if ts > base_sum + 1e-9:
                    base_sum = ts
                    improved = True
                else:
                    centers[i, 0] -= dx
                    centers[i, 1] -= dy
        if base_sum > best_sum:
            best_sum = base_sum
            best_centers = centers.copy()
        if not improved:
            break

    centers = best_centers
    radii = _compute_radii(centers)
    sum_radii = float(np.sum(radii))
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