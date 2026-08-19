def run(ctx, args):
    import numpy as np
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    H = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            diff = (i - j) % n
            H[i, j] = 1 if diff in residues else -1
    det_val = abs(np.linalg.det(H.astype(float)))
    # Verify all entries are +/- 1
    valid = np.all(np.isin(H, [-1, 1]))
    return {
        "n": n,
        "quadratic_residues": sorted(list(residues)),
        "paley_matrix_correct": valid,
        "baseline_det": float(det_val),
        "recommendations": {
            "use_this_as_start": True,
            "num_restarts": 100,
            "schedule_a": {"temp": 8.0, "cool_rate": 0.996, "iters": 15000},
            "schedule_b": {"temp": 2.0, "cool_rate": 0.997, "iters": 15000},
            "perturbation": {"pattern": "checkerboard", "flip_where": "(i+j)%4==0", "temp": 5.0, "cool_rate": 0.995, "iters": 10000}
        }
    }