# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles (hexagonal brick + polish)."""
import numpy as np

N = 26


def _solve_radii(centers):
    """Feasible radii via wall-limit then sequential pair-scaling (robust)."""
    n = centers.shape[0]
    radii = np.empty(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    for _ in range(300):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                if radii[i] + radii[j] > dist:
                    scale = dist / (radii[i] + radii[j])
                    radii[i] *= scale
                    radii[j] *= scale
                    changed = True
        if not changed:
            break
    return radii


def _rows(counts, s, vs):
    n_rows = len(counts)
    ys = np.linspace(0.5 - (n_rows - 1) * vs / 2, 0.5 + (n_rows - 1) * vs / 2, n_rows)
    centers = []
    for k, y in enumerate(ys):
        cnt = counts[k]
        xs = 0.5 + (np.arange(cnt) - (cnt - 1) / 2) * s
        centers.extend([(x, y) for x in xs])
    return np.array(centers, dtype=float)


def _polish(c, steps=250, lr=0.012):
    """Nudge the tightest-contact pair apart; keep only improving moves."""
    c = c.copy().astype(float)
    best = float(np.sum(_solve_radii(c)))
    for _ in range(steps):
        r = _solve_radii(c)
        d = np.linalg.norm(c[:, None, :] - c[None, :, :], axis=2)
        over = r[None, :] + r[:, None] - d
        over = np.where(np.eye(c.shape[0]) < 0.5, over, -np.inf)
        i, j = np.unravel_index(int(np.argmax(over)), over.shape)
        diff = c[i] - c[j]
        norm = np.linalg.norm(diff)
        if norm < 1e-9:
            diff = np.array([1.0, 0.0]); norm = 1.0
        unit = diff / norm
        c[i] += unit * lr
        c[j] -= unit * lr
        if c[:, 0].min() < 1e-4 or c[:, 0].max() > 1 - 1e-4:
            c[i] -= unit * lr; c[j] += unit * lr
            continue
        if c[:, 1].min() < 1e-4 or c[:, 1].max() > 1 - 1e-4:
            c[i] -= unit * lr; c[j] += unit * lr
            continue
        s = float(np.sum(_solve_radii(c)))
        if s > best:
            best = s
        else:
            c[i] -= unit * lr
            c[j] += unit * lr
    return c, best


def construct_packing():
    best_c = None
    best_s = -1.0
    top = []  # list of (sum, centers)
    patterns = [
        [5, 5, 6, 5, 5],
        [5, 6, 5, 5, 5],
        [6, 5, 5, 5, 5],
        [4, 6, 6, 5, 5],
        [5, 5, 5, 6, 5],
        [5, 5, 5, 5, 6],
        [4, 5, 6, 5, 6],
        [5, 4, 6, 6, 5],
        [7, 6, 6, 7],
        [6, 7, 6, 7],
        [7, 7, 6, 6],
        [4, 5, 5, 5, 4, 3],
        [3, 5, 5, 5, 5, 3],
        [5, 4, 5, 4, 5, 3],
    ]
    for counts in patterns:
        if sum(counts) != 26:
            continue
        n_rows = len(counts)
        s_lo = 0.155
        s_hi = 0.225
        vs_lo = 0.130 if n_rows >= 6 else 0.155
        vs_hi = 0.225
        for s in np.linspace(s_lo, s_hi, 7):
            for vs in np.linspace(vs_lo, vs_hi, 7):
                c = _rows(counts, s, vs)
                if c[:, 0].min() < 1e-4 or c[:, 0].max() > 1 - 1e-4:
                    continue
                if c[:, 1].min() < 1e-4 or c[:, 1].max() > 1 - 1e-4:
                    continue
                r = _solve_radii(c)
                ssum = float(np.sum(r))
                if ssum > best_s:
                    best_s = ssum
                    best_c = c
                top.append((ssum, c))
    # polish top-3 layouts, keep the best
    top.sort(key=lambda t: -t[0])
    final_c = best_c
    final_s = best_s
    for ssum0, c0 in top[:3]:
        cp, sp = _polish(c0, steps=250, lr=0.012)
        if sp > final_s:
            final_s = sp
            final_c = cp
    radii = _solve_radii(final_c)
    return final_c, radii, float(np.sum(radii))
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