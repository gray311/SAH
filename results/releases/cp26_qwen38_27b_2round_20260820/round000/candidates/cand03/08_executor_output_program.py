# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles (hexagonal patch)"""
import numpy as np


def build_hex(rows, a):
    n_rows = len(rows)
    centers = []
    for k, n_k in enumerate(rows):
        y = 0.5 + (k - (n_rows - 1) / 2.0) * a * np.sqrt(3) / 2.0
        x0 = 0.5 - (n_k - 1) * a / 2.0
        for i in range(n_k):
            x = x0 + i * a
            centers.append([x, y])
    return np.array(centers, dtype=float)


def radii_for(centers):
    """Per-circle radius = min(wall distance, half nearest-neighbor distance)."""
    n = len(centers)
    r = np.empty(n)
    for i in range(n):
        x, y = centers[i]
        wall = min(x, y, 1 - x, 1 - y)
        nn = 1e9
        for j in range(n):
            if i == j:
                continue
            d = float(np.hypot(centers[i, 0] - centers[j, 0],
                               centers[i, 1] - centers[j, 1]))
            nn = min(nn, d)
        r[i] = min(wall, nn / 2.0)
    return r


def construct_packing():
    rows = [6, 5, 6, 5, 4]
    best = None
    for a in [0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22]:
        centers = build_hex(rows, a)
        # validity guard: all circles must be inside
        ok = True
        for (x, y) in centers:
            if x < 0 or x > 1 or y < 0 or y > 1:
                ok = False
                break
        if not ok:
            continue
        r = radii_for(centers)
        s = float(np.sum(r))
        if best is None or s > best[0]:
            best = (s, centers.copy(), r.copy())
    return best[1], best[2], best[0]
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