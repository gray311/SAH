def run(ctx, args):
    import numpy as np
    n = 29
    results = {}
    
    if args.get("num_matrices", 3) > 0:
        for i in range(args.get("num_matrices", 3)):
            rng = np.random.RandomState(i + 42)
            mat = rng.randint(-1, 2, size=(n, n)) - 1
            results[f"random_{i}"] = mat.tolist()
    
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    paley = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            diff = (i - j) % n
            paley[i, j] = 1 if diff in residues else -1
    results["paley"] = paley.tolist()
    
    greedy = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            greedy[i, j] = 1 if i == j else -1
    results["greedy"] = greedy.tolist()
    
    return {"num_matrices": args.get("num_matrices", 3), "paly_variations": args.get("paly_variations", 2), "matrices": results}
