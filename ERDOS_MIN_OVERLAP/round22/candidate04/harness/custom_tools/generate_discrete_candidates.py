def run(ctx, args):
    import numpy as np
    domain = 2.0
    dx = domain / 50
    def compute_c5(h, N):
        j_val = 1.0 - h
        h_pad = np.pad(h, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad := np.pad(1.0-h, (0, N))))).real
        return float(np.max(corr * dx))
    def normalize(h): return h / float(np.sum(h) * dx)
    candidates = []
    for N_int in [30, 50, 70]:
        dx_int = domain / N_int
        # Bipartite
        for seed in range(10):
            np.random.seed(seed)
            h = np.zeros(N_int); m = N_int // 4
            h[:m] = 2.0; h[m:] = 0.0
            h = normalize(h)
            candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx_int),
                "c5_bound": compute_c5(h, N_int), "pattern": "bipartite", "N": N_int})
        # Tri-modal
        for seed in range(10):
            np.random.seed(seed)
            peaks = [0.2+np.random.rand()*0.4, 0.6+np.random.rand()*0.4, 1.0+np.random.rand()*0.4]
            peaks = [max(0.1, min(1.9, p)) for p in peaks]
            h = np.zeros(N_int)
            for p in peaks:
                h += 5.0 * np.exp(-((np.linspace(0, 2, N_int) - p) / 0.2)**2)
            h = normalize(np.clip(h, 0.01, 5.0))
            candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx_int),
                "c5_bound": compute_c5(h, N_int), "pattern": "tri_modal", "N": N_int, "peaks": peaks})
    return {"candidates": candidates, "num_candidates": len(candidates)}