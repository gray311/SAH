def run(ctx, args):
    import numpy as np
    n = 29
    quadratic_residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    H = []
    for i in range(n):
        row = []
        for j in range(n):
            diff = (i - j) % n
            if diff in quadratic_residues:
                row.append(1)
            else:
                row.append(-1)
        H.append(row)
    det_val = abs(np.linalg.det(np.array(H, dtype=float)))
    ratio = det_val / (n * np.sqrt(n))
    return {
        "paley_matrix_constructed": True,
        "n": n,
        "paley_det": float(det_val),
        "expected_max": float(n * np.sqrt(n)),
        "quality_ratio": float(ratio),
        "valid": ratio > 0.7,
        "recommendation": "FIX PALEY CONSTRUCTION" if ratio < 0.7 else "PALEY IS VALID, proceed to hill climbing"
    }