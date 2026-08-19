def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    candidates = []
    key = np.random.RandomState(42)
    
    # Pattern 1: Piecewise constant (2 blocks)
    x = np.linspace(0, 2, N)
    h = np.where(x < 1.0, 5.0, -1.0)
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "piecewise_const_2"})
    
    # Pattern 2: Piecewise constant (3 blocks)
    h = np.zeros(N)
    h[:int(0.3*N)] = 4.0
    h[int(0.3*N):int(0.7*N)] = -1.0
    h[int(0.7*N):] = 3.0
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "piecewise_const_3"})
    
    # Pattern 3: Piecewise linear ramp
    h = np.linspace(0.1, 1.0, N)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "piecewise_linear"})
    
    # Pattern 4: Random block placement
    num_blocks = 5
    positions = key.randint(0, N, num_blocks)
    h = np.zeros(N)
    block_size = int(N / num_blocks)
    for pos in positions:
        h[pos:pos+block_size] += 6.0
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "random_blocks"})
    
    # Pattern 5: Delta-like bumps (narrow peaks)
    num_peaks = 4
    bump_centers = key.randint(50, N-50, num_peaks)
    h = np.zeros(N)
    for center in bump_centers:
        h = h + 15.0 * np.exp(-((np.arange(N) - center) / 10)**2)
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "delta_bumps"})
    
    # Pattern 6: Checkerboard (spaced blocks)
    h = np.zeros(N)
    for i in range(0, N, 100):
        h[i:i+20] = 4.0
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "checkerboard"})
    
    # Pattern 7: Sparse Golomb variant (7 marks)
    marks = np.array([0.0, 0.35, 0.70, 1.05, 1.40, 1.75, 0.18])
    h = np.zeros(N)
    for m in marks:
        idx = int(m * N)
        h = h + 8.0 * np.exp(-((np.arange(N) - idx) / 8)**2)
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "sparse_golomb_7"})
    
    # Pattern 8: Extended tri-modal (4 peaks)
    peaks = np.array([0.25, 0.5, 1.0, 1.75])
    h = np.zeros(N)
    for p in peaks:
        idx = int(p * N)
        h = h + 6.0 * np.exp(-((np.arange(N) - idx) / 15)**2)
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "quad_modal"})
    
    # Pattern 9: Plateau with dips
    h = np.ones(N) * 2.0
    h[100:200] = -3.0
    h[500:600] = -3.0
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "plateau_dips"})
    
    # Pattern 10: Valley pattern (high sides, low center)
    h = np.ones(N) * 3.0
    h[150:650] = -4.0
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.001, 1.0)
    h = h / (np.sum(h) * dx)
    j = 1.0 - h
    corr = np.fft.ifft(np.fft.fft(h, N) * np.conj(np.fft.fft(j, N))).real[:N] * dx
    candidates.append({"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(np.max(corr)), "pattern": "valley"})
    
    return {"candidates": candidates, "num_candidates": len(candidates), "note": "Extra patterns to complement seed's 15 patterns. Merge and re-optimize with num_restarts=5."}
