# EVOLVE-BLOCK-START
"""Constructor-based circle packing for n=26 circles"""
import numpy as np
from scipy.optimize import linprog, minimize


def construct_packing():
    """
    Construct a specific arrangement of 26 circles in a unit square
    that attempts to maximize the sum of their radii.
    Uses local optimization of center positions to maximize LP sum.
    """
    n = 26
    best_centers = None
    best_sum = -1

    # Generate multiple initial configurations
    inits = []

    # Hex lattice with various spacings
    for s in [0.14, 0.15, 0.16, 0.17]:
        pts = hex_lattice(s)
        if len(pts) >= 26:
            dists = np.sqrt((pts[:, 0] - 0.5)**2 + (pts[:, 1] - 0.5)**2)
            idx = np.argsort(dists)
            inits.append(pts[idx[:26]].copy())

    # Grid 5x5 + 1
    grid_pts = []
    for i in range(5):
        for j in range(5):
            grid_pts.append([0.1 + i*0.2, 0.1 + j*0.2])
    grid_pts.append([0.5, 0.5])
    inits.append(np.array(grid_pts[:26]))

    # Structured rows
    for config in [[5,5,5,5,5,1], [4,5,5,5,5,2], [3,5,5,5,5,3]]:
        centers = row_config(config)
        inits.append(centers)

    # Optimize each initial configuration
    for init in inits:
        # Local optimization of center positions
        result = minimize(
            lambda x: -lp_sum(x.reshape(26, 2)),
            init.flatten(),
            method='L-BFGS-B',
            bounds=[(0.01, 0.99)] * 52,
            options={'maxiter': 200, 'ftol': 1e-8}
        )
        opt_centers = result.x.reshape(26, 2)
        radii = solve_max_radii_lp(opt_centers)
        s_sum = np.sum(radii)
        if s_sum > best_sum:
            best_sum = s_sum
            best_centers = opt_centers.copy()

    radii = solve_max_radii_lp(best_centers)
    return best_centers, radii, np.sum(radii)


def hex_lattice(s):
    dy = s * np.sqrt(3) / 2
    pts = []
    row = 0
    y = 0.02
    while y <= 0.98:
        x_offset = (s / 2) if (row % 2 == 1) else 0
        x = 0.02 + x_offset
        while x <= 0.98:
            pts.append([x, y])
            x += s
        y += dy
        row += 1
    return np.array(pts)


def row_config(config):
    n = sum(config)
    n_rows = len(config)
    dy = 1.0 / (n_rows + 1)
    centers = np.zeros((n, 2))
    idx = 0
    for r in range(n_rows):
        n_in_row = config[r]
        y = dy * (r + 1)
        if n_in_row > 1:
            xs = np.linspace(0.1, 0.9, n_in_row)
        else:
            xs = np.array([0.5])
        for x in xs:
            centers[idx] = [x, y]
            idx += 1
    return centers


def lp_sum(centers):
    """Compute sum of optimal radii for given centers (for optimization)."""
    radii = solve_max_radii_lp(centers)
    return np.sum(radii)


def solve_max_radii_lp(centers):
    n = centers.shape[0]
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
    else:
        return compute_max_radii_fallback(centers)


def compute_max_radii_fallback(centers):
    n = centers.shape[0]
    radii = np.ones(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    for _ in range(200):
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
                if radii[i] + radii[j] > dist:
                    scale = dist / (radii[i] + radii[j])
                    radii[i] *= scale
                    radii[j] *= scale
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