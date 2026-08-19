# EVOLVE-BLOCK-START
"""Deterministic n=26 staggered-layout search with LP radius refinement."""
import numpy as np


def _optimal_radii(centers):
    n = len(centers)
    border = np.min(np.column_stack((centers, 1.0 - centers)), axis=1)
    try:
        from scipy.optimize import linprog
        rows, limits = [], []
        for i in range(n):
            for j in range(i + 1, n):
                row = np.zeros(n)
                row[i] = row[j] = 1.0
                rows.append(row)
                limits.append(float(np.linalg.norm(centers[i] - centers[j])))
        result = linprog(-np.ones(n), A_ub=np.asarray(rows),
                         b_ub=np.asarray(limits), bounds=[(0.0, float(v)) for v in border],
                         method="highs")
        if result.success:
            return np.maximum(result.x - 2e-8, 0.0)
    except Exception:
        pass
    radii = border.copy()
    for _ in range(25):
        for i in range(n):
            for j in range(i + 1, n):
                distance = float(np.linalg.norm(centers[i] - centers[j]))
                excess = radii[i] + radii[j] - distance
                if excess > 0:
                    cut_i = min(radii[i], 0.5 * excess + 1e-9)
                    radii[i] -= cut_i
                    radii[j] = max(0.0, radii[j] - (excess - cut_i + 1e-9))
    return np.maximum(radii - 2e-8, 0.0)


def _layout(counts, spacing, margin, phase):
    ys = np.linspace(margin, 1.0 - margin, len(counts))
    points = []
    for row, (count, y) in enumerate(zip(counts, ys)):
        start = 0.5 - 0.5 * (count - 1) * spacing
        if row % 2:
            start += phase * spacing
        end = start + (count - 1) * spacing
        if start <= 0.002 or end >= 0.998:
            return None
        points.extend((start + k * spacing, y) for k in range(count))
    return np.asarray(points, dtype=float)


def _score(centers):
    radii = _optimal_radii(centers)
    return float(np.sum(radii)), radii


def construct_packing():
    requested = [5, 5, 5, 5, 6]
    patterns = [requested, [4, 5, 4, 5, 4, 4], [5, 4, 5, 4, 4, 4],
                [5, 5, 5, 5, 6], [6, 5, 5, 5, 5]]
    unique, seen = [], set()
    for counts in patterns:
        key = tuple(counts)
        if key not in seen and sum(key) == 26:
            seen.add(key)
            unique.append(list(key))
    # A validity-safe 5x5 anchor plus one tiny corner circle matches the strong
    # historical 2.502 family; the staggered/LP search below can improve it.
    anchor = np.asarray([(0.1 + 0.2 * x, 0.1 + 0.2 * y)
                         for y in range(5) for x in range(5)] + [(0.002, 0.002)])
    best_sum, best_radii = _score(anchor)
    best_centers = anchor.copy()
    for counts in unique:
        for spacing in np.linspace(0.17, 0.225, 6):
            for margin in (0.06, 0.08, 0.10, 0.12):
                for phase in (-0.25, 0.0, 0.25):
                    centers = _layout(counts, float(spacing), margin, phase)
                    if centers is None or centers.shape != (26, 2):
                        continue
                    value, radii = _score(centers)
                    if value > best_sum:
                        best_sum, best_centers, best_radii = value, centers.copy(), radii
    for _ in range(2):
        for step in (0.012, 0.006, 0.003):
            for i in range(26):
                for dim in (0, 1):
                    for direction in (-1.0, 1.0):
                        trial = best_centers.copy()
                        trial[i, dim] += direction * step
                        if not 0.002 < trial[i, dim] < 0.998:
                            continue
                        value, radii = _score(trial)
                        if value > best_sum + 1e-9:
                            best_sum, best_centers, best_radii = value, trial, radii
    best_radii = np.maximum(best_radii - 2e-8, 0.0)
    return best_centers, best_radii, float(np.sum(best_radii))
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