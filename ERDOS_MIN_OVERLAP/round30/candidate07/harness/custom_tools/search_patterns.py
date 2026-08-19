def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    def compute_c5(h_arr):
        h_padded = np.pad(h_arr, (0, N))
        j_padded = np.pad(1.0 - h_arr, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
        return np.max(corr * dx)
    
    def normalize_and_clip(h_arr):
        h_norm = h_arr / (np.sum(h_arr) * dx)
        h_norm = np.clip(h_norm, 0.001, 1.0)
        h_norm = h_norm / (np.sum(h_norm) * dx)
        return h_norm
    
    # Pattern 1: Golomb ruler (4 marks at optimal spacing for C5)
    golomb_marks = np.array([0.0, 0.4, 1.0, 1.6])
    golomb_h = np.zeros(N)
    for mark in golomb_marks:
        width = N * 0.15
        golomb_h += 12.0 * np.exp(-((np.arange(N) - int(mark * N)) / width)**2)
    golomb_h = normalize_and_clip(golomb_h)
    golomb_c5 = compute_c5(golomb_h)
    
    # Pattern 2: Bipartite (threshold at a=0.55 for integral=1)
    bipartite_a = 0.55
    bipartite_raw = np.zeros(N)
    bipartite_raw[:int(N*bipartite_a)] = 4.0
    bipartite_raw[int(N*bipartite_a):] = -1.0
    bipartite_h = normalize_and_clip(bipartite_raw)
    bipartite_c5 = compute_c5(bipartite_h)
    
    # Pattern 3: Triangular (single peak at center)
    tri_width = N * 0.1
    tri_h = np.zeros(N)
    tri_h[400:int(400+tri_width)] = 20.0
    tri_h = normalize_and_clip(tri_h)
    tri_c5 = compute_c5(tri_h)
    
    # Pattern 4: Multi-peak (3 peaks at 0.4, 1.0, 1.6)
    multi_width = N * 0.1
    multi_h = np.zeros(N)
    for center in [0.4, 1.0, 1.6]:
        multi_h += 15.0 * np.exp(-((np.arange(N) - int(center * N)) / multi_width)**2)
    multi_h = normalize_and_clip(multi_h)
    multi_c5 = compute_c5(multi_h)
    
    # Pattern 5: Random-structured (Laplace distribution with mean 1.0)
    laplace_vals = -np.log(np.random.laplace(0.0, 1.0, N) + 1e-10)
    random_h = normalize_and_clip(laplace_vals)
    random_c5 = compute_c5(random_h)
    
    candidates = [
        {"h": golomb_h.tolist(), "integral": float(np.sum(golomb_h)*dx), "c5_bound": float(golomb_c5), "pattern_type": "golomb_4"},
        {"h": bipartite_h.tolist(), "integral": float(np.sum(bipartite_h)*dx), "c5_bound": float(bipartite_c5), "pattern_type": "bipartite"},
        {"h": tri_h.tolist(), "integral": float(np.sum(tri_h)*dx), "c5_bound": float(tri_c5), "pattern_type": "triangular"},
        {"h": multi_h.tolist(), "integral": float(np.sum(multi_h)*dx), "c5_bound": float(multi_c5), "pattern_type": "multi_peak"},
        {"h": random_h.tolist(), "integral": float(np.sum(random_h)*dx), "c5_bound": float(random_c5), "pattern_type": "laplace"}
    ]
    return {"candidates": candidates, "num_candidates": 5}
