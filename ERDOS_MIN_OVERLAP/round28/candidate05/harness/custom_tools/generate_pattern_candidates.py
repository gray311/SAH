def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    def make_candidate(marks=None, split_a=None, uniform=False, peaks=None, pattern_label=""):
        h = np.zeros(N)
        if uniform:
            h = np.full(N, 0.5)
        elif peaks:
            for p in peaks:
                h += 10.0 * np.exp(-((np.arange(N) - int(p * N)) / (N * 0.12))**2)
        elif split_a is not None:
            h[:int(N*split_a)] = 5.0
            h[int(N*split_a):] = -0.5
        elif marks:
            for m in marks:
                width = N * 0.08
                h += 8.0 * np.exp(-((np.arange(N) - int(m * N)) / width)**2)
        else:
            h = np.random.randn(N) * 0.3 + 0.5
        
        h = np.clip(h, 0.01, 5.0)
        h = np.exp(h) / (np.sum(np.exp(h)) + 1e-10)
        integral = np.sum(h) * dx
        h = h / integral
        h = np.clip(h, 0.001, 1.0)
        h = h / (np.sum(h) * dx)
        h = np.clip(h, 0.001, 1.0)
        
        j = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j, (0, N))
        corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
        correlation = np.fft.ifft(corr_fft).real
        c5_bound = np.max(correlation * dx)
        
        return {"h": h.tolist(), "integral": float(np.sum(h) * dx), "c5_bound": float(c5_bound), "pattern_type": pattern_label}
    
    candidates = []
    candidates.append(make_candidate(marks=[0.0, 0.4, 0.8, 1.2, 1.6], pattern_label="Golomb_5"))
    candidates.append(make_candidate(split_a=0.5, pattern_label="Bipartite_0.5"))
    candidates.append(make_candidate(peaks=[0.4, 1.0, 1.6], pattern_label="Tri_modal_0.12"))
    candidates.append(make_candidate(marks=[0.0, 0.45, 0.9, 1.35, 1.8], pattern_label="Golomb_4.5"))
    candidates.append(make_candidate(split_a=0.6, pattern_label="Bipartite_0.6"))
    candidates.append(make_candidate(uniform=True, pattern_label="Uniform_0.5"))
    candidates.append(make_candidate(peaks=[0.3, 1.7], pattern_label="Two_bump_0.3_1.7"))
    candidates.append(make_candidate(peaks=[0.2, 1.5], pattern_label="Skewed_bimodal_0.2_1.5"))
    return {"candidates": candidates, "num_candidates": len(candidates)}
