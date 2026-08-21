# EVOLVE-BLOCK-START
"""Circle packing for n=26: hexagonal layout + L-BFGS center optimization."""
import numpy as np
from scipy.optimize import linprog, minimize


def _radii_lp(centers):
    n = len(centers)
    c = -np.ones(n)
    A_rows = []
    b_vals = []
    for i in range(n):
        for j in range(i + 1, n):
            d = np.hypot(centers[i][0] - centers[j][0],
                         centers[i][1] - centers[j][1])
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
    wall = np.array([min(x, y, 1 - x, 1 - y) for x, y in centers])
    return wall


def _neg_sum_lp(centers_flat):
    centers = centers_flat.reshape(-1, 2)
    return -float(np.sum(_radii_lp(centers)))


def construct_packing():
    n = 26

    # Hexagonal layout: rows of 5-4-5-4-5-3 = 26
    centers = []
    y0 = 0.08
    for c in range(5):
        centers.append([0.1 + c * 0.2, y0])
    y1 = 0.22
    for c in range(4):
        centers.append([0.2 + c * 0.2, y1])
    y2 = 0.36
    for c in range(5):
        centers.append([0.1 + c * 0.2, y2])
    y3 = 0.50
    for c in range(4):
        centers.append([0.2 + c * 0.2, y3])
    y4 = 0.64
    for c in range(5):
        centers.append([0.1 + c * 0.2, y4])
    y5 = 0.78
    for c in range(3):
        centers.append([0.2 + c * 0.2, y5])
    centers = np.array(centers, dtype=float)

    # Also try 5x5 grid + 1
    centers2 = []
    for i in range(5):
        for j in range(5):
            centers2.append([0.1 + i * 0.2, 0.1 + j * 0.2])
    centers2.append([0.5, 0.5])  # duplicate, will be handled
    # Remove duplicate and add a gap circle
    centers2 = []
    for i in range(5):
        for j in range(5):
            centers2.append([0.1 + i * 0.2, 0.1 + j * 0.2])
    # 25 circles, add 26th in a gap between (0.5,0.5),(0.7,0.5),(0.5,0.7),(0.7,0.7)
    centers2.append([0.6, 0.6])
    centers2 = np.array(centers2, dtype=float)

    best_centers = None
    best_sum = -1

    for init in [centers, centers2]:
        result = minimize(
            _neg_sum_lp,
            init.flatten(),
            method='L-BFGS-B',
            bounds=[(0.02, 0.98)] * 52,
            options={'maxiter': 300, 'ftol': 1e-10}
        )
        opt_centers = result.x.reshape(26, 2)
        radii = _radii_lp(opt_centers)
        s = float(np.sum(radii))
        if s > best_sum:
            best_sum = s
            best_centers = opt_centers.copy()

    radii = _radii_lp(best_centers)
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