def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N

    def compute_c5(h):
        j_val = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        return float(np.max(correlation * dx))

    def normalize(h):
        integral = float(np.sum(h) * dx)
        if integral > 0:
            return h / integral
        return h

    pattern_type = args.get("pattern_type", "bipartite")
    peak_positions = args.get("peak_positions", None)
    num_peaks = args.get("num_peaks", 2)

    if peak_positions is None:
        if pattern_type == "bipartite":
            peak_positions = [0.2, 1.8]
        elif pattern_type == "tri_modal":
            peak_positions = [0.4, 1.0, 1.6]
        elif pattern_type == "golomb":
            # Normalize Golomb ruler [0,1,3,6] to [0,2]
            ruler = [0, 1, 3, 6]
            min_r, max_r = 0, 6
            peak_positions = [((p - min_r) / (max_r - min_r)) * 2 for p in ruler[:num_peaks]]
        elif pattern_type == "gaussian":
            peak_positions = [0.5, 1.0, 1.5]
        else:
            peak_positions = [0.5, 1.5]

    # Build h from peaks using Gaussian bumps
    h = np.zeros(N)
    sigma = 0.15
    for pos in peak_positions:
        indices = (np.arange(N) * dx)
        mask = np.abs(indices - pos) < 0.1
        h[mask] += 4.0

    # Add small noise for diversity
    h = h + np.random.normal(0, 0.05, N)
    h = np.clip(h, 0.001, 5.0)

    # Normalize
    h = normalize(h)

    integral = float(np.sum(h) * dx)
    c5 = compute_c5(h)

    # Check constraints
    valid = (0.99 <= integral <= 1.01) and (0 <= h.min() and h.max() <= 1.1)

    return {
        "pattern_type": pattern_type,
        "integral": integral,
        "c5_bound_approx": c5,
        "valid": valid,
        "num_peaks": len(peak_positions),
        "h_sample": h[:100].tolist()  # Return small sample
    }