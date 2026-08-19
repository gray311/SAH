def run(ctx, args):
    import numpy as np
    temp = args.get("temperature", 0.7)
    N = 800
    domain = 2.0
    dx = domain / N

    rng = np.random.RandomState(int(temp * 12345))

    def normalize_to_integral_one(h_raw):
        h = 1.0 / (1.0 + np.exp(-h_raw))
        total = np.sum(h) * dx
        if total < 1e-6:
            return h
        h = h / total
        h = np.clip(h, 0.001, 1.0)
        total_after = np.sum(h) * dx
        h = h / total_after
        return np.clip(h, 0.001, 1.0)

    def compute_c5(h):
        j_val = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        return float(np.max(correlation * dx))

    candidates = []

    golomb_5 = np.zeros(N)
    marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
    for m in marks:
        idx = int(m * N)
        width = N * 0.06
        start = max(0, idx - 5)
        end = min(N, idx + 6)
        local_idx = np.arange(start, end)
        offsets = local_idx - idx
        golomb_5[start:end] += 8.0 * np.exp(-((offsets / width)**2))
    h1 = normalize_to_integral_one(golomb_5)
    c5_1 = compute_c5(h1)

    golomb_4 = np.zeros(N)
    marks = np.array([0.0, 0.5, 1.0, 1.5])
    for m in marks:
        idx = int(m * N)
        width = N * 0.08
        start = max(0, idx - 6)
        end = min(N, idx + 7)
        local_idx = np.arange(start, end)
        offsets = local_idx - idx
        golomb_4[start:end] += 10.0 * np.exp(-((offsets / width)**2))
    h2 = normalize_to_integral_one(golomb_4)
    c5_2 = compute_c5(h2)

    bipartite = np.zeros(N)
    split_idx = int(0.45 * N)
    bipartite[:split_idx] = 5.0
    bipartite[split_idx:] = -2.0
    h3 = normalize_to_integral_one(bipartite)
    c5_3 = compute_c5(h3)

    cands = [
        {"h": h1.tolist(), "integral": float(np.sum(h1)*dx), "c5_bound": c5_1, "pattern_type": "golomb_5"},
        {"h": h2.tolist(), "integral": float(np.sum(h2)*dx), "c5_bound": c5_2, "pattern_type": "golomb_4"},
        {"h": h3.tolist(), "integral": float(np.sum(h3)*dx), "c5_bound": c5_3, "pattern_type": "bipartite_a045"}
    ]
    return {"candidates": cands, "num_candidates": 3, "temperature": temp}