def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    patterns = []
    for b_frac in [1/6, 1/5, 1/4, 1/3, 0.3, 0.4, 0.5, 0.6, 2/3, 3/4, 4/5, 5/6, 0.618]:
        h = np.zeros(N)
        cutoff = int(b_frac * N)
        h[cutoff:] = 1.0
        total = h.sum() * dx
        h = h / total
        patterns.append(("2-level", b_frac, h))
    for n in [3, 4, 5, 6]:
        levels = np.linspace(0, 1, n+1)[1:-1]
        h = np.zeros(N)
        for i, level in enumerate(levels):
            start = int(i * N / n)
            end = int((i+1) * N / n)
            h[start:end] = level
        total = h.sum() * dx
        h = h / total
        patterns.append(("3-level-uniform", n, h))
    return {"candidates": patterns, "num_generated": len(patterns)}