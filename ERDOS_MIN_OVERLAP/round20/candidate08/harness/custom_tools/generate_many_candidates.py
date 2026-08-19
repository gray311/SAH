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
    
    # Pattern 0-7: Random-based patterns
    seeds = [0, 1, 2, 3, 4, 5, 6, 7]
    for i, seed in enumerate(seeds[:4]):
        np.random.seed(seed)
        latent = np.random.normal(0, 1.5, N)
        h = np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0)
        h = normalize(h)
        c5 = compute_c5(h)
        candidates.append({
            "h": h.tolist(),
            "integral": float(np.sum(h) * dx),
            "c5_bound": float(c5),
            "pattern_type": f"random_norm_seed{seed}"
        })
    
    # Pattern 8-11: Threshold patterns
    thresholds = [(0.4, 0.6), (0.5, 0.5), (0.6, 0.4), (0.3, 0.7)]
    for idx, (t1, t2) in enumerate(thresholds):
        np.random.seed(10 + idx)
        x = np.linspace(0, 2, N)
        latent = np.where(x < t1, 4.0, -4.0)
        latent = latent + np.random.normal(0, 0.5, N)
        h = np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0)
        h = normalize(h)
        c5 = compute_c5(h)
        candidates.append({
            "h": h.tolist(),
            "integral": float(np.sum(h) * dx),
            "c5_bound": float(c5),
            "pattern_type": f"threshold_t1{t1}_t2{t2}"
        })
    
    # Pattern 12: Bipartite
    np.random.seed(20)
    x = np.linspace(0, 2, N)
    a = 0.5 + 0.1 * np.random.rand()
    latent = np.where(x < a, 3.0, -3.0)
    latent = latent + np.random.normal(0, 0.3, N)
    h = np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0)
    h = normalize(h)
    c5 = compute_c5(h)
    candidates.append({
        "h": h.tolist(),
        "integral": float(np.sum(h) * dx),
            "c5_bound": float(c5),
        "pattern_type": "bipartite_var"
    })
    
    # Pattern 13: Tri-modal
    np.random.seed(30)
    x = np.linspace(0, 2, N)
    peaks = [0.4 + np.random.rand() * 0.2, 
             1.0 + np.random.rand() * 0.05, 
             1.6 + np.random.rand() * 0.2]
    peaks = [max(0.1, min(1.9, p)) for p in peaks]
    tri_h = np.zeros(N)
    for p in peaks:
        tri_h += 6.0 * np.exp(-((x - p) / 0.15)**2)
    tri_h = np.clip(tri_h, 0.001, 5.0)
    tri_h = normalize(tri_h)
    c5 = compute_c5(tri_h)
    candidates.append({
        "h": tri_h.tolist(),
        "integral": float(np.sum(tri_h) * dx),
            "c5_bound": float(c5),
        "pattern_type": "tri_modal_var"
    })
    
    # Pattern 14: Golomb-like
    np.random.seed(40)
    marks = [0.0, 0.45 + np.random.rand()*0.1, 1.0, 1.6, 2.0 - 0.1 - np.random.rand()*0.1]
    marks = [max(0.05, min(1.95, m)) for m in marks]
    golomb_h = np.zeros(N)
    for m in marks:
        golomb_h += 8.0 * np.exp(-((x - m) / 0.15)**2)
    golomb_h = normalize(np.clip(golomb_h, 0.001, 5.0))
    c5 = compute_c5(golomb_h)
    candidates.append({
        "h": golomb_h.tolist(),
        "integral": float(np.sum(golomb_h) * dx),
            "c5_bound": float(c5),
        "pattern_type": "golomb_var"
    })
    
    # Pattern 15: Wave pattern
    np.random.seed(50)
    x = np.linspace(0, 2, N)
    latent = np.sin(2 * np.pi * x) * 1.5 + np.cos(4 * np.pi * x) * 0.8
    latent = latent + np.random.normal(0, 0.4, N)
    h = np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0)
    h = normalize(h)
    c5 = compute_c5(h)
    candidates.append({
        "h": h.tolist(),
        "integral": float(np.sum(h) * dx),
            "c5_bound": float(c5),
        "pattern_type": "wave_var"
    })
    
    return {"candidates": candidates, "num_candidates": len(candidates)}