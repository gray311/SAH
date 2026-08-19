def run(ctx, args):
    import numpy as np
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    
    # Build base Paley
    paley = [[1 if (i-j)%n in residues else -1 for j in range(n)] for i in range(n)]
    base_det = abs(np.linalg.det(np.array(paley, dtype=float)))
    
    # Function to run quick SA
    def quick_sa(start_mat, iters, T, cool):
        rng = np.random.RandomState(42)
        cur = [row[:] for row in start_mat]
        best = cur[:]
        cd = abs(np.linalg.det(np.array(cur, dtype=float)))
        bd = cd
        T_val = T
        
        for _ in range(iters):
            i, j = rng.randint(0, n), rng.randint(0, n)
            cur[i][j] *= -1
            nd = abs(np.linalg.det(np.array(cur, dtype=float)))
            delta = nd - cd
            
            if delta >= 0:
                cd = nd
                if T_val > 1e-15: T_val *= cool
            elif T_val > 1e-15 and rng.random() < np.exp(delta/T_val):
                cd = nd
                if T_val > 1e-15: T_val *= cool
            else:
                cur[i][j] *= -1
                if T_val > 1e-15: T_val *= cool
            
            if nd > bd: bd, best = nd, cur[:]
        return best, bd
    
    # Test strategies
    results = {}
    
    # 1. Single Paley
    best500, d500 = quick_sa(paley, 100, 5.0, 0.997)
    results["single_paley"] = float(d500)
    
    # 2. Perturbed Paley (5 flips)
    pert5 = paley.copy()
    rng2 = np.random.RandomState(42)
    for _ in range(5):
        i, j = rng2.randint(0, n), rng2.randint(0, n)
        pert5[i][j] *= -1
    best5, d5 = quick_sa(pert5, 100, 5.0, 0.997)
    results["perturbed_5flips"] = float(d5)
    
    # 3. Perturbed Paley (15 flips)
    pert15 = paley.copy()
    rng3 = np.random.RandomState(42)
    for _ in range(15):
        i, j = rng3.randint(0, n), rng3.randint(0, n)
        pert15[i][j] *= -1
    best15, d15 = quick_sa(pert15, 100, 5.0, 0.997)
    results["perturbed_15flips"] = float(d15)
    
    # 4. Random start
    rng4 = np.random.RandomState(42)
    rand_mat = [[rng4.randint(0, 2)*2 - 1 for _ in range(n)] for _ in range(n)]
    bestrand, drand = quick_sa(rand_mat, 100, 10.0, 0.997)
    results["random_start"] = float(drand)
    
    return {
        "n": n,
        "seed_paley_det": float(base_det),
        "results": results,
        "recommendation": "If perturbed versions beat single_paley, use multi-chain strategy"
    }