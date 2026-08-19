def run(ctx, args):
    import numpy as np
    breakpoints = sorted(args.get("breakpoints", []))
    values = args.get("values", [])
    
    # Ensure we have values for all intervals
    if len(values) != len(breakpoints) + 1:
        return {"valid": False, "error": "values must have len(breakpoints)+1"}
    
    # Check h ∈ [0,1]
    if not all(0 <= v <= 1 for v in values):
        return {"valid": False, "error": "values must be in [0,1]"}
    
    # Compute integral approx
    domain_width = 2.0
    prev_x = 0
    total_integral = 0
    for i, b in enumerate(breakpoints):
        width = b - prev_x
        if width <= 0:
            return {"valid": False, "error": f"negative or zero interval at {prev_x}"}
        total_integral += values[i] * width
        prev_x = b
    last_width = domain_width - prev_x
    total_integral += values[-1] * last_width
    
    # Check integral constraint
    if abs(total_integral - 1.0) > 1e-6:
        return {"valid": False, "error": f"integral {total_integral:.6f} != 1.0", "integral": total_integral}
    
    # Compute approximate c5_bound using FFT
    N = 800
    dx = domain_width / N
    x_grid = np.linspace(0, domain_width, N)
    h_interp = np.zeros(N)
    
    for i, b in enumerate(breakpoints):
        mask = (x_grid >= b - 1e-9) & (x_grid < b)
        if i < len(values):
            h_interp = h_interp + values[i] * mask
    
    # Add last interval
    mask_last = x_grid >= breakpoints[-1] if breakpoints else True
    h_interp = h_interp + values[-1] * mask_last
    
    # Compute c5
    j = 1.0 - h_interp
    h_padded = np.pad(h_interp, (0, N))
    j_padded = np.pad(j, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = float(np.max(correlation * dx))
    
    return {"valid": True, "integral": total_integral, "c5_bound": c5_bound}