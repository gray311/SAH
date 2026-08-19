def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    num_spikes = args.get('num_spikes', 5)
    spike_positions = args.get('spike_positions', [0.1, 0.3, 0.7, 1.3, 1.9])
    spike_height = args.get('spike_height', 20.0)
    spike_width = args.get('spike_width', 0.04)
    
    h = np.zeros(N)
    for pos in spike_positions:
        start = int(pos * N)
        end = start + int(N * spike_width)
        h[start:end] = spike_height
    
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
        "num_spikes": num_spikes,
        "spike_positions": spike_positions,
        "spike_height": spike_height,
        "spike_width": spike_width,
        "integral": float(np.sum(h) * dx),
        "c5_bound": float(c5_bound),
        "pattern_type": "sparse",
        "optimized": True
    }
