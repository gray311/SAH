def run(ctx, args):
    import numpy as np
    N = 150
    domain = 2.0
    dx = domain / N

    def compute_c5(h):
        h_clipped = np.clip(h, 0.001, 0.999)
        j_val = 1.0 - h_clipped
        h_padded = np.pad(h_clipped, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        return float(np.max(correlation * dx))

    def normalize(h):
        integral = np.sum(h) * dx
        if integral < 0.001:
            return h, 1.0
        return h / integral, integral

    candidates = []

    # Pattern 1: Bipartite - random split
    np.random.seed(42)
    x = np.linspace(0, 2, N)
    a = 0.4 + np.random.rand() * 0.2
    h = np.where(x < a, 2.5, -2.5)
    h, integral = normalize(h)
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(integral), "c5_bound": float(c5), "pattern_type": "bipartite"})

    # Pattern 2: Tri-modal - 3 random peaks
    np.random.seed(123)
    h = np.zeros(N)
    peaks = [0.3 + np.random.rand()*0.3, 0.9 + np.random.rand()*0.2, 1.4 + np.random.rand()*0.2]
    for p in peaks:
        h += 4.0 * np.exp(-((x - p) / 0.12)**2)
    h, integral = normalize(h)
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(integral), "c5_bound": float(c5), "pattern_type": "tri_modal"})

    # Pattern 3: Golomb ruler
    np.random.seed(456)
    h = np.zeros(N)
    marks = [0.0, 0.4, 0.8, 1.2, 1.6]
    for m in marks:
        h += 6.0 * np.exp(-((x - m) / 0.18)**2)
    h, integral = normalize(h)
    c5 = compute_c5(h)
    candidates.append({"h": h.tolist(), "integral": float(integral), "c5_bound": float(c5), "pattern_type": "golomb"})

    # Patterns 4-12: Random seeds
    for seed_num in range(4, 13):
        np.random.seed(seed_num)
        latent = np.random.normal(0, 1.0, N)
        h = normalize(np.clip(1.0 / (1.0 + np.exp(-latent)), 0.001, 0.999))[0]
        c5 = compute_c5(h)
        candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5), "pattern_type": f"random_{seed_num}"})

    return {"candidates": candidates, "num_candidates": len(candidates)}