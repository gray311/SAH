# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 (non-uniform grid + polish)"""
import numpy as np


def _wall_slack(c):
    return min(c[0], c[1], 1.0 - c[0], 1.0 - c[1])


def _radii_for(centers):
    n = centers.shape[0]
    r = np.array([_wall_slack(centers[i]) for i in range(n)])
    for _ in range(3):
        for i in range(n):
            for j in range(i + 1, n):
                d = np.linalg.norm(centers[i] - centers[j])
                if r[i] + r[j] > d:
                    scale = d / (r[i] + r[j])
                    r[i] *= scale
                    r[j] *= scale
    return r


def _objective(centers):
    return float(np.sum(_radii_for(centers)))


def construct_packing():
    n = 26
    # Non-uniform 5x6 grid: outer ring pushed toward walls (bigger circles),
    # interior densified (smaller circles). Dropped sites: 4.
    xs = np.array([0.06, 0.27, 0.50, 0.73, 0.94])
    ys = np.array([0.06, 0.25, 0.43, 0.57, 0.75, 0.94])
    pts = np.array([[x, y] for y in ys for x in xs])
    slack = np.array([_wall_slack(p) for p in pts])
    order = np.argsort(slack)
    keep = np.setdiff1d(np.arange(len(pts)), order[:4])
    centers = pts[keep].copy()
    assert len(centers) == n

    # Deterministic polish.
    rng = np.random.default_rng(0)
    best = _objective(centers)
    step = 0.02
    for it in range(2000):
        i = it % n
        base = centers[i].copy()
        for _ in range(8):
            cand = centers.copy()
            cand[i] = np.clip(base + np.array([rng.uniform(-step, step),
                                               rng.uniform(-step, step)]), 0.0, 1.0)
            val = _objective(cand)
            if val > best + 1e-12:
                centers = cand
                best = val
                break
        if it % 200 == 199:
            step *= 0.85
    centers = np.clip(centers, 0.0, 1.0)
    radii = _radii_for(centers)
    return centers, radii, float(np.sum(radii))
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