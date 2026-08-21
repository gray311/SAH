# EVOLVE-BLOCK-START
"""Packing n=26: 4 corners + hex core, shrink-to-touch radii (proven)."""
import numpy as np


def _max_radii(centers):
    """Greedy shrink: each pass, resolve the pair with the largest overlap first."""
    centers = np.asarray(centers, dtype=float)
    n = centers.shape[0]
    r = np.array([min(c[0], 1 - c[0], c[1], 1 - c[1]) for c in centers])
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = np.hypot(centers[i][0] - centers[j][0],
                               centers[i][1] - centers[j][1])
    for _ in range(300):
        # find the pair with the largest (r_i + r_j - d) overlap
        best_i, best_j, best_ov = -1, -1, 1e-9
        for i in range(n):
            for j in range(i + 1, n):
                ov = r[i] + r[j] - D[i, j]
                if ov > best_ov:
                    best_ov, best_i, best_j = ov, i, j
        if best_i < 0:
            break
        d = D[best_i, best_j]
        t = d / (r[best_i] + r[best_j])
        r[best_i] *= t
        r[best_j] *= t
    return r


def construct_packing():
    n = 26
    centers = []

    rc = 0.16
    centers.append([rc, rc])
    centers.append([1 - rc, rc])
    centers.append([rc, 1 - rc])
    centers.append([1 - rc, 1 - rc])

    dx = 0.205
    dy = np.sqrt(3) / 2 * dx

    pts = []
    for row in range(-4, 5):
        for col in range(-4, 5):
            x = col * dx + (0.5 * dx if (row % 2) else 0.0)
            y = row * dy
            pts.append([x, y])
    pts = np.array(pts)

    dists = np.linalg.norm(pts, axis=1)
    order = np.argsort(dists)
    core = pts[order[:22]]

    centroid = core.mean(axis=0)
    core = core - centroid + np.array([0.5, 0.5])
    centers.extend([list(p) for p in core])

    centers = np.array(centers, dtype=float)
    centers = np.clip(centers, 0.02, 0.98)

    radii = _max_radii(centers)
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