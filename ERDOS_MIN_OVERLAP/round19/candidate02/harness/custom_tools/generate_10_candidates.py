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
    
    np.random.seed(args.get('seed', 0))
    candidates = []
    
    # Patterns 0-3: Random-based
    for seed in [0, 1, 2, 3]:
        np.random.seed(seed)
        latent = np.random.normal(0, 1.2, N)
        h = np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0)
        h = normalize(h)
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                         "c5_bound": float(c5), "pattern": f"random_seed{seed}"})
    
    # Pattern 4: Golomb-like (optimal spacing)
    np.random.seed(4)
    x = np.linspace(0, 2, N)
    marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
    golomb = np.zeros(N)
    for m in marks:
        golomb += 6.0 * np.exp(-((x - m) / 0.12)**2)
    golomb = normalize(np.clip(golomb, 0.001, 5.0))
    c5 = compute_c5(golomb)
    candidates.append({"h": golomb.tolist(), "integral": float(np.sum(golomb) * dx),
                     "c5_bound": float(c5), "pattern": "golomb_optimal"})
    
    # Pattern 5: Bipartite
    np.random.seed(5)
    x = np.linspace(0, 2, N)
    a = 0.45
    bipartite = np.where(x < a, 4.0, -4.0)
    bipartite = bipartite + np.random.normal(0, 0.3, N)
    bipartite = normalize(np.clip(1.0 / (1.0 + np.exp(-bipartite)), 0.001, 1.0))
    c5 = compute_c5(bipartite)
    candidates.append({"h": bipartite.tolist(), "integral": float(np.sum(bipartite) * dx),
                     "c5_bound": float(c5), "pattern": "bipartite"})
    
    # Pattern 6: Tri-modal
    np.random.seed(6)
    x = np.linspace(0, 2, N)
    peaks = [0.35, 1.0, 1.65]
    tri = np.zeros(N)
    for p in peaks:
        tri += 5.0 * np.exp(-((x - p) / 0.1)**2)
    tri = normalize(np.clip(tri, 0.001, 5.0))
    c5 = compute_c5(tri)
    candidates.append({"h": tri.tolist(), "integral": float(np.sum(tri) * dx),
                     "c5_bound": float(c5), "pattern": "tri_modal"})
    
    # Pattern 7: Wave
    np.random.seed(7)
    x = np.linspace(0, 2, N)
    wave = 1.2 * np.sin(2 * np.pi * x) + 0.7 * np.cos(4 * np.pi * x)
    wave = normalize(np.clip(1.0 / (1.0 + np.exp(-wave)), 0.001, 1.0))
    c5 = compute_c5(wave)
    candidates.append({"h": wave.tolist(), "integral": float(np.sum(wave) * dx),
                     "c5_bound": float(c5), "pattern": "wave"})
    
    # Patterns 8-9: Threshold variations
    for t1, t2 in [(0.35, 0.65), (0.45, 0.55)]:
        np.random.seed(8 + len([p for p in candidates]))
        x = np.linspace(0, 2, N)
        latent = np.where(x < t1, 3.0, -3.0)
        latent = latent + np.random.normal(0, 0.4, N)
        h = normalize(np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                         "c5_bound": float(c5), "pattern": f"threshold_t1{t1}"})
    
    return {"candidates": candidates, "num_candidates": len(candidates)}
