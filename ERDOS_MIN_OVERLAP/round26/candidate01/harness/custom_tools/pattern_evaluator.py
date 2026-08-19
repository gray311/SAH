def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    temp = args.get("temperature", 0.3)
    
    def make_pattern(peak_locs, width, amplitude):
        h = np.zeros(N)
        for loc in peak_locs:
            h += amplitude * np.exp(-((np.arange(N) - int(loc * N)) / width)**2)
        h = np.clip(h, 0, 10)
        # Normalize to integral = 1
        integral = np.sum(h) * dx
        h = h / integral
        h = np.clip(h, 0.001, 1.0)
        integral = np.sum(h) * dx
        h = h / integral
        return h
    
    # Candidate 1: Golomb ruler pattern (4 marks, well-separated)
    golomb_peaks = [0.0, 0.4, 1.2, 1.6]
    golomb_h = make_pattern(golomb_peaks, 0.04, 8.0)
    j_golomb = 1.0 - golomb_h
    h_padded = np.pad(golomb_h, (0, N))
    j_padded = np.pad(j_golomb, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    golomb_c5 = float(np.max(correlation * dx))
    
    # Candidate 2: Tri-modal pattern (3 narrow peaks)
    tri_peaks = [0.4, 1.0, 1.6]
    tri_h = make_pattern(tri_peaks, 0.03, 10.0)
    j_tri = 1.0 - tri_h
    h_padded = np.pad(tri_h, (0, N))
    j_padded = np.pad(j_tri, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    tri_c5 = float(np.max(correlation * dx))
    
    # Candidate 3: Bipartite pattern (high on [0,a), low on [a,2])
    a = 0.5
    bipartite_h = np.zeros(N)
    bipartite_h[:int(N*a)] = 2.0
    bipartite_h[int(N*a):] = -0.5
    bipartite_h = np.clip(bipartite_h, 0.01, 10.0)
    integral = np.sum(bipartite_h) * dx
    bipartite_h = bipartite_h / integral
    bipartite_h = np.clip(bipartite_h, 0.01, 1.0)
    integral = np.sum(bipartite_h) * dx
    bipartite_h = bipartite_h / integral
    j_bipartite = 1.0 - bipartite_h
    h_padded = np.pad(bipartite_h, (0, N))
    j_padded = np.pad(j_bipartite, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    bipartite_c5 = float(np.max(correlation * dx))
    
    # Candidate 4: 5-peak pattern (more marks)
    five_peaks = [0.0, 0.4, 0.8, 1.2, 1.6]
    five_h = make_pattern(five_peaks, 0.03, 12.0)
    j_five = 1.0 - five_h
    h_padded = np.pad(five_h, (0, N))
    j_padded = np.pad(j_five, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    five_c5 = float(np.max(correlation * dx))
    
    candidates = [
        {"h": golomb_h.tolist(), "integral": float(np.sum(golomb_h)*dx), "c5_bound": golomb_c5, "pattern_type": "golomb_4"},
        {"h": tri_h.tolist(), "integral": float(np.sum(tri_h)*dx), "c5_bound": tri_c5, "pattern_type": "tri_modal_3"},
        {"h": bipartite_h.tolist(), "integral": float(np.sum(bipartite_h)*dx), "c5_bound": bipartite_c5, "pattern_type": "bipartite_a0.5"},
        {"h": five_h.tolist(), "integral": float(np.sum(five_h)*dx), "c5_bound": five_c5, "pattern_type": "five_peaks"}
    ]
    
    # Sort by c5_bound
    candidates.sort(key=lambda x: x["c5_bound"])
    
    return {"candidates": candidates[:3], "num_candidates": 3, "best_c5": candidates[0]["c5_bound"]}