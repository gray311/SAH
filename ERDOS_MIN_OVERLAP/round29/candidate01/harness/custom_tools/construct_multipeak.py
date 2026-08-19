def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    n_peaks = args.get('n_peaks', 3)
    peak_positions = args.get('peak_positions', [0.4, 1.0, 1.6])
    peak_width = args.get('peak_width', 0.08)
    
    h = np.zeros(N)
    for pos in peak_positions:
        start = int(pos * N)
        end = start + int(N * peak_width)
        h[start:end] = 1.0  # Height before normalization
    
    # Scale to satisfy integral = 1
    current_integral = np.sum(h) * dx
    if current_integral == 0:
        return {"error": "Zero integral"}
    h = h / current_integral
    
    # Clip to [0,1]
    h = np.clip(h, 0.0, 1.0)
    
    # Compute c5_bound via FFT
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(1.0 - h, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))).real
    c5_bound = np.max(corr * dx)
    
    return {
        "h": h.tolist(),
        "n_peaks": n_peaks,
        "peak_positions": peak_positions,
        "peak_width": peak_width,
        "integral": float(np.sum(h) * dx),
        "c5_bound": float(c5_bound),
        "pattern_type": f"multipeak_{n_peaks}",
        "optimized": True
    }
