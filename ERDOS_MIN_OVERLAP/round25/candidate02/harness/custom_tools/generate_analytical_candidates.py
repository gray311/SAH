def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N

    candidates = []

    # Pattern 1: Golomb-4 (4 marks: 0, 0.4, 0.8, 1.2)
    golomb4_marks = np.array([0.0, 0.4, 0.8, 1.2])
    golomb4_h = np.zeros(N)
    for mark in golomb4_marks:
        idx = int(mark * N)
        width = int(N * 0.08)
        for d in range(-width, width+1):
            new_idx = idx + d
            if 0 <= new_idx < N:
                golomb4_h[new_idx] += 10.0 / (1.0 + np.abs(d) * 0.5)
    golomb4_h = np.clip(golomb4_h, 0.01, 10.0)
    golomb4_sum = np.sum(golomb4_h) * dx
    golomb4_h = golomb4_h / golomb4_sum
    golomb4_h = np.clip(golomb4_h, 0.01, 1.0)
    golomb4_sum2 = np.sum(golomb4_h) * dx
    golomb4_h = golomb4_h / golomb4_sum2
    j4 = 1.0 - golomb4_h
    h4 = np.pad(golomb4_h, (0, N))
    j4p = np.pad(j4, (0, N))
    c4 = np.fft.ifft(np.fft.fft(h4) * np.conj(np.fft.fft(j4p))).real
    c4_bound = np.max(c4 * dx)
    candidates.append({"h": golomb4_h.tolist(), "integral": float(golomb4_sum2),
                       "c5_bound": float(c4_bound), "pattern": "golomb4"})

    # Pattern 2: Golomb-5 (5 marks: optimal spacing)
    golomb5_marks = np.array([0.0, 0.4, 0.8, 1.2, 1.6])
    golomb5_h = np.zeros(N)
    for mark in golomb5_marks:
        idx = int(mark * N)
        width = int(N * 0.08)
        for d in range(-width, width+1):
            new_idx = idx + d
            if 0 <= new_idx < N:
                golomb5_h[new_idx] += 10.0 / (1.0 + np.abs(d) * 0.5)
    golomb5_h = np.clip(golomb5_h, 0.01, 10.0)
    golomb5_sum = np.sum(golomb5_h) * dx
    golomb5_h = golomb5_h / golomb5_sum
    golomb5_h = np.clip(golomb5_h, 0.01, 1.0)
    golomb5_sum2 = np.sum(golomb5_h) * dx
    golomb5_h = golomb5_h / golomb5_sum2
    j5 = 1.0 - golomb5_h
    h5 = np.pad(golomb5_h, (0, N))
    j5p = np.pad(j5, (0, N))
    c5 = np.fft.ifft(np.fft.fft(h5) * np.conj(np.fft.fft(j5p))).real
    c5_bound = np.max(c5 * dx)
    candidates.append({"h": golomb5_h.tolist(), "integral": float(golomb5_sum2),
                       "c5_bound": float(c5_bound), "pattern": "golomb5"})

    # Pattern 3: Bipartite (3 split points)
    for a in [0.3, 0.5, 0.7]:
        split = int(a * N)
        bipartite_h = np.zeros(N)
        bipartite_h[:split] = 4.0
        bipartite_h[split:] = -1.0
        bipartite_h = np.clip(bipartite_h, 0.01, 5.0)
        bipartite_sum = np.sum(bipartite_h) * dx
        bipartite_h = bipartite_h / bipartite_sum
        bipartite_h = np.clip(bipartite_h, 0.01, 1.0)
        bipartite_sum2 = np.sum(bipartite_h) * dx
        bipartite_h = bipartite_h / bipartite_sum2
        j_b = 1.0 - bipartite_h
        hb = np.pad(bipartite_h, (0, N))
        jbp = np.pad(j_b, (0, N))
        cb = np.fft.ifft(np.fft.fft(hb) * np.conj(np.fft.fft(jbp))).real
        cbound = np.max(cb * dx)
        candidates.append({"h": bipartite_h.tolist(), "integral": float(bipartite_sum2),
                           "c5_bound": float(cbound), "pattern": "bipartite_a" + str(int(a*10))})

    # Pattern 4: Tri-modal (3 peaks)
    peaks = [0.4, 1.0, 1.6]
    tri_h = np.zeros(N)
    for p in peaks:
        idx = int(p * N)
        width = int(N * 0.2)
        for d in range(-width, width+1):
            new_idx = idx + d
            if 0 <= new_idx < N:
                tri_h[new_idx] += 15.0 / (1.0 + np.abs(d) * 0.8)
    tri_h = np.clip(tri_h, 0.01, 15.0)
    tri_sum = np.sum(tri_h) * dx
    tri_h = tri_h / tri_sum
    tri_h = np.clip(tri_h, 0.01, 1.0)
    tri_sum2 = np.sum(tri_h) * dx
    tri_h = tri_h / tri_sum2
    jt = 1.0 - tri_h
    h_tri = np.pad(tri_h, (0, N))
    jtp = np.pad(jt, (0, N))
    ct = np.fft.ifft(np.fft.fft(h_tri) * np.conj(np.fft.fft(jtp))).real
    ct_bound = np.max(ct * dx)
    candidates.append({"h": tri_h.tolist(), "integral": float(tri_sum2),
                       "c5_bound": float(ct_bound), "pattern": "tri_modal"})

    # Pattern 5: Uniform-2 (2 blocks)
    for a in [0.4, 0.5, 0.6]:
        split = int(a * N)
        unif2_h = np.zeros(N)
        unif2_h[:split] = 6.0
        unif2_h[split:] = -2.0
        unif2_h = np.clip(unif2_h, 0.01, 10.0)
        unif2_sum = np.sum(unif2_h) * dx
        unif2_h = unif2_h / unif2_sum
        unif2_h = np.clip(unif2_h, 0.01, 1.0)
        unif2_sum2 = np.sum(unif2_h) * dx
        unif2_h = unif2_h / unif2_sum2
        j2 = 1.0 - unif2_h
        h2 = np.pad(unif2_h, (0, N))
        j2p = np.pad(j2, (0, N))
        c2 = np.fft.ifft(np.fft.fft(h2) * np.conj(np.fft.fft(j2p))).real
        c2_bound = np.max(c2 * dx)
        candidates.append({"h": unif2_h.tolist(), "integral": float(unif2_sum2),
                           "c5_bound": float(c2_bound), "pattern": "uniform2_a" + str(int(a*10))})

    return {"candidates": candidates, "num_candidates": len(candidates)}