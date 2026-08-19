def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    def compute_c5(h):
        j_val = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        return np.max(correlation * dx)
    
    def normalize(h):
        integral = np.sum(h) * dx
        return h / integral
    
    candidates = []
    
    # Pattern: Golomb ruler with fixed marks
    np.random.seed(42)
    marks = [0.0, 0.4, 0.8, 1.2, 1.6]
    golomb_h = np.zeros(N)
    for m in marks:
        golomb_h += 8.0 * np.exp(-((np.linspace(0, 2, N) - m) / 0.15)**2)
    golomb_h = normalize(np.clip(golomb_h, 0.001, 5.0))
    c5 = compute_c5(golomb_h)
    candidates.append({"h": golomb_h.tolist(), "integral": float(np.sum(golomb_h) * dx),
                     "c5_bound": float(c5), "pattern_type": "golomb_fixed"})
    
    # Pattern: Bipartite with random split
    np.random.seed(123)
    x = np.linspace(0, 2, N)
    a = 0.5 + np.random.rand() * 0.2
    bipartite_h = np.where(x < a, 3.0, -3.0)
    bipartite_h = bipartite_h + np.random.normal(0, 0.3, N)
    bipartite_h = normalize(np.clip(1.0 / (1.0 + np.exp(-bipartite_h)), 0.001, 1.0))
    c5 = compute_c5(bipartite_h)
    candidates.append({"h": bipartite_h.tolist(), "integral": float(np.sum(bipartite_h) * dx),
                     "c5_bound": float(c5), "pattern_type": "bipartite_rand"})
    
    # Pattern: Tri-modal with random peaks
    np.random.seed(456)
    x = np.linspace(0, 2, N)
    peaks = [0.4 + np.random.rand()*0.1, 1.0 + np.random.rand()*0.05, 1.6 + np.random.rand()*0.1]
    peaks = [max(0.1, min(1.9, p)) for p in peaks]
    tri_h = np.zeros(N)
    for p in peaks:
        tri_h += 6.0 * np.exp(-((x - p) / 0.15)**2)
    tri_h = normalize(np.clip(tri_h, 0.001, 5.0))
    c5 = compute_c5(tri_h)
    candidates.append({"h": tri_h.tolist(), "integral": float(np.sum(tri_h) * dx),
                     "c5_bound": float(c5), "pattern_type": "tri_modal_rand"})
    
    # Pattern: Random seed 1
    np.random.seed(789)
    latent = np.random.normal(0, 1.0, N)
    h = normalize(np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0))
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                     "c5_bound": float(c5), "pattern_type": "random_seed1"})
    
    return {"candidates": candidates, "num_candidates": len(candidates)}