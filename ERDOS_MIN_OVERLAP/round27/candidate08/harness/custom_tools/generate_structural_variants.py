def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    config = args.get("config", "narrow_4pulse")
    
    def make_pulses(centers, width):
        h = np.zeros(N)
        for c in centers:
            center_idx = int(c * N)
            half_w = int(width * N)
            for i in range(center_idx - half_w, center_idx + half_w + 1):
                if 0 <= i < N:
                    dist = abs(i - center_idx)
                    pulse_val = max(0.0, 1.0 - dist / half_w)
                    h[i] += pulse_val
        integral = np.sum(h) * dx
        if integral > 0:
            h = h / integral
        h = np.clip(h, 0.0, 1.0)
        return h
    
    centers_by_config = {
        "narrow_4pulse": ([0.2, 0.7, 1.2, 1.7], 0.12),
        "medium_5pulse": ([0.15, 0.5, 0.85, 1.2, 1.55], 0.18),
        "wide_6pulse": ([0.1, 0.4, 0.6, 1.0, 1.4, 1.7], 0.25),
        "bipolar_2pulse": ([0.5, 1.5], 0.3),
        "central_1pulse": ([1.0], 0.5),
    }
    
    candidates = []
    for name, (centrs, w) in centers_by_config.items():
        h = make_pulses(centrs, w)
        j = 1.0 - h
        h_pad = np.pad(h, (0, N))
        j_pad = np.pad(j, (0, N))
        corr = np.fft.fft(h_pad) * np.fft.fft(j_pad).conj()
        corr = np.fft.ifft(corr).real
        c5 = float(np.max(corr * dx))
        
        candidates.append({
            "h": h.tolist(),
            "c5_bound": c5,
            "pattern_type": name,
            "centers": centrs,
            "width": w,
            "integral": float(np.sum(h) * dx),
        })
    
    return {"candidates": candidates, "num_candidates": len(candidates)}
