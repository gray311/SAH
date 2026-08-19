def run(ctx, args):
    import numpy as np
    
    intervals = args.get("intervals", [])
    N = args.get("num_intervals_for_fft", 800)
    domain_width = 2.0
    dx = domain_width / N
    
    # Build h array from intervals
    h = np.zeros(N)
    valid = True
    
    total_integral = 0.0
    for i, (start, end, height) in enumerate(intervals):
        if not (0 <= start <= end <= 2):
            valid = False
            break
        if height < 0 or height > 1:
            valid = False
            break
        start_idx = int(start / domain_width * N)
        end_idx = int(end / domain_width * N)
        h[start_idx:end_idx] = height
        total_integral += height * (end - start)
    
    # Check integral constraint
    integral_check = total_integral
    if not (0.99 <= integral_check <= 1.01):
        if integral_check > 0:
            h = h / integral_check
            integral_check = 1.0
        else:
            valid = False
    
    # Compute c5_bound
    j = 1.0 - h
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(j, (0, N))
    
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = float(np.max(correlation * dx))
    
    if c5_bound == 0:
        combined_score = 0.0
    else:
        combined_score = 0.38092303510845016 / c5_bound
    
    return {
        "c5_bound": c5_bound,
        "combined_score": combined_score,
        "integral": float(total_integral),
        "valid": valid,
        "note": f"Piecewise function with {len(intervals)} intervals"
    }