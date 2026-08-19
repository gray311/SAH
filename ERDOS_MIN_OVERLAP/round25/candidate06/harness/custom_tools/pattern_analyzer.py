def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    def compute_c5(h_arr):
        h = np.array(h_arr, dtype=np.float64)
        j_val = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        return np.max(correlation * dx)
    
    results = []
    
    # Golomb variants
    golomb_marks_list = [
        [0.0, 0.35, 0.7, 1.05, 1.4],
        [0.0, 0.3, 0.6, 0.9, 1.2],
        [0.0, 0.4, 0.8, 1.2, 1.6],
        [0.0, 0.25, 0.5, 0.75, 1.0],
        [0.0, 0.33, 0.66, 1.0, 1.33]
    ]
    for marks in golomb_marks_list:
        latent = np.zeros(N)
        for m in marks:
            width = N * 0.08
            mask = np.abs(np.arange(N) - int(m * N)) < width
            latent[mask] = 4.0
        latent -= 2.0
        h = np.clip(np.exp(latent) / (1.0 + np.exp(latent)), 0.001, 1.0)
        h = h / np.sum(h) * (1.0/dx)  # normalize to integral 1
        c5 = compute_c5(h)
        results.append({"type": "golomb", "marks": marks, "c5": float(c5)})
    
    # Bipartite variants
    bipartite_a_list = [0.4, 0.5, 0.6, 0.7]
    for a in bipartite_a_list:
        latent = np.zeros(N)
        x = np.linspace(0, 2, N)
        latent[x < a] = 4.0
        latent[x >= a] = -1.0
        h = np.clip(np.exp(latent) / (1.0 + np.exp(latent)), 0.001, 1.0)
        h = h / np.sum(h) * (1.0/dx)
        c5 = compute_c5(h)
        results.append({"type": "bipartite", "a": a, "c5": float(c5)})
    
    # Tri-modal variants
    tri_peaks_list = [
        [0.3, 0.9, 1.5],
        [0.25, 1.0, 1.75],
        [0.35, 1.05, 1.65],
        [0.2, 1.0, 1.8],
        [0.4, 1.0, 1.6]
    ]
    for peaks in tri_peaks_list:
        latent = np.zeros(N)
        for p in peaks:
            bw = 0.06
            mask = np.abs(np.arange(N) - int(p * N)) < N * bw
            latent[mask] = 4.0
        latent -= 2.0
        h = np.clip(np.exp(latent) / (1.0 + np.exp(latent)), 0.001, 1.0)
        h = h / np.sum(h) * (1.0/dx)
        c5 = compute_c5(h)
        results.append({"type": "tri_modal", "peaks": peaks, "c5": float(c5)})
    
    best = min(results, key=lambda x: x["c5"])
    return {
        "results": results,
        "best": best,
        "best_type": best["type"],
        "best_c5": best["c5"],
        "best_params": best["marks"] if best["type"] == "golomb" else ({"a": best["a"]} if best["type"] == "bipartite" else {"peaks": best["peaks"]})
    }