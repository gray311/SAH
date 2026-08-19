def run(ctx, args):
    import numpy as np
    N = 500
    domain = 2.0
    dx = domain / N
    
    pattern_type = args.get("pattern_type", "golomb")
    marks = args.get("marks", [0.0, 0.4, 1.0, 1.6])
    threshold = args.get("threshold", 0.5)
    peak_width = args.get("peak_width", 0.1)
    num_peaks = args.get("num_peaks", 3)
    distribution = args.get("distribution", "laplace")
    
    def build_h_from_params(p_type, marks, thresh, width, npeaks, dist):
        h = np.zeros(N)
        if p_type == "golomb":
            for m in marks:
                idx = int(m * N)
                if idx < N:
                    h[idx] = 4.0
            h = h / (np.sum(h) * dx)
            h = np.clip(h, 0.001, 1.0)
            h = h / (np.sum(h) * dx)
        elif p_type == "bipartite":
            n_thresh = int(thresh * N)
            if n_thresh < N:
                h[:n_thresh] = 4.0
            h[n_thresh:] = -1.0
            h = h / (np.sum(h) * dx)
            h = np.clip(h, 0.001, 1.0)
            h = h / (np.sum(h) * dx)
        elif p_type == "triangular":
            center_idx = int(1.0 * N)
            start = center_idx - int(width*N)
            end = center_idx + int(width*N)
            if start >= 0 and end <= N:
                h[start:end] = 20.0
            h = h / (np.sum(h) * dx)
            h = np.clip(h, 0.001, 1.0)
            h = h / (np.sum(h) * dx)
        elif p_type == "multi_peak":
            centers = [0.4, 1.0, 1.6]
            for c in centers:
                idx = int(c * N)
                if idx < N:
                    h[idx] = 15.0
            h = h / (np.sum(h) * dx)
            h = np.clip(h, 0.001, 1.0)
            h = h / (np.sum(h) * dx)
        elif p_type == "random":
            if dist == "laplace":
                vals = -np.log(-np.log(np.random.uniform(0.001, 0.999, N)) + 1e-10)
            else:
                vals = np.random.uniform(0, 3, N)
            h = vals / (np.sum(vals) * dx)
            h = np.clip(h, 0.001, 1.0)
            h = h / (np.sum(h) * dx)
        return h
    
    if pattern_type == "golomb":
        h = build_h_from_params(pattern_type, marks, None, None, None, None)
    elif pattern_type == "bipartite":
        h = build_h_from_params(pattern_type, None, threshold, None, None, None)
    elif pattern_type == "triangular":
        h = build_h_from_params(pattern_type, None, None, peak_width, None, None)
    elif pattern_type == "multi_peak":
        h = build_h_from_params(pattern_type, None, None, None, num_peaks, None)
    elif pattern_type == "random":
        h = build_h_from_params(pattern_type, None, None, None, None, distribution)
    else:
        return {"error": "Unknown pattern type"}
    
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(1.0 - h, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
    c5_bound = np.max(corr * dx)
    
    return {"c5_bound": float(c5_bound), "pattern_type": pattern_type}