def run(ctx, args):
    import numpy as np
    import random

    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    best_det = 0
    best_mat = None
    strategy = args.get("strategy", "shifted")
    shift = args.get("shift", 0)
    num_shifts = args.get("num_shifts", 3)
    iters = args.get("iterations", 10000)
    num_seeds = args.get("num_seeds", 5)

    for s in range(shift, shift + num_shifts):
        shifted_residues = {(r + s) % n for r in residues}
        # Build Paley with shifted residues
        paly = [[1 if (i - j) % n in shifted_residues else -1 for j in range(n)] for i in range(n)]

        # Quick SA
        rng = random.Random(42 + s)
        cur = [row[:] for row in paly]
        T_val = 10.0
        cd = abs(np.linalg.det(np.array(cur, dtype=float)))

        for _ in range(iters):
            i, j = rng.randrange(n), rng.randrange(n)
            cur[i][j] *= -1
            nd = abs(np.linalg.det(np.array(cur, dtype=float)))
            delta = nd - cd
            if delta >= 0:
                cd = nd
            elif T_val > 1e-15 and rng.random() < np.exp(delta / T_val):
                cd = nd
            else:
                cur[i][j] *= -1

            if nd > best_det:
                best_det, best_mat = nd, [row[:] for row in cur]

    return {"strategy": strategy, "best_det": float(best_det), "estimated_time": num_shifts * iters * 0.001 * 10}