def run(ctx, args):
    import numpy as np
    N_base = 800
    domain = 2.0
    candidates = []
    
    # Construction 1: Uniform n-partitions for n in [2, 6]
    for n in [2, 3, 4, 5, 6]:
        boundaries = np.linspace(0, domain, n+1)[1:-1]
        values = np.ones(n) / n
        candidates.append((boundaries.tolist(), values.tolist()))
    
    # Construction 2: Two-interval alternating (a, b) with integral = 1
    # h = a on [0, x), h = b on [x, 2]
    # constraint: a*x + b*(2-x) = 1
    # Try various ratios and solve for x
    for ratio in [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9]:
        a = 1 - ratio
        b = ratio
        x_opt = 1 / (a + b)
        if 0 < x_opt < 2:
            boundaries = [x_opt]
            values = [a, b]
            candidates.append((boundaries, values))
    
    # Construction 3: Golomb-like spacing for n=5
    marks = [0, 0.25, 0.625, 0.9375, 1.0]
    widths = [marks[i+1] - marks[i] for i in range(4)]
    values_uniform = np.ones(5) / 5
    candidates.append((marks[:-1], values_uniform.tolist()))
    
    # Construction 4: Concentrated mass
    for center in [0.25, 0.5, 0.75, 1.0, 1.25]:
        boundaries = [center - 0.1, center + 0.1]
        values = [1.0, 0.0]
        candidates.append((boundaries, values))
    
    return {"constructions": candidates, "count": len(candidates)}
