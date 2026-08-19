def run(ctx, args):
    import numpy as np
    import random
    n = 29
    strategy = args.get("strategy", "paley")
    seeds = args.get("seeds", 2)
    iters = args.get("iterations", 2000)
    
    if strategy == "paley":
        residues = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
        def construct():
            return [[1 if (i-j)%n in residues else -1 for j in range(n)] for i in range(n)]
    elif strategy == "random":
        def construct():
            return [[random.choice([1, -1]) for _ in range(n)] for _ in range(n)]
    elif strategy == "perturbed":
        residues = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
        def construct():
            H = [[1 if (i-j)%n in residues else -1 for j in range(n)] for i in range(n)]
            flips = random.sample([(i,j) for i in range(n) for j in range(n)], 5)
            for i,j in flips:
                H[i][j] *= -1
            return H
    elif strategy == "alt_residues":
        choices = [(0,14), (1,14), (2,14), (3,14), (4,14), (5,14)]
        r = random.Random(42)
        selected = r.sample(choices, 6)
        residues = {diff for diff in selected for _ in range(15)} | {0, 1, 4, 5, 6, 7}
        residues = set([(i-j)%n for i in range(n) for j in range(n)] if (i-j)%n <= 14 else None)
        residues = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
        def construct():
            return [[1 if (i-j)%n in residues else -1 for j in range(n)] for i in range(n)]
    else:
        return {"error": f"Unknown strategy: {strategy}"}
    
    rng = random.Random(12345)
    best_det = 0
    best_matrix = None
    
    for s in range(seeds):
        mat = construct()
        det_val = abs(np.linalg.det(np.array(mat, dtype=float)))
        if det_val > best_det:
            best_det = det_val
            best_matrix = [row[:] for row in mat]
    
    return {
        "strategy": strategy,
        "seeds_run": seeds,
        "iterations_per_seed": iters,
        "best_det": float(best_det),
        "best_matrix_size": f"{len(best_matrix)}x{len(best_matrix[0]) if best_matrix else 0}"
    }