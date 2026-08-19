def run(ctx, args):
    import numpy as np
    pattern = args.get("pattern", "bipartite_left")
    params = args.get("parameters", {})
    
    N = 800
    domain = 2.0
    dx = domain / N
    x = np.linspace(0, 2, N+1)[:-1]
    
    if pattern == "bipartite_left":
        h = np.where(x < 0.5, 1.0, 0.0)
        integral_check = np.trapz(h, dx=dx)
    elif pattern == "bipartite_right":
        h = np.where(x >= 0.5, 1.0, 0.0)
        integral_check = np.trapz(h, dx=dx)
    elif pattern == "centered":
        center = params.get("center", 1.0)
        half_width = 0.5
        left = center - half_width
        right = center + half_width
        h = np.where((x >= left) & (x <= right), 1.0, 0.0)
        integral_check = np.trapz(h, dx=dx)
    elif pattern == "two_plateaus_left":
        a = params.get("a_left", 0.4)
        b = params.get("b_right", 1.6)
        total_on = a + (2.0 - b)
        if abs(total_on - 1.0) > 0.001:
            b = a + (2.0 - 1.0)  # enforce integral=1
        h = np.zeros(N)
        h[:int(a/ dx)] = 1.0
        h[int(b/ dx):] = 1.0
        integral_check = np.trapz(h, dx=dx)
    elif pattern == "alternating":
        # Four small plateaus: [0,0.2], [0.8,1.0], [1.2,1.4], [1.8,2.0]
        h = np.zeros(N)
        h[:int(0.2/dx)] = 1.0
        h[int(0.8/dx):int(1.0/dx)] = 1.0
        h[int(1.2/dx):int(1.4/dx)] = 1.0
        h[int(1.8/dx):] = 1.0
        integral_check = np.trapz(h, dx=dx)
    else:
        return {"error": f"Unknown pattern: {pattern}"}
    
    # Pad for FFT computation
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(1.0 - h, (0, N))
    
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = np.max(correlation * dx)
    
    return {
        "pattern": pattern,
        "parameters": params,
        "h_preview": h[:20].tolist(),
        "integral_check": float(integral_check),
        "c5_bound_approx": float(c5_bound),
        "note": f"Generated step function pattern {pattern}. Integral = {integral_check:.4f}"
    }