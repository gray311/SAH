def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N

    def compute_c5(h):
        j = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5 = np.max(correlation * dx)
        return c5

    def normalize_to_integral_1(h):
        integral = np.sum(h) * dx
        if integral > 0:
            h = h / integral
        return h

    # Pattern 1: 3-block [high, medium, low]
    h3 = np.zeros(N)
    a, b = int(N * 0.33), int(N * 0.66)
    h3[:a] = 2.0
    h3[a:b] = 1.0
    h3[b:] = 0.25
    h3 = normalize_to_integral_1(h3)
    c5_3 = compute_c5(h3)

    # Pattern 2: 5-block [high, med, low, low, zero]
    h5 = np.zeros(N)
    h5[:int(N*0.2)] = 2.5
    h5[int(N*0.2):int(N*0.4)] = 1.5
    h5[int(N*0.4):int(N*0.6)] = 0.8
    h5[int(N*0.6):int(N*0.8)] = 0.4
    h5[int(N*0.8):] = 0.1
    h5 = normalize_to_integral_1(h5)
    c5_5 = compute_c5(h5)

    # Pattern 3: Asymmetric [0,1] concentrated
    h_asym = np.zeros(N)
    h_asym[:int(N*0.7)] = 1.5
    h_asym[int(N*0.7):int(N*1.4)] = 0.6
    h_asym[int(N*1.4):] = 0.1
    h_asym = normalize_to_integral_1(h_asym)
    c5_asym = compute_c5(h_asym)

    # Pattern 4: Bipartite [1.0, 0.0] at optimal split
    h_bip = np.zeros(N)
    split = int(N * 0.55)
    h_bip[:split] = 2.0
    h_bip[split:] = 0.5
    h_bip = normalize_to_integral_1(h_bip)
    c5_bip = compute_c5(h_bip)

    # Pattern 5: Tri-modal [narrow peaks at 0.4, 1.0, 1.6]
    h_tri = np.zeros(N)
    for center in [int(N*0.4), int(N*1.0), int(N*1.6)]:
        width = int(N * 0.08)
        left = max(0, center - width)
        right = min(N, center + width)
        h_tri[left:right] = 4.0
    h_tri = normalize_to_integral_1(h_tri)
    c5_tri = compute_c5(h_tri)

    candidates = [
        {"h": h3.tolist(), "integral": float(np.sum(h3)*dx), "c5_bound": float(c5_3), "pattern_type": "3_block"},
        {"h": h5.tolist(), "integral": float(np.sum(h5)*dx), "c5_bound": float(c5_5), "pattern_type": "5_block"},
        {"h": h_asym.tolist(), "integral": float(np.sum(h_asym)*dx), "c5_bound": float(c5_asym), "pattern_type": "asymmetric"},
        {"h": h_bip.tolist(), "integral": float(np.sum(h_bip)*dx), "c5_bound": float(c5_bip), "pattern_type": "bipartite"},
        {"h": h_tri.tolist(), "integral": float(np.sum(h_tri)*dx), "c5_bound": float(c5_tri), "pattern_type": "tri_modal"}
    ]
    return {"candidates": candidates, "num_candidates": 5}
