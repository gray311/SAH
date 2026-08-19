def run(ctx, args):
    import numpy as np
    N = 400  # Small intervals for fast evaluation (5x faster than N=800)
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
        return h / integral if integral > 0 else h
    
    def generate_pattern(name, seed, center_h=1.0, width=0.2, offset=0.0):
        np.random.seed(seed)
        h = np.zeros(N)
        if name.startswith("bipartite"):
            a = offset + np.random.rand() * (1.0 - 2*offset)
            h = np.where(np.linspace(0, 2, N) < a, 3.0, -3.0)
        elif name.startswith("tri_modal"):
            centers = [center_h + np.random.rand()*0.2, 
                     center_h + np.random.rand()*0.2 + 0.5,
                     center_h + np.random.rand()*0.2 + 1.0]
            for c in centers:
                mask = np.abs(np.linspace(0, 2, N) - c) < width
                h[mask] += 8.0
        elif name.startswith("golomb"):
            marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
            for m in marks:
                mask = np.abs(np.linspace(0, 2, N) - m) < width
                h[mask] += 6.0
        elif name.startswith("random"):
            latent = np.random.normal(0, 1.5, N)
            latent += offset + np.random.rand() * 4.0
            h = 1.0 / (1.0 + np.exp(-latent))
        else:
            latent = np.random.normal(0, 1.0, N) + offset
            h = 1.0 / (1.0 + np.exp(-latent))
        h = np.clip(h, 0.001, 10.0)
        h = normalize(h)
        return h, compute_c5(h)
    
    np.random.seed(42)
    temperature = args.get("temperature", 0.7)
    seed_start = args.get("seed_start", 42)
    np.random.seed(int(seed_start) + int(temperature * 1000))
    
    candidates = []
    
    # Pattern 1: Bipartite (4 variants)
    for i in range(4):
        name = f"bipartite_{i}"
        h, c5 = generate_pattern(name, seed_start + i, center_h=1.0, width=0.15, offset=0.0)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                         "c5_bound": float(c5), "pattern_type": name})
    
    # Pattern 2: Tri-modal (4 variants)
    for i in range(4):
        name = f"tri_modal_{i}"
        h, c5 = generate_pattern(name, seed_start + 10 + i, center_h=1.0, width=0.12, offset=0.0)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                         "c5_bound": float(c5), "pattern_type": name})
    
    # Pattern 3: Golomb ruler-like (2 variants)
    for i in range(2):
        name = f"golomb_{i}"
        h, c5 = generate_pattern(name, seed_start + 20 + i, center_h=0.5, width=0.18, offset=0.0)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                         "c5_bound": float(c5), "pattern_type": name})
    
    # Pattern 4: Random (2 variants)
    for i in range(2):
        name = f"random_{i}"
        h, c5 = generate_pattern(name, seed_start + 30 + i, center_h=1.0, width=0.0, offset=0.0)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx),
                         "c5_bound": float(c5), "pattern_type": name})
    
    # Add temperature-based noise to all
    if temperature > 0.5:
        noise_scale = 0.3 + temperature * 0.5
        for cand in candidates:
            h_arr = np.array(cand["h"])
            noise = np.random.normal(0, noise_scale, N)
            h_arr = (np.clip(1.0 / (1.0 + np.exp(-h_arr)), 0.001, 5.0) + noise)
            h_arr = np.clip(h_arr, 0.001, 10.0)
            cand["h"] = h_arr.tolist()
            cand["integral"] = float(np.sum(h_arr) * dx)
            cand["h"] = normalize(h_arr).tolist()
            cand["c5_bound"] = float(compute_c5(h_arr))
    
    return {"candidates": candidates, "num_candidates": len(candidates),
            "N_used": N, "dx": float(dx)}