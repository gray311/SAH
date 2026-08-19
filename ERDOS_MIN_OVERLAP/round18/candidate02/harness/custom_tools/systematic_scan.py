def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    temp = args.get("temperature", 0.5)
    n_peaks = args.get("num_peaks", 3)
    spacing = args.get("peak_spacing", "equal")
    
    def make_candidate(peaks, widths, amplitudes):
        h = np.zeros(N)
        for i, (center, w, amp) in enumerate(zip(peaks, widths, amplitudes)):
            # Gaussian peak
            h += amp * np.exp(-((np.arange(N) - int(center * N)) / (N * w))**2)
        
        # Normalize to integral=1
        if np.sum(h) > 1e-10:
            h = h / (np.sum(h) * dx)
        
        # Clip and re-normalize
        h = np.clip(h, 0.01, 5.0)
        h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
        h = h / (np.sum(h) * dx)  # integral=1
        h = np.clip(h, 0.001, 1.0)
        
        # Compute c5_bound
        h_padded = np.pad(h, (0, N))
        j_val = np.clip(1.0 - h, 0, 1)
        j_padded = np.pad(j_val, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5 = np.max(correlation * dx)
        
        return {"h": h.tolist(), "integral": float(np.sum(h) * dx),
                "c5_bound": float(c5), "pattern": f"peaks_{n_peaks}"}
    
    # Generate 6 candidates
    candidates = []
    
    # Candidate 0: 2 peaks at 1/3, 2/3
    peaks = [2/3, 4/3]
    widths = [0.12, 0.12]
    amps = [4.0, 4.0]
    candidates.append(make_candidate(peaks, widths, amps))
    
    # Candidate 1: 3 peaks equal spacing
    peaks = [0.6, 1.0, 1.4]
    widths = [0.1, 0.1, 0.1]
    amps = [3.0, 3.0, 3.0]
    candidates.append(make_candidate(peaks, widths, amps))
    
    # Candidate 2: 3 peaks at 0.5, 1.0, 1.5
    peaks = [0.5, 1.0, 1.5]
    widths = [0.15, 0.15, 0.15]
    amps = [3.5, 3.5, 3.5]
    candidates.append(make_candidate(peaks, widths, amps))
    
    # Candidate 3: 4 peaks quarter spacing
    peaks = [0.5, 1.0, 1.5, 2.0]
    widths = [0.08, 0.08, 0.08, 0.08]
    amps = [2.5, 2.5, 2.5, 2.5]
    candidates.append(make_candidate(peaks, widths, amps))
    
    # Candidate 4: Gaussian peaks at optimized locations
    peaks = [0.35, 0.8, 1.3, 1.75]
    widths = [0.12, 0.12, 0.12, 0.12]
    amps = [2.0, 2.0, 2.0, 2.0]
    candidates.append(make_candidate(peaks, widths, amps))
    
    # Candidate 5: Narrow peaks with large amplitude
    peaks = [0.4, 1.0, 1.6]
    widths = [0.06, 0.06, 0.06]
    amps = [5.0, 5.0, 5.0]
    candidates.append(make_candidate(peaks, widths, amps))
    
    return {"candidates": candidates, "num_candidates": 6}