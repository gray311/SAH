def run(ctx, args):
    import numpy as np
    import random
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    def build_paley():
        H = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                diff = (i - j) % n
                H[i, j] = 1 if diff in residues else -1
        return H
    def quick_anneal(H, seed, iters):
        rng = random.Random(seed)
        cur = [row[:] for row in H]
        det_fn = lambda A: abs(np.linalg.det(np.array(A, dtype=float)))
        cd = det_fn(cur)
        best = [row[:] for row in cur]
        best_det = cd
        T = 3.0
        for _ in range(iters):
            i, j = rng.randrange(n), rng.randrange(n)
            cur[i][j] *= -1
            nd = det_fn(cur)
            delta = nd - cd
            if delta >= 0:
                cd = nd
                T *= 0.997
            elif T > 1e-15 and rng.random() < np.exp(delta/T):
                cd = nd
                T *= 0.997
            if nd > best_det:
                best_det = nd
                best = [row[:] for row in cur]
        return best_det, best
    best_det = 0
    for seed in range(args.get("min_seed", 0), args.get("max_seed", 100)+1):
        H = build_paley()
        det_val, _ = quick_anneal(H, seed, args.get("iterations_per_seed", 1000))
        if det_val > best_det:
            best_det = det_val
    return {"best_det": float(best_det)}