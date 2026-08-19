def run(ctx, args):
    import numpy as np
    import random
    
    def det_bareiss(A):
        size = len(A)
        if size == 0:
            return 1
        M = [row.copy() for row in A]
        for k in range(size - 1):
            if M[k][k] == 0:
                for i in range(k + 1, size):
                    if M[i][k] != 0:
                        M[k], M[i] = M[i], M[k]
                        break
                else:
                    return 0
            for i in range(k + 1, size):
                for j in range(k + 1, size):
                    num = M[i][j] * M[k][k] - M[i][k] * M[k][j]
                    den = M[k - 1][k - 1] if k > 0 else 1
                    M[i][j] = num // den
        return M[-1][-1]
    
    def hill_climb(A, iters=500, seed=42):
        rng = random.Random(seed)
        curr = [row.copy() for row in A]
        det_curr = det_bareiss(curr)
        best_det = det_curr
        best_mat = [row.copy() for row in curr]
        for t in range(iters):
            i, j = rng.randrange(29), rng.randrange(29)
            curr[i][j] = -curr[i][j]
            new_det = det_bareiss(curr)
            T = 0.5 / (1.0 + t * 0.001)
            if abs(new_det) >= abs(det_curr) or (rng.random() < np.exp((abs(new_det) - abs(det_curr)) / max(1.0, T * abs(det_curr)))):
                det_curr = new_det
                if abs(det_curr) > abs(best_det):
                    best_det = det_curr
                    best_mat = [row.copy() for row in curr]
            else:
                curr[i][j] = -curr[i][j]
        return best_det
    
    try:
        prog = ctx.get_program()
        
        # Generate Paley construction
        n = 29
        residues = {1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
        matrix = [[1]]
        for i in range(1, n):
            row = [1 if (i-j) % n in residues else -1 for j in range(n)]
            matrix.append(row)
        
        # Subsample to 5x5 for fast probe
        idx = np.random.RandomState(42).choice(n, size=(5, n), replace=False)
        sampled = np.array(matrix)[idx]
        probe_det = det_bareiss(sampled)
        approx_score = abs(probe_det) / (n**2)
        
        # Quick hill climb on sampled
        sampled_list = sampled.tolist()
        probed_det = det_bareiss(sampled_list)
        sampled_list = hill_climb(sampled_list, iters=100, seed=123)
        sampled_final = np.array(sampled_list)
        probed_det = det_bareiss(sampled_final)
        approx_score = abs(probed_det) / (n**2)
        
        return {
            "method": "paley_probe",
            "probe_score": float(approx_score),
            "det": probed_det,
            "note": "Subsampled Paley + hill climb"
        }
    except Exception as e:
        return {"note": f"probe failed: {str(e)}", "probe_score": 0.0}
