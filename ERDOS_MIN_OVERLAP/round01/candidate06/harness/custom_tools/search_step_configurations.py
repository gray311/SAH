def run(ctx, args):
    import numpy as np
    N = 200
    domain_width = 2.0
    dx = domain_width / N
    best_h = None
    best_obj = float('inf')
    
    # Strategy 1: Coordinate descent on interval heights
    h = np.ones(N) / N
    for _ in range(50):
        for i in range(N):
            for h_val in [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
                h_copy = h.copy()
                h_copy[i] = h_val
                h_copy = np.clip(h_copy, 0, 1)
                integral = np.sum(h_copy) * dx
                if integral > 0:
                    h_copy = h_copy * (1.0 / integral)
                    h_copy = np.clip(h_copy, 0, 1)
                j = 1.0 - h_copy
                corr = np.fft.ifft(np.fft.fft(h_copy) * np.conj(np.fft.fft(j))).real * dx
                obj = np.max(corr)
                if obj < best_obj:
                    best_obj = obj
                    best_h = h_copy.copy()
    
    # Strategy 2: Alternating pattern
    alt_h = np.zeros(N)
    for i in range(N):
        x = i * dx
        if x < 0.5:
            alt_h[i] = 0.8
        elif x < 1.0:
            alt_h[i] = 0.2
        elif x < 1.5:
            alt_h[i] = 0.6
        else:
            alt_h[i] = 0.4
    alt_h = alt_h / (np.sum(alt_h) * dx)
    alt_h = np.clip(alt_h, 0, 1)
    j = 1.0 - alt_h
    corr = np.fft.ifft(np.fft.fft(alt_h) * np.conj(np.fft.fft(j))).real * dx
    alt_obj = np.max(corr)
    if alt_obj < best_obj:
        best_obj = alt_obj
        best_h = alt_h
    
    # Strategy 3: Decreasing from left
    dec_h = np.linspace(1.0, 0.0, N)
    dec_h = dec_h * (N / np.sum(dec_h))
    dec_h = np.clip(dec_h, 0, 1)
    j = 1.0 - dec_h
    corr = np.fft.ifft(np.fft.fft(dec_h) * np.conj(np.fft.fft(j))).real * dx
    dec_obj = np.max(corr)
    if dec_obj < best_obj:
        best_obj = dec_obj
        best_h = dec_h
    
    # Strategy 4: Two-block pattern
    two_block = np.zeros(N)
    two_block[:N//2] = 0.9
    two_block[N//2:] = 0.1
    two_block = two_block / (np.sum(two_block) * dx)
    two_block = np.clip(two_block, 0, 1)
    j = 1.0 - two_block
    corr = np.fft.ifft(np.fft.fft(two_block) * np.conj(np.fft.fft(j))).real * dx
    two_obj = np.max(corr)
    if two_obj < best_obj:
        best_obj = two_obj
        best_h = two_block
    
    return {"best_h": best_h.tolist(), "best_c5": float(best_obj), "strategies_tested": 4}
