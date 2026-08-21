# EVOLVE-BLOCK-START
import numpy as np
from scipy.optimize import linprog


def _radii_lp(centers):
    n = len(centers)
    c = -np.ones(n)
    A_rows = []
    b_vals = []
    for i in range(n):
        for j in range(i + 1, n):
            d = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            row = np.zeros(n)
            row[i] = 1
            row[j] = 1
            A_rows.append(row)
            b_vals.append(d)
    for i in range(n):
        x, y = centers[i]
        b_dist = min(x, y, 1 - x, 1 - y)
        row = np.zeros(n)
        row[i] = 1
        A_rows.append(row)
        b_vals.append(b_dist)
    A = np.array(A_rows)
    b = np.array(b_vals)
    bounds = [(0, None)] * n
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    if result.success:
        return np.maximum(result.x, 0)
    return _radii_fallback(centers)


def _radii_fallback(centers):
    n = len(centers)
    radii = np.array([min(x, y, 1 - x, 1 - y) for x, y in centers])
    for _ in range(300):
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                s = radii[i] + radii[j]
                if s > dist and s > 0:
                    scale = dist / s
                    radii[i] *= scale
                    radii[j] *= scale
    return radii


def _grid55_plus1():
    pts = []
    for i in range(5):
        for j in range(5):
            pts.append([0.1 + i * 0.2, 0.1 + j * 0.2])
    pts.append([0.5, 0.5])
    return np.array(pts)


def _rows(config):
    n = sum(config)
    n_rows = len(config)
    dy = 1.0 / (n_rows + 1)
    centers = np.zeros((n, 2))
    idx = 0
    for r in range(n_rows):
        k = config[r]
        y = dy * (r + 1)
        if k > 1:
            xs = np.linspace(0.1, 0.9, k)
        else:
            xs = np.array([0.5])
        for x in xs:
            centers[idx] = [x, y]
            idx += 1
    return centers


def _hex_select(s):
    dy = s * np.sqrt(3) / 2
    pts = []
    row = 0
    y = 0.03
    while y <= 0.97:
        x_offset = (s / 2) if (row % 2 == 1) else 0
        x = 0.03 + x_offset
        while x <= 0.97:
            pts.append([x, y])
            x += s
        y += dy
        row += 1
    pts = np.array(pts)
    dists = np.sqrt((pts[:, 0] - 0.5) ** 2 + (pts[:, 1] - 0.5) ** 2)
    idx = np.argsort(dists)
    return pts[idx[:26]].copy()


def _smooth_grad(centers, r):
    n = len(centers)
    d = np.linalg.norm(centers[:, None, :] - centers[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    nb = d - r[None, :]
    arg = np.argmin(nb, axis=1)
    best = nb[np.arange(n), arg]
    wall = np.minimum(np.minimum(centers[:, 0], centers[:, 1]),
                      np.minimum(1 - centers[:, 0], 1 - centers[:, 1]))
    use_wall = wall < best
    grad = np.zeros((n, 2))
    widx = np.where(use_wall)[0]
    for i in widx:
        x, y = centers[i]
        g = np.zeros(2)
        if x == wall[i]:
            g[0] = 1.0
        elif (1 - x) == wall[i]:
            g[0] = -1.0
        if y == wall[i]:
            g[1] = 1.0
        elif (1 - y) == wall[i]:
            g[1] = -1.0
        grad[i] += g
    nidx = np.where(~use_wall)[0]
    for i in nidx:
        j = arg[i]
        dd = d[i, j]
        if dd > 1e-9:
            u = (centers[i] - centers[j]) / dd
            grad[i] += u
            grad[j] -= u
    return grad


def _gradient_optimize(centers, steps, lr):
    c = centers.copy()
    r = _radii_lp(c)
    for t in range(steps):
        grad = _smooth_grad(c, r)
        c = c + lr * grad
        c = np.clip(c, 0.02, 0.98)
        if (t + 1) % 15 == 0:
            r = _radii_lp(c)
    return c


def _refine(c, schedule):
    for steps, lr in schedule:
        c = _gradient_optimize(c, steps, lr)
    return c


def construct_packing():
    rng = np.random.default_rng(0)
    starts = [
        _grid55_plus1(),
        _rows([5, 5, 5, 5, 5, 1]),
        _hex_select(0.18),
        _hex_select(0.19),
        _hex_select(0.20),
        _hex_select(0.21),
        _hex_select(0.22),
    ]
    best = None
    best_sum = -1.0
    best_radii = None
    for cand in starts:
        radii = _radii_lp(cand)
        s = float(np.sum(radii))
        if s > best_sum:
            best_sum, best, best_radii = s, cand.copy(), radii
        for steps, lr in [(400, 0.006), (400, 0.003)]:
            opt = _gradient_optimize(cand, steps, lr)
            radii = _radii_lp(opt)
            s = float(np.sum(radii))
            if s > best_sum:
                best_sum, best, best_radii = s, opt.copy(), radii
    best = _refine(best, [(300, 0.003), (300, 0.0015), (400, 0.0008), (400, 0.0005)])
    radii = _radii_lp(best)
    best_sum = float(np.sum(radii))
    best_radii = radii
    scales = [0.02, 0.015, 0.01, 0.02, 0.015, 0.01, 0.025, 0.012, 0.008, 0.02]
    for k in range(10):
        pert = best + rng.normal(0, scales[k], best.shape)
        pert = np.clip(pert, 0.02, 0.98)
        cand = _refine(pert, [(200, 0.003), (300, 0.001), (300, 0.0005)])
        radii = _radii_lp(cand)
        s = float(np.sum(radii))
        if s > best_sum:
            best_sum, best, best_radii = s, cand.copy(), radii
    return best, best_radii, best_sum
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