def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    def sigmoid_normalize(latent):
        h = 1.0 / (1.0 + np.exp(-latent))
        integral = np.sum(h) * dx
        if integral > 0:
            h = h / integral
        h = np.clip(h, 0.01, 1.0)
        h = h / np.sum(h) * (1.0 / dx)
        return h
    
    def compute_c5(h):
        j_val = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5 = np.max(correlation * dx)
        return c5
    
    # Candidate 1: Golomb-7
    marks1 = np.array([0.0, 0.333, 0.666, 1.0, 1.333, 1.666, 1.999])
    latent1 = np.zeros(N)
    for m in marks1:
        w = N * 0.08
        idx = np.clip(np.round(m * N).astype(int), 0, N-1)
        latent1[idx] = 4.0
    latent1 = latent1 - 2.0
    h1 = sigmoid_normalize(latent1)
    c5_1 = compute_c5(h1)
    
    # Candidate 2: Tri-modal-3
    peaks2 = np.array([0.3, 1.0, 1.7])
    latent2 = np.zeros(N)
    for p in peaks2:
        center_idx = np.clip(np.round(p * N).astype(int), 0, N-1)
        start = max(0, center_idx - 30)
        end = min(N, center_idx + 30)
        latent2[start:end] = 5.0
    latent2 = latent2 - 3.0
    h2 = sigmoid_normalize(latent2)
    c5_2 = compute_c5(h2)
    
    # Candidate 3: Bipartite-var
    a3 = 0.45
    idx_cut3 = int(a3 * N)
    latent3 = np.where(np.arange(N) < idx_cut3, 4.0, -2.0)
    h3 = sigmoid_normalize(latent3)
    c5_3 = compute_c5(h3)
    
    # Candidate 4: Multi-peak-4
    peaks4 = np.array([0.25, 0.65, 1.05, 1.45])
    latent4 = np.zeros(N)
    for p in peaks4:
        center_idx4 = np.clip(np.round(p * N).astype(int), 0, N-1)
        latent4[center_idx4 - 20: center_idx4 + 20] = 4.5
    latent4 = latent4 - 2.5
    h4 = sigmoid_normalize(latent4)
    c5_4 = compute_c5(h4)
    
    # Candidate 5: Golomb-5-shifted
    marks5 = np.array([0.1, 0.5, 0.9, 1.3, 1.7])
    latent5 = np.zeros(N)
    for m in marks5:
        w = N * 0.08
        idx = np.clip(np.round(m * N).astype(int), 0, N-1)
        latent5[idx] = 4.0
    latent5 = latent5 - 2.0
    h5 = sigmoid_normalize(latent5)
    c5_5 = compute_c5(h5)
    
    candidates = [
        {"h": h1.tolist(), "pattern_type": "golomb_7", "integral": float(np.sum(h1) * dx), "c5_bound": float(c5_1)},
        {"h": h2.tolist(), "pattern_type": "tri_modal_3", "integral": float(np.sum(h2) * dx), "c5_bound": float(c5_2)},
        {"h": h3.tolist(), "pattern_type": "bipartite_var", "integral": float(np.sum(h3) * dx), "c5_bound": float(c5_3)},
        {"h": h4.tolist(), "pattern_type": "multi_peak_4", "integral": float(np.sum(h4) * dx), "c5_bound": float(c5_4)},
        {"h": h5.tolist(), "pattern_type": "golomb_5_shifted", "integral": float(np.sum(h5) * dx), "c5_bound": float(c5_5)}
    ]
    return {"candidates": candidates, "num_candidates": 5}
