def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N

    def sigmoid_normalize(latent):
        h = 1.0 / (1.0 + np.exp(-latent))
        integral = np.sum(h) * dx
        if integral > 0 and integral < 2.0:
            h = h / integral
        h = np.clip(h, 0.001, 0.999)
        integral = np.sum(h) * dx
        return h

    # Golomb-4 pattern (4 marks)
    golomb4_latent = np.zeros(N)
    marks = np.array([0.0, 0.4, 0.8, 1.2])
    for m in marks:
        idx = int(np.round(m * N))
        if 0 <= idx < N:
            golomb4_latent[idx] = 5.0
    golomb4_latent -= 2.0
    golomb4_h = sigmoid_normalize(golomb4_latent)
    j = 1.0 - golomb4_h
    h_pad = np.pad(golomb4_h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.fft(h_pad) * np.fft.fft(j_pad).real
    golomb4_c5 = np.max(corr) * dx

    # Golomb-5 pattern (5 marks)
    golomb5_latent = np.zeros(N)
    marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
    for m in marks:
        idx = int(np.round(m * N))
        if 0 <= idx < N:
            golomb5_latent[idx] = 5.0
    golomb5_latent -= 2.0
    golomb5_h = sigmoid_normalize(golomb5_latent)
    j = 1.0 - golomb5_h
    h_pad = np.pad(golomb5_h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.fft(h_pad) * np.fft.fft(j_pad).real
    golomb5_c5 = np.max(corr) * dx

    # Tri-modal-3 pattern
    tri_latent = np.zeros(N)
    peaks = [0.4, 1.0, 1.6]
    for p in peaks:
        idx = int(np.round(p * N))
        start = max(0, idx - 5)
        end = min(N, idx + 6)
        tri_latent[start:end] = 4.0
    tri_latent -= 2.0
    tri_h = sigmoid_normalize(tri_latent)
    j = 1.0 - tri_h
    h_pad = np.pad(tri_h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.fft(h_pad) * np.fft.fft(j_pad).real
    tri_c5 = np.max(corr) * dx

    # Bipartite pattern
    bip_latent = np.zeros(N)
    split_idx = int(0.5 * N)
    bip_latent[:split_idx] = 4.0
    bip_latent[split_idx:] = -2.0
    bip_h = sigmoid_normalize(bip_latent)
    j = 1.0 - bip_h
    h_pad = np.pad(bip_h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.fft(h_pad) * np.fft.fft(j_pad).real
    bip_c5 = np.max(corr) * dx

    candidates = [
        {"h": golomb4_h.tolist(), "integral": float(np.sum(golomb4_h)*dx), "c5_bound": float(golomb4_c5), "pattern": "golomb4"},
        {"h": golomb5_h.tolist(), "integral": float(np.sum(golomb5_h)*dx), "c5_bound": float(golomb5_c5), "pattern": "golomb5"},
        {"h": tri_h.tolist(), "integral": float(np.sum(tri_h)*dx), "c5_bound": float(tri_c5), "pattern": "tri_modal"},
        {"h": bip_h.tolist(), "integral": float(np.sum(bip_h)*dx), "c5_bound": float(bip_c5), "pattern": "bipartite"}
    ]
    return {"candidates": candidates, "num_candidates": 4}