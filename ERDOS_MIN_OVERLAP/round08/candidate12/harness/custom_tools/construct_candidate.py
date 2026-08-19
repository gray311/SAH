def run(ctx, args):
    import math
    import numpy as np
    num_intervals = args.get("num_intervals", 200)
    N = num_intervals
    params = args.get("params", {})
    pattern = args.get("pattern", "single_step")
    
    dx = 2.0 / N
    h = np.zeros(N)
    
    # Single step: h=1 on [0,1], need to normalize for integral=1
    if pattern == "single_step":
        h = np.ones(N // 2)
    
    elif pattern == "double_step":
        half_N = N // 4
        h = np.ones(half_N)
        h = np.concatenate([h, np.zeros(half_N), np.ones(half_N)])
    
    elif pattern == "symmetric_3step":
        third_N = N // 3
        h = np.zeros(N)
        h[:third_N] = 1.0/3.0
        h[2*third_N:3*third_N] = 1.0/3.0
    
    elif pattern == "concentrated_mass":
        start_idx = int(0.5 / 2.0 * N)
        end_idx = int(1.5 / 2.0 * N)
        h[start_idx:end_idx] = 1.0
    
    elif pattern == "triangular":
        x = np.linspace(0, 2, N)
        h = np.maximum(0.0, 1.0 - np.abs(x - 1.0))
    
    elif pattern == "sine_wave":
        x = np.linspace(0, 2, N)
        h = 0.5 + 0.5 * np.sin(math.pi * x)
    
    elif pattern == "piecewise_constant":
        h = np.full(N, 0.5)
    
    # Normalize h to ensure integral = 1
    integral_h = np.sum(h) * dx
    if integral_h > 0 and integral_h != 1.0:
        h = h / integral_h
        h = np.clip(h, 0.0, 1.0)
        integral_h = np.sum(h) * dx
        if integral_h > 0:
            h = h / integral_h
    
    # Compute c5_bound
    j_arr = 1.0 - h
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(j_arr, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = np.max(correlation) * dx
    
    return {
        "h": h.tolist(),
        "c5_bound": float(c5_bound),
        "pattern": pattern,
        "num_intervals": N,
        "integral": float(np.sum(h) * dx)
    }