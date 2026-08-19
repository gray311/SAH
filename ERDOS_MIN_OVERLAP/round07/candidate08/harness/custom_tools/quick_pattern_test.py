def run(ctx, args):
    import numpy as np
    
    N = 40
    dx = 2.0 / N
    
    def compute_c5(h):
        j = 1.0 - h
        h_p = np.pad(h, (0, N))
        j_p = np.pad(j, (0, N))
        corr = np.fft.ifft(np.fft.fft(h_p) * np.conj(np.fft.fft(j_p))).real
        return float(np.max(corr) * dx)
    
    def make_single_block(width_frac=0.5):
        width = 2.0 * width_frac
        h = np.zeros(N)
        start_idx = 0
        end_idx = int(width / dx + 0.5)
        h[start_idx:end_idx] = 1.0 / width
        return h
    
    def make_two_blocks(w1=0.5, w2=0.5, offset=1.0):
        h = np.zeros(N)
        n1 = int(w1 / dx)
        h[0:n1] = 1.0 / w1
        start2 = int(offset * N / 2.0)
        end2 = start2 + int(w2 / dx + 0.5)
        h[start2:end2] = 1.0 / w2
        return h
    
    def make_uniform():
        return np.ones(N) * 0.5
    
    def make_biphasic(w=0.5, gap=0.5):
        h = np.zeros(N)
        n_per = int(w / dx)
        h[0:n_per] = 1.0 / w
        h_gap = int(gap * N / 2.0)
        h[h_gap:h_gap+n_per] = 1.0 / w
        return h
    
    def make_concentrated(w=1.0, pos=0.25):
        h = np.zeros(N)
        start = int(pos * N / 2.0)
        end = start + int(w * N / 2.0)
        h[start:end] = 1.0 / w
        return h
    
    c1 = make_single_block(width_frac=0.5)
    c2 = make_two_blocks(w1=0.5, w2=0.5, offset=1.0)
    c3 = make_uniform()
    c4 = make_biphasic(w=0.5, gap=0.5)
    c5 = make_concentrated(w=1.0, pos=0.25)
    
    results = []
    for i, h_arr in enumerate([c1, c2, c3, c4, c5], 1):
        c5_val = compute_c5(h_arr)
        combined = 0.38092303510845016 / c5_val
        results.append({"pattern": i, "c5": c5_val, "combined": combined})
    
    return {"patterns_tested": 5, "results": results}