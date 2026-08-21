# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 (L-BFGS + Nelder-Mead)"""
import time
import numpy as np
from scipy.optimize import linprog, minimize


def _solve_radii(centers):
    """Maximize sum of radii for fixed centers via LP (robust, exact)."""
    centers = np.asarray(centers, dtype=float)
    n = len(centers)
    c = -np.ones(n)
    A_rows = []
    b_vals = []
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.hypot(centers[i, 0] - centers[j, 0],
                               centers[i, 1] - centers[j, 1]))
            row = np.zeros(n)
            row[i] = 1
            row[j] = 1
            A_rows.append(row)
            b_vals.append(d)
    for i in range(n):
        x, y = centers[i]
        row = np.zeros(n)
        row[i] = 1
        A_rows.append(row)
        b_vals.append(min(x, y, 1.0 - x, 1.0 - y))
    A = np.array(A_rows)
    b = np.array(b_vals)
    bounds = [(0, None)] * n
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    if result.success:
        return np.maximum(result.x, 0.0)
    r = np.array([min(x, y, 1.0 - x, 1.0 - y) for x, y in centers])
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.hypot(centers[i, 0] - centers[j, 0],
                               centers[i, 1] - centers[j, 1]))
            D[i, j] = D[j, i] = d
    for _ in range(3000):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                s = r[i] + r[j]
                d = D[i, j]
                if s > d + 1e-12:
                    if s <= 0:
                        r[i] = r[j] = 0.0
                        continue
                    t = d / s
                    r[i] *= t
                    r[j] *= t
                    changed = True
        if not changed:
            break
    return r


def _hex_centers(spacing):
    dy = spacing * np.sqrt(3) / 2
    pts = []
    row = 0
    y = spacing
    while y <= 1.0 - spacing:
        x_offset = (spacing / 2) if (row % 2 == 1) else 0.0
        x = spacing + x_offset
        while x <= 1.0 - spacing:
            pts.append([x, y])
            x += spacing
        y += dy
        row += 1
    pts = np.array(pts)
    if len(pts) < 26:
        return None
    dists = np.sqrt((pts[:, 0] - 0.5) ** 2 + (pts[:, 1] - 0.5) ** 2)
    idx = np.argsort(dists)
    return pts[idx[:26]].copy()


def _lp_objective(x):
    # Nelder-Mead has no bounds; add a soft wall penalty.
    c = np.clip(x, 0.0, 1.0).reshape(26, 2)
    pen = 0.0
    for i in range(26):
        for axis in range(2):
            v = c[i, axis]
            if v < 0.02:
                pen += 5.0 * (0.02 - v) ** 2
            if v > 0.98:
                pen += 5.0 * (v - 0.98) ** 2
    return -float(np.sum(_solve_radii(c))) + pen


def _lbfgs_objective(x):
    return -float(np.sum(_solve_radii(x.reshape(26, 2))))


def construct_packing():
    n = 26
    t0 = time.time()
    deadline = t0 + 40.0

    inits = []
    for sp in [0.17, 0.19]:
        c = _hex_centers(sp)
        if c is not None:
            inits.append(c)
    gg = [0.13, 0.28, 0.5, 0.72, 0.87]
    cb = []
    for x in gg:
        for y in gg:
            if abs(x - 0.5) < 1e-9 and abs(y - 0.5) < 1e-9:
                continue
            cb.append([x, y])
    cb.append([0.5, 0.205])
    cb.append([0.5, 0.795])
    inits.append(np.array(cb)[:26])

    best_centers = None
    best_sum = -1.0
    # Phase A: L-BFGS
    for init in inits:
        if time.time() > deadline - 12.0:
            break
        result = minimize(
            _lbfgs_objective, init.flatten(), method='L-BFGS-B',
            bounds=[(0.02, 0.98)] * 52,
            options={'maxiter': 60, 'ftol': 1e-9}
        )
        opt_centers = np.clip(result.x, 0.02, 0.98).reshape(26, 2)
        s = float(np.sum(_solve_radii(opt_centers)))
        if s > best_sum:
            best_sum = s
            best_centers = opt_centers.copy()

    # Phase B: Nelder-Mead from the best (different basin behavior)
    if best_centers is not None and time.time() < deadline - 5.0:
        try:
            result = minimize(
                _lp_objective, best_centers.flatten(), method='Nelder-Mead',
                options={'maxiter': 3000, 'xatol': 1e-6, 'fatol': 1e-7,
                         'adaptive': True}
            )
            nm_centers = np.clip(result.x, 0.02, 0.98).reshape(26, 2)
            s = float(np.sum(_solve_radii(nm_centers)))
            if s > best_sum:
                best_sum = s
                best_centers = nm_centers.copy()
        except Exception:
            pass

    if best_centers is None:
        best_centers = inits[0]
        best_sum = float(np.sum(_solve_radii(best_centers)))

    radii = _solve_radii(best_centers)
    return best_centers, radii, float(np.sum(radii))
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