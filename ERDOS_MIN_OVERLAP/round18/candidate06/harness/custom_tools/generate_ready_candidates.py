def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N

    # Candidate 1: Golomb ruler pattern
    golomb_marks = np.array([0.0, 0.45, 1.2, 1.8])
    golomb_h = np.zeros(N)
    for mark in golomb_marks:
        width = N * 0.08
        golomb_h += 8.0 * np.exp(-((np.arange(N) - int(mark * N)) / width)**2)
    golomb_h = np.clip(golomb_h, 0, 5)
    golomb_h = np.exp(golomb_h) / (np.sum(np.exp(golomb_h)) + 1e-10)
    golomb_integral = np.sum(golomb_h) * dx
    golomb_h = golomb_h / golomb_integral
    golomb_h = np.clip(golomb_h, 0.001, 1.0)
    golomb_h = golomb_h / np.sum(golomb_h) * (1.0/dx)
    golomb_h = np.clip(golomb_h, 0.001, 1.0)
    golomb_h = golomb_h / (np.sum(golomb_h) * dx)
    golomb_c5 = 0.0
    j_golomb = 1.0 - golomb_h
    h_padded = np.pad(golomb_h, (0, N))
    j_padded = np.pad(j_golomb, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    golomb_c5 = np.max(correlation * dx)

    # Candidate 2: Bipartite pattern
    bipartite_h = np.zeros(N)
    a = 0.55
    bipartite_h[:int(N*a)] = 4.0
    bipartite_h[int(N*a):int(N*(2-a))] = -1.0
    bipartite_h[int(N*(2-a)):] = 3.0
    bipartite_h = np.clip(bipartite_h, 0.01, 5.0)
    bipartite_h = np.exp(bipartite_h) / (np.sum(np.exp(bipartite_h)) + 1e-10)
    bipartite_integral = np.sum(bipartite_h) * dx
    bipartite_h = bipartite_h / bipartite_integral
    bipartite_h = np.clip(bipartite_h, 0.01, 1.0)
    bipartite_h = bipartite_h / np.sum(bipartite_h) * (1.0/dx)
    bipartite_h = np.clip(bipartite_h, 0.01, 1.0)
    bipartite_h = bipartite_h / (np.sum(bipartite_h) * dx)
    bipartite_c5 = 0.0
    j_bipartite = 1.0 - bipartite_h
    h_padded = np.pad(bipartite_h, (0, N))
    j_padded = np.pad(j_bipartite, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    bipartite_c5 = np.max(correlation * dx)

    # Candidate 3: Tri-modal
    tri_h = np.zeros(N)
    peaks = [0.4, 1.0, 1.6]
    bw = 0.06
    for p in peaks:
        tri_h += 6.0 * np.exp(-((np.arange(N) - int(p * N)) / (N * bw))**2)
    tri_h = np.clip(tri_h, 0.01, 5.0)
    tri_h = np.exp(tri_h) / (np.sum(np.exp(tri_h)) + 1e-10)
    tri_integral = np.sum(tri_h) * dx
    tri_h = tri_h / tri_integral
    tri_h = np.clip(tri_h, 0.01, 1.0)
    tri_h = tri_h / np.sum(tri_h) * (1.0/dx)
    tri_h = np.clip(tri_h, 0.01, 1.0)
    tri_h = tri_h / (np.sum(tri_h) * dx)
    tri_c5 = 0.0
    j_tri = 1.0 - tri_h
    h_padded = np.pad(tri_h, (0, N))
    j_padded = np.pad(j_tri, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    tri_c5 = np.max(correlation * dx)

    candidates = [
        {"h": golomb_h.tolist(), "integral": float(golomb_integral),
         "c5_bound": float(golomb_c5), "pattern_type": "golomb_4"},
        {"h": bipartite_h.tolist(), "integral": float(bipartite_integral),
         "c5_bound": float(bipartite_c5), "pattern_type": "bipartite"},
        {"h": tri_h.tolist(), "integral": float(tri_integral),
         "c5_bound": float(tri_c5), "pattern_type": "tri_modal"}
    ]
    return {"candidates": candidates, "num_candidates": 3}
