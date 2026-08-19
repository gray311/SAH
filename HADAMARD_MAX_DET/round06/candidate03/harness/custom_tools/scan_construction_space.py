def run(ctx, args):
    import numpy as np
    import random

    results = []
    n = 29
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    
    for t_start in [2.0, 3.0, 5.0]:
        for cool_rate in [0.995, 0.996, 0.997]:
            for seeds in [3, 5]:
                best_det = 0
                for s in range(seeds):
                    rng = random.Random(1000000 + s)
                    cur = np.zeros((n, n), dtype=int)
                    for i in range(n):
                        for j in range(n):
                            diff = (i - j) % n
                            cur[i, j] = 1 if diff in residues else -1
                    T = t_start
                    for _ in range(5000):
                        i, j = rng.randrange(n), rng.randrange(n)
                        cur[i, j] *= -1
                        nd = abs(np.linalg.det(cur.astype(float)))
                        if nd > best_det:
                            best_det = nd
                    cur = np.zeros((n, n), dtype=int)
                    for i in range(n):
                        for j in range(n):
                            diff = (i - j) % n
                            cur[i, j] = 1 if diff in residues else -1
                results.append({"type": "paley", "temp": t_start, 
                              "cool": cool_rate, "seeds": seeds, "det": best_det})
    
    results.sort(key=lambda x: x["det"], reverse=True)
    return {"rankings": results[:10]}
