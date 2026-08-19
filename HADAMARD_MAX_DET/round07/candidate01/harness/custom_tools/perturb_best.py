def run(ctx, args):
    import numpy as np
    
    n = 29
    best = args.get("best_matrix")
    if best is None:
        return {"variants": [], "num_flips": 0, "num_variants": 0}
    if isinstance(best, np.ndarray):
        best = best.tolist()
    else:
        best = list(best)
    
    num_flips = args.get("num_flips", 10)
    num_variants = args.get("num_variants", 5)
    
    variants = []
    base = [row[:] for row in best]
    
    for v in range(num_variants):
        variant = [row[:] for row in base]
        flips = np.random.choice(n*n, size=num_flips, replace=False).tolist()
        for flip_idx in flips:
            i = flip_idx // n
            j = flip_idx % n
            variant[i][j] *= -1
        variants.append(variant)
    
    return {"variants": variants, "num_flips": num_flips, "num_variants": num_variants}