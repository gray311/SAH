def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    cand = []

    # Wavelet bands at different scales
    for scale in [4, 3]:
        h = np.zeros(N)
        step = 2.0 / scale
        for i in range(int(N // (2*scale))):
            band_start = int(i * 2 * step * N)
            band_end = band_start + int(step * N)
            if band_end > N:
                band_end = N
            h[band_start:band_end] = 4.0
        h = np.clip(h, 0.01, 5.0)
        h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
        h = h / (np.sum(h) * dx)
        h = np.clip(h, 0.01, 1.0)
        j = 1.0 - h
        h_pad = np.pad(h, (0, N))
        j_pad = np.pad(j, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
        c5 = float(np.max(corr * dx))
        cand.append({"h": h.tolist(), "integral": float(np.sum(h)*dx), "c5_bound": c5, "pattern": f"wavelet_scale_{scale}"})

    # Fourier modes
    h = np.zeros(N)
    for freq, amp in [(1, 0.8), (3, 0.5), (5, 0.3)]:
        h += amp * np.cos(2 * np.pi * freq * np.arange(N) / 2.0)
    h = np.clip(h, -3.0, 5.0)
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.01, 1.0)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = float(np.max(corr * dx))
    cand.append({"h": h.tolist(), "integral": float(np.sum(h)*dx), "c5_bound": c5, "pattern": "fourier_modes"})

    # Piecewise linear
    h = np.zeros(N)
    h[:int(0.3*N)] = 3.0
    h[int(0.3*N):int(0.6*N)] = np.linspace(3.0, 0.5, int(0.3*N))
    h[int(0.6*N):] = 0.5
    h = np.clip(h, 0.01, 5.0)
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.01, 1.0)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = float(np.max(corr * dx))
    cand.append({"h": h.tolist(), "integral": float(np.sum(h)*dx), "c5_bound": c5, "pattern": "piecewise_linear"})

    # Multi-scale bumps
    h = np.zeros(N)
    for center, width in [(0.4, 0.05), (1.0, 0.15), (1.6, 0.03)]:
        pos = int(center * N)
        bw = int(N * width)
        for k in range(-bw, bw+1):
            idx = pos + k
            if 0 <= idx < N:
                h[idx] += 6.0 * np.exp(-((k) / bw)**2)
    h = np.clip(h, 0.01, 5.0)
    h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
    h = h / (np.sum(h) * dx)
    h = np.clip(h, 0.01, 1.0)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = float(np.max(corr * dx))
    cand.append({"h": h.tolist(), "integral": float(np.sum(h)*dx), "c5_bound": c5, "pattern": "multi_scale_bumps"})

    return {"candidates": cand, "num_candidates": len(cand)}