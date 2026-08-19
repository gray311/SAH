def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    seed = args.get("seed", 42)
    np.random.seed(seed)
    
    def norm(h):
        """Normalize to integral=1."""
        integral = np.sum(h) * dx
        return h / integral if integral > 0 else h
    
    def clamp_to_01(h):
        """Clamp to [0.001, 1.0] then renormalize."""
        h = np.clip(h, 0.001, 1.0)
        h = norm(h)
        h = np.clip(h, 0.001, 1.0)
        return h
    
    def compute_c5(h_arr):
        """Compute c5_bound via FFT."""
        j_val = 1.0 - h_arr
        h_padded = np.pad(h_arr, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5 = np.max(correlation * dx)
        return float(c5)
    
    candidates = []
    
    # Pattern 1: 5 Gaussians
    h1 = np.zeros(N)
    centers = np.array([0.5, 1.5, 0.8, 1.2, 1.0]) * N
    bw = 3
    for c in centers:
        h1 += 20.0 * np.exp(-0.5 * ((np.arange(N) - c) / bw)**2)
    h1 = clamp_to_01(h1)
    c5_1 = compute_c5(h1)
    candidates.append({"h": h1.tolist(), "integral": 1.0, "c5_bound": c5_1, "pattern": "gauss_5"})
    
    # Pattern 2: 4 Gaussians
    h2 = np.zeros(N)
    centers = np.array([0.25, 0.75, 1.25, 1.75]) * N
    bw = 3
    for c in centers:
        h2 += 20.0 * np.exp(-0.5 * ((np.arange(N) - c) / bw)**2)
    h2 = clamp_to_01(h2)
    c5_2 = compute_c5(h2)
    candidates.append({"h": h2.tolist(), "integral": 1.0, "c5_bound": c5_2, "pattern": "gauss_4"})
    
    # Pattern 3: Uniform on [0,1]
    h3 = np.zeros(N)
    h3[:int(N/2)] = 1.0 / (N/2 * dx)  # integral=1 on [0,1]
    h3 = clamp_to_01(h3)
    c5_3 = compute_c5(h3)
    candidates.append({"h": h3.tolist(), "integral": 1.0, "c5_bound": c5_3, "pattern": "uniform_half"})
    
    # Pattern 4: Three Gaussians
    h4 = np.zeros(N)
    centers = np.array([0.4, 1.0, 1.6]) * N
    bw = 2
    for c in centers:
        h4 += 15.0 * np.exp(-0.5 * ((np.arange(N) - c) / bw)**2)
    h4 = clamp_to_01(h4)
    c5_4 = compute_c5(h4)
    candidates.append({"h": h4.tolist(), "integral": 1.0, "c5_bound": c5_4, "pattern": "gauss_3"})
    
    # Pattern 5: Concentrated at 0.8
    h5 = np.zeros(N)
    c = 0.8 * N
    h5[int(c)-2:int(c)+3] = 5.0
    h5 = clamp_to_01(h5)
    c5_5 = compute_c5(h5)
    candidates.append({"h": h5.tolist(), "integral": 1.0, "c5_bound": c5_5, "pattern": "concentrated"})
    
    # Return sorted by c5_bound
    candidates.sort(key=lambda x: x["c5_bound"])
    return {"candidates": candidates, "num_candidates": len(candidates)}