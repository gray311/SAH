# EVOLVE-BLOCK-START
import numpy as np
from scipy.optimize import linprog

_N = 26
_pair_idx = [(i, j) for i in range(_N) for j in range(i + 1, _N)]
_A = np.zeros((len(_pair_idx) + _N, _N))
for k, (i, j) in enumerate(_pair_idx):
    _A[k, i] = 1.0
    _A[k, j] = 1.0
for i in range(_N):
    _A[len(_pair_idx) + i, i] = 1.0
_BOUNDS = [(0, None)] * _N
_C = -np.ones(_N)


def _lp_b(centers):
    b = np.empty(len(_pair_idx) + _N)
    k = 0
    for (i, j) in _pair_idx:
        b[k] = np.hypot(centers[i, 0] - centers[j, 0],
                        centers[i, 1] - centers[j, 1])
        k += 1
    for i in range(_N):
        x, y = centers[i]
        b[k] = min(x, y, 1 - x, 1 - y)
        k += 1
    return b


def solve_radii_lp(centers):
    res = linprog(_C, A_ub=_A, b_ub=_lp_b(centers),
                  bounds=_BOUNDS, method='highs')
    if res.success:
        return np.maximum(res.x, 0.0)
    return _explicit_radii(centers)


def construct_packing():
    best = None
    best_sum = -1.0
    for base in _all_constructions():
        radii = solve_radii_lp(base)
        s = float(np.sum(radii))
        c, radii, s = _hill_climb(base, radii, s, rounds=8, seed=0,
                                  joint=True)
        c, radii, s = _hill_climb(c, radii, s, rounds=4, seed=99,
                                  step0=0.02, joint=False)
        if s > best_sum:
            best_sum = s
            best = (c, radii)
    return best[0], best[1], best_sum


def _all_constructions():
    cands = []
    g = np.array([[0.1 + 0.2 * i, 0.1 + 0.2 * j]
                  for i in range(5) for j in range(5)])
    cands.append(np.vstack([g, [0.5, 0.5]]))
    pts = np.array([[0.15 + 0.7 * i / 4, 0.15 + 0.7 * j / 4]
                    for i in range(5) for j in range(5)])
    cands.append(np.vstack([pts, [0.5, 0.5]]))
    # corner-biased (strong push)
    pts = np.array([[0.15 + 0.7 * i / 4, 0.15 + 0.7 * j / 4]
                    for i in range(5) for j in range(5)])
    for i in range(5):
        for j in range(5):
            tx = 0.07 if i == 0 else (0.93 if i == 4 else None)
            ty = 0.07 if j == 0 else (0.93 if j == 4 else None)
            if tx is not None:
                pts[i * 5 + j, 0] = tx
            if ty is not None:
                pts[i * 5 + j, 1] = ty
    cands.append(np.vstack([pts, [0.5, 0.5]]))
    # edge-pushed: edge circles pushed to the border
    pts = np.array([[0.15 + 0.7 * i / 4, 0.15 + 0.7 * j / 4]
                    for i in range(5) for j in range(5)])
    for i in range(5):
        for j in range(5):
            if i == 0:
                pts[i * 5 + j, 0] = 0.06
            elif i == 4:
                pts[i * 5 + j, 0] = 0.94
            if j == 0:
                pts[i * 5 + j, 1] = 0.06
            elif j == 4:
                pts[i * 5 + j, 1] = 0.94
    cands.append(np.vstack([pts, [0.5, 0.5]]))
    return cands


def _hill_climb(centers, radii, cur, rounds=9, seed=0, step0=0.06,
                joint=True):
    rng = np.random.default_rng(seed)
    n = centers.shape[0]
    best = cur
    best_c = centers.copy()
    best_r = radii.copy()
    order = list(range(n))
    step = step0
    for _ in range(rounds):
        rng.shuffle(order)
        for i in order:
            for ax in (0, 1):
                for sgn in (1.0, -1.0):
                    trial = best_c.copy()
                    trial[i, ax] = np.clip(best_c[i, ax] + sgn * step,
                                           1e-3, 1 - 1e-3)
                    r = solve_radii_lp(trial)
                    s = float(np.sum(r))
                    if s > best + 1e-9:
                        best = s
                        best_c = trial
                        best_r = r
            if joint:
                for dx in (-step, 0.0, step):
                    for dy in (-step, 0.0, step):
                        if dx == 0 and dy == 0:
                            continue
                        trial = best_c.copy()
                        trial[i, 0] = np.clip(best_c[i, 0] + dx,
                                              1e-3, 1 - 1e-3)
                        trial[i, 1] = np.clip(best_c[i, 1] + dy,
                                              1e-3, 1 - 1e-3)
                        r = solve_radii_lp(trial)
                        s = float(np.sum(r))
                        if s > best + 1e-9:
                            best = s
                            best_c = trial
                            best_r = r
        step *= 0.6
    return best_c, best_r, best


def _explicit_radii(centers):
    n = centers.shape[0]
    wall = np.array([min(x, y, 1 - x, 1 - y) for x, y in centers])
    r = wall.copy()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = np.hypot(centers[i, 0] - centers[j, 0],
                         centers[i, 1] - centers[j, 1])
            r[i] = min(r[i], d - r[j])
    return np.clip(r, 0.0, wall)
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