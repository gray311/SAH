def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    seed = args.get("seed", 42)
    np.random.seed(seed)
    
    candidates = []
    
    # Pattern 1: Gaussian peaks at 0.5 and 1.5
    g1 = np.zeros(N)
    for center in [0.5 * N, 1.5 * N]:
        std = N * 0.04
        g1 += np.exp(-0.5 * ((np.arange(N) - center) / std)**2)
    g1 = np.clip(g1, 1e-6, 100)
    g1 = np.exp(g1) / (np.sum(np.exp(g1)) + 1e-10)
    g1 = g1 / (np.sum(g1) * dx)
    g1 = np.clip(g1, 1e-4, 1.0)
    j1 = 1.0 - g1
    corr = np.fft.fft(g1) * np.conj(np.fft.fft(j1))
    c5 = np.max(np.fft.ifft(corr).real * dx)
    candidates.append({"h": g1.tolist(), "c5_bound": float(c5), "pattern": "gaussian_2peaks"})
    
    # Pattern 2: Sparse spikes (3 high regions)
    s2 = np.zeros(N)
    for mark in [N/3, N/2, 2*N/3]:
        width = N * 0.025
        s2 += 20.0 * np.exp(-((np.arange(N) - mark) / width)**2)
    s2 = np.clip(s2, 1e-6, 100)
    s2 = np.exp(s2) / (np.sum(np.exp(s2)) + 1e-10)
    s2 = s2 / (np.sum(s2) * dx)
    s2 = np.clip(s2, 1e-4, 1.0)
    j2 = 1.0 - s2
    corr = np.fft.fft(s2) * np.conj(np.fft.fft(j2))
    c5 = np.max(np.fft.ifft(corr).real * dx)
    candidates.append({"h": s2.tolist(), "c5_bound": float(c5), "pattern": "sparse_3spikes"})
    
    # Pattern 3: Triangular (single peak at center)
    t3 = np.zeros(N)
    peak = N / 2
    for i in range(N):
        t3[i] = 1.0 - abs(i - peak) / (N / 2)
    t3 = np.maximum(t3, 0.1)
    t3 = np.exp(t3) / (np.sum(np.exp(t3)) + 1e-10)
    t3 = t3 / (np.sum(t3) * dx)
    t3 = np.clip(t3, 1e-4, 1.0)
    j3 = 1.0 - t3
    corr = np.fft.fft(t3) * np.conj(np.fft.fft(j3))
    c5 = np.max(np.fft.ifft(corr).real * dx)
    candidates.append({"h": t3.tolist(), "c5_bound": float(c5), "pattern": "triangular"})
    
    # Pattern 4: Asymmetric bimodal (high on left, low on right)
    a4 = np.zeros(N)
    split = N * 0.7
    a4[:int(split)] = 10.0
    a4[int(split):] = 0.5
    a4 = np.clip(a4, 1e-6, 100)
    a4 = np.exp(a4) / (np.sum(np.exp(a4)) + 1e-10)
    a4 = a4 / (np.sum(a4) * dx)
    a4 = np.clip(a4, 1e-4, 1.0)
    j4 = 1.0 - a4
    corr = np.fft.fft(a4) * np.conj(np.fft.fft(j4))
    c5 = np.max(np.fft.ifft(corr).real * dx)
    candidates.append({"h": a4.tolist(), "c5_bound": float(c5), "pattern": "asymmetric_bimodal"})
    
    # Pattern 5: Multi-modal (4 narrow peaks)
    m5 = np.zeros(N)
    for center in [N * 0.25, N * 0.5, N * 0.75, N]:
        width = N * 0.02
        m5 += 25.0 * np.exp(-((np.arange(N) - center) / width)**2)
    m5 = np.clip(m5, 1e-6, 100)
    m5 = np.exp(m5) / (np.sum(np.exp(m5)) + 1e-10)
    m5 = m5 / (np.sum(m5) * dx)
    m5 = np.clip(m5, 1e-4, 1.0)
    j5 = 1.0 - m5
    corr = np.fft.fft(m5) * np.conj(np.fft.fft(j5))
    c5 = np.max(np.fft.ifft(corr).real * dx)
    candidates.append({"h": m5.tolist(), "c5_bound": float(c5), "pattern": "quad_modal"})
    
    return {"candidates": candidates, "num_candidates": len(candidates), "patterns": [c["pattern"] for c in candidates]}
