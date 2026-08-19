import numpy as np

def compute_max_radii(centers):
    n = centers.shape[0]
    radii = np.zeros(n)
    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))
            if radii[i] + radii[j] > dist:
                if radii[i] >= radii[j]:
                    radii[i] = max(0.001, dist - radii[j])
                else:
                    radii[j] = max(0.001, dist - radii[i])
    return radii

def run(ctx, args):
    centers = []
    centers.append([0.5, 0.5])
    r_center = 0.16
    for angle in [0, 60, 120, 180, 240, 300]:
        rad = angle * np.pi / 180
        centers.append([0.5 + r_center * 2 * np.cos(rad), 0.5 + r_center * 2 * np.sin(rad)])
    corners = [(0.05, 0.05), (0.95, 0.05), (0.05, 0.95), (0.95, 0.95)]
    centers.extend(corners)
    edges = [(0.5, 0.05), (0.5, 0.95), (0.05, 0.5), (0.95, 0.5)]
    centers.extend(edges)
    fill_positions = [
        (0.2, 0.2), (0.8, 0.2), (0.2, 0.8), (0.8, 0.8),
        (0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7),
        (0.4, 0.2), (0.6, 0.2), (0.4, 0.8), (0.6, 0.8)
    ]
    for pos in fill_positions:
        centers.append(list(pos))
    centers = np.array(centers)
    radii = compute_max_radii(centers)
    best = np.sum(np.maximum(radii, 0.001))
    return {"best_score": best, "budget_left": ctx.budget_left()}
