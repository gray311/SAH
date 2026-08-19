def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    # Pattern 1: Uniform split - h=0.5 everywhere (integral = 0.5*2 = 1)
    h_uniform = np.full(N, 0.5)
    
    # Pattern 2: Bipartite - h=1 on [0,1), h=0 on [1,2)
    h_bipartite = np.where(np.arange(N) < N/2, 1.0, 0.0)
    
    # Pattern 3: Symmetric bimodal - two peaks at 0.5 and 1.5
    h_bimodal = np.zeros(N)
    for center in [N*0.5, N*1.5]:
        width = int(N * 0.2)
        h_bimodal[int(center-width):int(center+width)] = 1.0/width * N * dx
    
    # Pattern 4: Triangular - rise then fall
    h_tri = np.zeros(N)
    peak_idx = int(N * 1.0)
    for i in range(peak_idx):
        h_tri[i] = 2.0 * (i + 1) / peak_idx
    for i in range(peak_idx, N):
        h_tri[i] = 2.0 * (N - i) / (N - peak_idx)
    
    # Pattern 5: Multi-step - 3 steps
    h_steps = np.zeros(N)
    h_steps[:int(N*0.3)] = 1.5  # [0, 0.6)
    h_steps[int(N*0.3):int(N*0.7)] = 0.5  # [0.6, 1.4)
    h_steps[int(N*0.7):] = 0.5  # [1.4, 2.0)
    
    # Normalize each to integral=1 exactly
    normalized = {}
    all_h = [h_uniform, h_bipartite, h_bimodal, h_tri, h_steps]
    for i, h in enumerate(all_h):
        integral = np.sum(h) * dx
        if integral > 0:
            h_norm = h / integral
        else:
            h_norm = h_uniform / (np.sum(h_uniform) * dx)
        normalized[f"pattern_{i}"] = h_norm
    
    return {"constructions": normalized, "num_constructions": 5}
