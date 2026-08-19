def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    def sigmoid_normalize(latent):
        h = 1.0 / (1.0 + np.exp(-latent))
        h = np.clip(h, 0.01, 0.99)
        integral = np.sum(h) * dx
        if integral > 0:
            h = h / integral
        return h
    
    def compute_c5(h):
        j = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5 = np.max(correlation * dx)
        return c5
    
    def make_candidate(latent, label, hyperparams):
        h = sigmoid_normalize(latent)
        c5 = compute_c5(h)
        return {
            "h": h.tolist(),
            "estimated_c5": float(c5),
            "hyperparameters": hyperparams,
            "pattern_type": label,
            "integral": float(np.sum(h) * dx)
        }
    
    candidates = []
    
    if args.get("coarse", True):
        patterns = [
            ([0.0, 0.45, 1.2, 1.8], "golomb_4"),
            ([0.0, 0.5, 1.0, 1.5, 2.0], "golomb_5"),
            ([0.4, 1.0, 1.6], "tri_modal"),
            ([0.0, 0.5], "bipartite"),
            ([0.3, 1.0, 1.7], "tri_modal_shift"),
            ([0.2, 1.0, 1.8], "tri_modal_wide")
        ]
        penalties = [30, 60, 100]
        lrs = [0.003, 0.006, 0.012]
        idx = 0
        for p_idx, (marks, label) in enumerate(patterns):
            if idx >= 6:
                break
            for penalty in penalties:
                if idx >= 6:
                    break
                for lr in lrs:
                    if idx >= 6:
                        break
                    latent = np.zeros(N)
                    for m in marks:
                        latent += 8.0 * np.exp(-((np.arange(N) - int(m * N)) / (N * 0.1))**2)
                    latent -= 2.0
                    h = sigmoid_normalize(latent)
                    c5 = compute_c5(h)
                    hyperparams = {"num_intervals": 800, "penalty_strength": penalty, "base_learning_rate": lr}
                    candidates.append(make_candidate(latent, label, hyperparams))
                    idx += 1
        if len(candidates) < 6:
            for i in range(6 - len(candidates)):
                latent = np.random.randn(N) * 3.0
                h = sigmoid_normalize(latent)
                c5 = compute_c5(h)
                hyperparams = {"num_intervals": 800, "penalty_strength": 60, "base_learning_rate": 0.006}
                candidates.append(make_candidate(latent, f"random_{i}", hyperparams))
    else:
        latent = np.zeros(N)
        for m in [0.0, 0.4, 0.8, 1.2, 1.6]:
            latent += 6.0 * np.exp(-((np.arange(N) - int(m * N)) / (N * 0.08))**2)
        latent -= 1.5
        h = sigmoid_normalize(latent)
        c5 = compute_c5(h)
        hyperparams = {"num_intervals": 800, "penalty_strength": 60, "base_learning_rate": 0.006}
        candidates.append(make_candidate(latent, "golomb_base", hyperparams))
        
        intervals = [800, 1600]
        penalties = [40, 60, 100]
        lrs = [0.004, 0.006, 0.008]
        for intervals_n in intervals:
            for penalty in penalties:
                for lr in lrs:
                    if len(candidates) >= 12:
                        break
                    h_fine = h.copy()
                    hyperparams = {"num_intervals": intervals_n, "penalty_strength": penalty, "base_learning_rate": lr}
                    candidates.append(make_candidate(latent, f"golomb_fine_{intervals_n}", hyperparams))
                if len(candidates) >= 12:
                    break
            if len(candidates) >= 12:
                break
    
    return {"candidates": candidates, "num_candidates": len(candidates)}