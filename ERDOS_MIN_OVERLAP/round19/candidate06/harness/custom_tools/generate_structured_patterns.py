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
        if integral < 0.001 or integral > 10.0:
            return h
        return h / integral
    
    ptype = args.get("pattern_type", "golomb_5")
    
    candidates = []
    
    if ptype == "golomb_5":
        marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
        h = np.zeros(N)
        for m in marks:
            h += 8.0 * np.exp(-((np.abs(np.arange(N) * dx - m)) / 0.15)**2)
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "golomb_5"})
    
    elif ptype == "golomb_7":
        marks = np.array([0.0, 1.0/6.0, 2.0/6.0, 3.0/6.0, 4.0/6.0, 5.0/6.0, 1.0])
        h = np.zeros(N)
        for m in marks:
            h += 6.0 * np.exp(-((np.abs(np.arange(N) * dx - m)) / 0.12)**2)
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "golomb_7"})
    
    elif ptype == "bipartite":
        x = np.arange(N) * dx
        a = 1.0 + np.random.rand() * 0.1
        h = np.where(x < a, 4.0, -2.0)
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "bipartite"})
    
    elif ptype == "tri_modal":
        x = np.arange(N) * dx
        peaks = np.array([0.4, 1.0, 1.6])
        h = np.zeros(N)
        for p in peaks:
            h += 8.0 * np.exp(-((np.abs(x - p)) / 0.12)**2)
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "tri_modal"})
    
    elif ptype == "bi_modal":
        x = np.arange(N) * dx
        peaks = np.array([0.6, 1.4])
        h = np.zeros(N)
        for p in peaks:
            h += 10.0 * np.exp(-((np.abs(x - p)) / 0.08)**2)
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "bi_modal"})
    
    elif ptype == "sparse_4":
        x = np.arange(N) * dx
        peaks = np.array([0.25, 0.75, 1.25, 1.75])
        h = np.zeros(N)
        for p in peaks:
            h += 6.0 * np.exp(-((np.abs(x - p)) / 0.1)**2)
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "sparse_4"})
    
    elif ptype == "uniform":
        h = np.ones(N) * 0.5
        h = normalize(h)
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "uniform"})
    
    elif ptype == "step":
        x = np.arange(N) * dx
        h = np.where(x < 1.0, 2.0, 0.0)
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "step"})
    
    elif ptype == "sinusoidal":
        x = np.arange(N) * dx
        latent = 0.5 + 0.3 * np.sin(2 * np.pi * x) + 0.1 * np.cos(4 * np.pi * x)
        h = np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 1.0)
        h = normalize(h)
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "sinusoidal"})
    
    elif ptype == "piecewise_5":
        x = np.arange(N) * dx
        h = np.zeros(N)
        h[0:N//5] = 2.0
        h[N//5:2*N//5] = 0.0
        h[2*N//5:3*N//5] = 1.5
        h[3*N//5:4*N//5] = 0.0
        h[4*N//5:] = 0.5
        h = normalize(h)
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "piecewise_5"})
    
    elif ptype == "threshold_3":
        x = np.arange(N) * dx
        h = np.zeros(N)
        h[x < 0.3] = 3.5
        h[(x >= 0.3) & (x < 0.7)] = 0.0
        h[(x >= 0.7) & (x < 1.0)] = 3.0
        h[(x >= 1.0) & (x < 1.5)] = 0.0
        h[x >= 1.5] = 2.0
        h = normalize(h)
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "threshold_3"})
    
    elif ptype == "multi_scale":
        x = np.arange(N) * dx
        h = np.zeros(N)
        h += 2.0 * np.exp(-((x - 1.0)**2) / 0.5)  # broad
        h += 5.0 * np.exp(-((x - 0.5)**2) / 0.05)  # narrow
        h += 5.0 * np.exp(-((x - 1.5)**2) / 0.05)  # narrow
        h = normalize(np.clip(h, 0.001, 10.0))
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": "multi_scale"})
    
    return {"candidates": candidates, "num_candidates": len(candidates), "pattern_type": ptype}
