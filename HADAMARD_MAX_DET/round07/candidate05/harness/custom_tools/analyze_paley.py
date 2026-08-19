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
    return {"paley_matrix": H.tolist(), "det": float(det_val), "n": n}
