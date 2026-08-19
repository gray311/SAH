def run(ctx, args):
    import numpy as np
    import math
    
    N = 800
    domain = 2.0
    dx = domain / N
    
    pattern_id = int(args.get("pattern_id", 12))
    mod_type = args.get("mod_type", "narrow_peaks")
    mod_value = float(args.get("mod_value", 0.5))
    
    def sigmoid(x):
        return 1.0 / (1.0 + np.exp(-x))
    
    # Base patterns from seed's _get_best_initialization
    x = np.linspace(0, 2, N)
    
    # Generate base latent for the requested pattern
    latent = None
    
    if pattern_id == 12:
        # Golomb ruler pattern
        marks = [0.0, 0.4, 0.8, 1.2, 1.6]
        latent = np.zeros(N)
        base_width = N * 0.1
        for m in marks:
            mask = np.abs(x - m) < mod_value
            latent[mask] = 4.0
        latent = latent - 2.0
    elif pattern_id == 14:
        # Tri-modal pattern
        peaks = [0.4, 1.0, 1.6]
        latent = np.zeros(N)
        base_bw = N * 0.15
        for center in peaks:
            mask = np.abs(x - center) < mod_value * 1.5
            latent[mask] = 4.0
        latent = latent - 2.0
    elif pattern_id in [5, 6, 8, 9, 13]:
        # Bipartite pattern
        a = 0.5  # base threshold
        if pattern_id == 5:
            a = 0.5
        elif pattern_id == 6:
            a = 1.0
        elif pattern_id == 8:
            a = 2.0 / 3.0
        elif pattern_id == 9:
            a = 1.0 / 3.0
        elif pattern_id == 13:
            a = 0.6
        
        # Apply modification
        if mod_type == 'adjust_threshold':
            a = float(mod_value)
        elif mod_type == 'shift_peaks':
            peaks = [(a - 0.2), a, a + 0.2]
        
        latent = np.where(x < a, 3.0, -3.0)
    elif pattern_id == 2:
        # Sin/cos pattern
        latent = np.sin(2 * np.pi * x) * mod_value * 2.0 + np.cos(4 * np.pi * x) * mod_value * 1.0
    else:
        # Default: random normal
        latent = np.random.randn(N) * mod_value * 0.5
    
    # Apply sigmoid and normalize
    latent = latent + np.random.randn(N) * 0.3  # Add noise
    latent = np.clip(latent, -20, 20)
    h = sigmoid(latent)
    
    # Normalize to integral = 1
    integral = np.sum(h) * dx
    h = h / integral
    h = np.clip(h, 0.001, 1.0)
    h = h / np.sum(h) * (1.0 / dx)
    h = np.clip(h, 0.001, 1.0)
    
    # Compute c5_bound analytically
    j = 1.0 - h
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(j, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    c5_bound = np.max(correlation * dx)
    
    return {
        "h": h.tolist(),
        "integral": float(np.sum(h) * dx),
        "c5_bound": float(c5_bound),
        "pattern_id": pattern_id,
        "mod_type": mod_type,
        "mod_value": mod_value
    }