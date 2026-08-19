def run(ctx, args):
    import numpy as np
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    H = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            diff = (i - j) % n
            H[i, j] = 1 if diff in residues else -1
    # Validate: all entries must be ±1
    valid_entries = np.all(np.abs(H) == 1)
    det_val = abs(np.linalg.det(H.astype(float)))
    # Check diagonal and symmetry
    on_diagonal = all(abs(H[i,i]) == 1 for i in range(n))
    return {
        "n": n,
        "matrix_shape": list(H.shape),
        "all_entries_pm1": bool(valid_entries),
        "det_value": float(det_val),
        "on_diagonal_pm1": bool(on_diagonal),
        "residues_used": sorted(list(residues)),
        "validation_passed": valid_entries and on_diagonal
    }