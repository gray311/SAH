def run(ctx, args):
    import numpy as np
    N = 200
    domain = 2.0
    dx = domain / N
    
    def compute_c5(h_arr):
        h_padded = np.pad(h_arr, (0, N))
        j_padded = np.pad(1.0 - h_arr, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
        return float(np.max(corr * dx))
    
    def normalize_to_integral(h_arr):
        current_int = np.sum(h_arr) * dx
        if current_int > 0:
            h_arr = h_arr / current_int
        return h_arr
    
    candidates = []
    
    # Golomb ruler patterns (4, 5, 6 marks)
    for num_marks in [4, 5, 6]:
        marks = np.linspace(0.2, 1.8, num_marks)
        h_arr = np.zeros(N)
        for mark in marks:
            width = N * 0.25
            h_arr += 4.0 * np.exp(-((np.arange(N) - int(mark * N)) / width)**2)
        h_arr = normalize_to_integral(h_arr)
        c5 = compute_c5(h_arr)
        candidates.append({"h": h_arr.tolist(), "c5_bound": c5, "pattern": f"golomb_{num_marks}_marks"})
    
    # Bipartite patterns (different thresholds)
    for threshold in [0.3, 0.4, 0.5, 0.6]:
        h_arr = np.zeros(N)
        h_arr[:int(N * threshold)] = 2.0
        h_arr[int(N * threshold):] = -1.0
        h_arr = normalize_to_integral(h_arr)
        c5 = compute_c5(h_arr)
        candidates.append({"h": h_arr.tolist(), "c5_bound": c5, "pattern": f"bipartite_a={threshold}"})
    
    # Triangular pattern (single peak at center)
    h_arr = np.zeros(N)
    peak_width = N * 0.2
    h_arr[N//2 - int(peak_width/2):N//2 + int(peak_width/2)] = 15.0
    h_arr = normalize_to_integral(h_arr)
    c5 = compute_c5(h_arr)
    candidates.append({"h": h_arr.tolist(), "c5_bound": c5, "pattern": "triangular_centered"})
    
    # Multi-peak patterns
    for num_peaks in [2, 3, 4]:
        centers = np.linspace(0.3, 1.7, num_peaks)
        h_arr = np.zeros(N)
        for center in centers:
            width = N * 0.15
            h_arr += 8.0 * np.exp(-((np.arange(N) - int(center * N)) / width)**2)
        h_arr = normalize_to_integral(h_arr)
        c5 = compute_c5(h_arr)
        candidates.append({"h": h_arr.tolist(), "c5_bound": c5, "pattern": f"multi_{num_peaks}_peaks"})
    
    # Gaussian pattern
    h_arr = np.exp(-((np.arange(N) - N/2) / (N * 0.15))**2)
    h_arr = normalize_to_integral(h_arr)
    c5 = compute_c5(h_arr)
    candidates.append({"h": h_arr.tolist(), "c5_bound": c5, "pattern": "gaussian_centered"})
    
    # Uniform pattern
    h_arr = np.ones(N) * 0.5
    h_arr = normalize_to_integral(h_arr)
    c5 = compute_c5(h_arr)
    candidates.append({"h": h_arr.tolist(), "c5_bound": c5, "pattern": "uniform"})
    
    return {"candidates": candidates, "num_candidates": 10}