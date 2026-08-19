def run(ctx, args):
    import numpy as np
    config = args.get("config", {})
    h_values = np.asarray(config.get("h_values", []), dtype=float)
    break_points = np.asarray(config.get("break_points", [0.0, 2.0]), dtype=float)
    
    domain = 2.0
    N = 800
    x = np.linspace(0, domain, N)
    h = np.zeros(N)
    
    if len(break_points) > 1 and len(h_values) > 0:
        for i in range(len(break_points)-1):
            if i >= len(h_values):
                break
            bp_start, bp_end = break_points[i], break_points[i+1]
            val = h_values[i]
            start_idx = np.searchsorted(x, bp_start, side='right') - 1
            end_idx = np.searchsorted(x, bp_end, side='right') - 1
            if 0 <= start_idx < end_idx < N:
                h[start_idx:end_idx] = val
    
    h_padded = np.pad(h, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(1.0 - h_padded))
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = np.max(correlation * (domain / N))
    
    if c5_bound == 0:
        c5_bound = 1e-10
    
    combined_score = 0.38092303510845016 / c5_bound
    
    return {
        "c5_bound": float(c5_bound),
        "combined_score": float(combined_score),
        "h_values": h.tolist(),
        "best": combined_score > 1.0
    }