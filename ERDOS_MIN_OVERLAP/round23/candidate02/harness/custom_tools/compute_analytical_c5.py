def run(ctx, args):
    import numpy as np
    
    h_array = np.array(args.get("h", []), dtype=np.float64)
    N = args.get("num_intervals", 800)
    domain = args.get("domain", 2.0)
    dx = domain / N
    
    # Sigmoid activation (matches seed)
    h = 1.0 / (1.0 + np.exp(-h_array))
    h = np.clip(h, 1e-6, 1.0 - 1e-6)
    
    # Normalize to integral = 1 (matches seed)
    integral = np.sum(h) * dx
    if integral < 1e-8:
        return {"c5_bound": float("inf"), "integral": float(integral), "normalized": False}
    h_normalized = h / integral
    
    # Compute c5_bound using FFT (exact seed implementation)
    h_padded = np.pad(h_normalized, (0, N))
    j_func = 1.0 - h_padded
    j_padded = np.pad(j_func, (0, N))
    
    h_fft = np.fft.fft(h_padded)
    j_fft = np.fft.fft(j_padded)
    corr_fft = h_fft * np.conj(j_fft)
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = np.max(correlation * dx)
    
    return {"c5_bound": float(c5_bound), "integral": float(integral), "normalized": True}