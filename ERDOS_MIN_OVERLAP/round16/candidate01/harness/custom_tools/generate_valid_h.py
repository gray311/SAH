def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    constructions = {}
    
    # Golomb-like: 5 narrow peaks at optimal marks for minimizing max overlap
    marks = np.array([0.0, 0.5, 1.6, 1.5, 1.0])
    peaks = [0.1, 0.2, 0.3, 0.25, 0.25]
    h = np.zeros(N)
    for m, w in zip(marks, peaks):
        idx_start = int(m * N / domain)
        idx_end = int((m + 2*w) * N / domain)
        if idx_end < N:
            h[idx_start:idx_end] = 1.0
    integral = np.sum(h) * dx
    if integral > 0:
        h = h / integral
    constructions['h_golomb'] = h
    
    # Bipartite: high on [0,0.75), low on [0.75, 1.5), high on [1.5,2]
    h = np.zeros(N)
    h[:int(0.75*N/domain)] = 1.0
    h[int(0.75*N/domain):int(1.5*N/domain)] = 0.0
    h[int(1.5*N/domain):] = 0.5
    integral = np.sum(h) * dx
    if integral > 0:
        h = h / integral
    constructions['h_bipartite'] = h
    
    # Triple peaks at 0.33, 1.0, 1.66
    h = np.zeros(N)
    for peak in [0.33, 1.0, 1.66]:
        idx = int(peak * N / domain)
        half = int(0.15 * N / domain)
        if idx + half < N:
            h[idx:idx+half] = 1.0
    integral = np.sum(h) * dx
    if integral > 0:
        h = h / integral
    constructions['h_triplet'] = h
    
    # Triangular wave: high-low-high-low-high
    h = np.zeros(N)
    h[:int(0.4*N/domain)] = 1.0
    h[int(0.4*N/domain):int(0.6*N/domain)] = 0.0
    h[int(0.6*N/domain):int(0.8*N/domain)] = 1.0
    h[int(0.8*N/domain):int(1.4*N/domain)] = 0.0
    h[int(1.4*N/domain):] = 1.0
    integral = np.sum(h) * dx
    if integral > 0:
        h = h / integral
    constructions['h_triangular'] = h
    
    return {"constructions": constructions, "num_constructions": 4}
