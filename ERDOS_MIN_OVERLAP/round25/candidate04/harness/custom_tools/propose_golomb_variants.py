def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N

    candidates = []

    # Variant 1: Standard Golomb (5 marks)
    marks1 = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
    h1 = np.zeros(N)
    for m in marks1:
        h1 += 10.0 * np.exp(-((np.arange(N) - int(m * N)) / (N * 0.15))**2)
    h1 = np.clip(h1, 0.01, 10.0)
    h1 = np.exp(h1)
    h1 = h1 / (np.sum(h1) * dx)
    h1 = np.clip(h1, 0.01, 1.0)
    j1 = 1.0 - h1
    corr1 = np.fft.ifft(np.fft.fft(np.pad(h1,(0,N))) * np.conj(np.fft.fft(np.pad(j1,(0,N))))).real
    c1 = np.max(corr1 * dx)
    candidates.append({"type": "golomb_5_std", "marks": marks1.tolist(), "c5_bound": float(c1), "integral": float(np.sum(h1)*dx)})

    # Variant 2: 4 marks (sparser)
    marks2 = np.array([0.0, 0.5, 1.0, 1.5])
    h2 = np.zeros(N)
    for m in marks2:
        h2 += 10.0 * np.exp(-((np.arange(N) - int(m * N)) / (N * 0.15))**2)
    h2 = np.clip(h2, 0.01, 10.0)
    h2 = np.exp(h2)
    h2 = h2 / (np.sum(h2) * dx)
    h2 = np.clip(h2, 0.01, 1.0)
    j2 = 1.0 - h2
    corr2 = np.fft.ifft(np.fft.fft(np.pad(h2,(0,N))) * np.conj(np.fft.fft(np.pad(j2,(0,N))))).real
    c2 = np.max(corr2 * dx)
    candidates.append({"type": "golomb_4_sparse", "marks": marks2.tolist(), "c5_bound": float(c2), "integral": float(np.sum(h2)*dx)})

    # Variant 3: 5 marks denser
    marks3 = np.array([0.0, 0.33, 0.66, 1.33, 1.66])
    h3 = np.zeros(N)
    for m in marks3:
        h3 += 10.0 * np.exp(-((np.arange(N) - int(m * N)) / (N * 0.15))**2)
    h3 = np.clip(h3, 0.01, 10.0)
    h3 = np.exp(h3)
    h3 = h3 / (np.sum(h3) * dx)
    h3 = np.clip(h3, 0.01, 1.0)
    j3 = 1.0 - h3
    corr3 = np.fft.ifft(np.fft.fft(np.pad(h3,(0,N))) * np.conj(np.fft.fft(np.pad(j3,(0,N))))).real
    c3 = np.max(corr3 * dx)
    candidates.append({"type": "golomb_5_dense", "marks": marks3.tolist(), "c5_bound": float(c3), "integral": float(np.sum(h3)*dx)})

    # Variant 4: Asymmetric spacing
    marks4 = np.array([0.0, 0.25, 0.75, 1.25, 1.75])
    h4 = np.zeros(N)
    for m in marks4:
        h4 += 10.0 * np.exp(-((np.arange(N) - int(m * N)) / (N * 0.15))**2)
    h4 = np.clip(h4, 0.01, 10.0)
    h4 = np.exp(h4)
    h4 = h4 / (np.sum(h4) * dx)
    h4 = np.clip(h4, 0.01, 1.0)
    j4 = 1.0 - h4
    corr4 = np.fft.ifft(np.fft.fft(np.pad(h4,(0,N))) * np.conj(np.fft.fft(np.pad(j4,(0,N))))).real
    c4 = np.max(corr4 * dx)
    candidates.append({"type": "golomb_5_asym", "marks": marks4.tolist(), "c5_bound": float(c4), "integral": float(np.sum(h4)*dx)})

    # Variant 5: Wider spacing
    marks5 = np.array([0.0, 0.3, 0.9, 1.5])
    h5 = np.zeros(N)
    for m in marks5:
        h5 += 10.0 * np.exp(-((np.arange(N) - int(m * N)) / (N * 0.15))**2)
    h5 = np.clip(h5, 0.01, 10.0)
    h5 = np.exp(h5)
    h5 = h5 / (np.sum(h5) * dx)
    h5 = np.clip(h5, 0.01, 1.0)
    j5 = 1.0 - h5
    corr5 = np.fft.ifft(np.fft.fft(np.pad(h5,(0,N))) * np.conj(np.fft.fft(np.pad(j5,(0,N))))).real
    c5 = np.max(corr5 * dx)
    candidates.append({"type": "golomb_4_wide", "marks": marks5.tolist(), "c5_bound": float(c5), "integral": float(np.sum(h5)*dx)})

    return {"candidates": candidates, "num_candidates": len(candidates)}
