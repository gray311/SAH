def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    def sigmoid_scale(h_latent):
        h = 1.0 / (1.0 + np.exp(-h_latent))
        total = np.sum(h) * dx
        if total < 1e-6:
            return h, 1.0
        h = h / total
        return np.clip(h, 0.001, 1.0), np.sum(h) * dx
    
    def compute_c5(h):
        j_val = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        return np.max(correlation * dx)
    
    def generate_golomb(variant, marks_base):
        marks = marks_base + [marks_base[0] + 0.3 * variant] if variant < 2 else marks_base
        h = np.zeros(N)
        for m in marks:
            idx = int(m * N)
            width = int(N * 0.15)
            mask = np.abs(np.arange(N) - idx) < width
            h[mask] = 6.0 + np.random.normal(0, 0.5)
        h, integral = sigmoid_scale(h)
        c5 = compute_c5(h)
        return {"h": h.tolist(), "integral": float(integral), "c5_bound": float(c5), "pattern": f"golomb_v{variant}"}
    
    def generate_bipartite(variant, split):
        a = 0.3 + 0.05 * variant if variant < 5 else 0.4
        h = np.zeros(N)
        h[:int(N * a)] = 4.0 + np.random.normal(0, 0.3)
        h[int(N * a):] = -2.0 + np.random.normal(0, 0.3)
        h, integral = sigmoid_scale(h)
        c5 = compute_c5(h)
        return {"h": h.tolist(), "integral": float(integral), "c5_bound": float(c5), "pattern": f"bipartite_a{a:.2f}"}
    
    def generate_trimodal(variant, peaks_base):
        peaks = peaks_base + [peaks_base[0] + 0.1 * variant] if variant < 2 else peaks_base
        h = np.zeros(N)
        for p in peaks:
            idx = int(p * N)
            width = int(N * 0.1)
            mask = np.abs(np.arange(N) - idx) < width
            h[mask] = 5.0 + np.random.normal(0, 0.4)
        h, integral = sigmoid_scale(h)
        c5 = compute_c5(h)
        return {"h": h.tolist(), "integral": float(integral), "c5_bound": float(c5), "pattern": f"trimodal_peaks{peaks}"}
    
    candidates = []
    for v in range(3):
        if v == 0:
            candidates.append(generate_golomb(v, [0.0, 0.4, 0.8, 1.2, 1.6]))
        elif v == 1:
            candidates.append(generate_golomb(v, [0.0, 0.5, 1.0, 1.5]))
        else:
            candidates.append(generate_golomb(v, [0.0, 0.3, 0.6, 0.9, 1.2]))
    for v in range(3):
        candidates.append(generate_bipartite(v, [0.3 + 0.05 * v]))
    for v in range(3):
        peaks = [0.4, 1.0, 1.6]
        if v == 1:
            peaks = [0.3, 1.0, 1.7]
        elif v == 2:
            peaks = [0.2, 0.8, 1.4]
        candidates.append(generate_trimodal(v, peaks))
    candidates.append(generate_trimodal(3, [0.5, 1.5]))
    
    candidates.sort(key=lambda x: x["c5_bound"])
    top10 = candidates[:10]
    return {"candidates": top10, "num_candidates": 10}
