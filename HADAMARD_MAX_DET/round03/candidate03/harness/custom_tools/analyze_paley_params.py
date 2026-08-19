def run(ctx, args):
    import numpy as np
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    H = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            diff = (i - j) % n
            H[i, j] = 1 if diff in residues else -1
    det_val = abs(np.linalg.det(H))
    # Expected range for n=29 Hadamard-like: 100-180
    expected_range = (100, 180)
    return {
        "n": n,
        "quadratic_residues": sorted(list(residues)),
        "paley_det": float(det_val),
        "expected_det_range": [expected_range[0], expected_range[1]],
        "recommendations": {
            "iterations_per_seed": 25000,
            "num_seeds": 5,
            "cooling_schedules": [
                {"initial_temp": 2.5, "cool_rate": 0.995},
                {"initial_temp": 1.0, "cool_rate": 0.998},
                {"initial_temp": 5.0, "cool_rate": 0.992}
            ],
            "use_numpy_det": True,
            "total_expected_time_seconds": 15
        }
    }