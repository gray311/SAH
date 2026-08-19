def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N

    def make_h(pattern_name, marks=None, step_pos=None, peaks=None):
        h = np.zeros(N)
        if pattern_name == 'golomb_5' and marks is not None:
            for m in marks:
                center = int(m * N)
                width = int(N * 0.15)
                h += np.exp(-((np.arange(N) - center) ** 2) / (2 * width ** 2))
        elif pattern_name == 'bipartite' and step_pos is not None:
            pos = int(step_pos * N)
            h[:pos] = 4.0
            h[pos:] = -1.0
        elif pattern_name == 'tri_3' and peaks is not None:
            for p in peaks:
                center = int(p * N)
                width = int(N * 0.1)
                h += np.exp(-((np.arange(N) - center) ** 2) / (2 * width ** 2))
        elif pattern_name == 'random_uniform':
            h = np.ones(N) * 0.5
        else:
            h = np.random.randn(N) * 0.3 + 0.5

        # Normalize to integral=1
        h = np.clip(h, 0.001, 5.0)
        integral = np.sum(h) * dx
        if integral > 0:
            h = h / integral
        h = np.clip(h, 0.001, 1.0)
        integral = np.sum(h) * dx
        return h

    pattern_name = args.get('pattern_name', 'golomb_5')
    marks = [0.0, 0.4, 0.8, 1.2, 1.6] if pattern_name == 'golomb_5' else None
    step_pos = 0.5 if pattern_name == 'bipartite' else None
    peaks = [0.4, 1.0, 1.6] if pattern_name == 'tri_3' else None

    h = make_h(pattern_name, marks, step_pos, peaks)
    integral = np.sum(h) * dx

    j = 1.0 - h
    h_padded = np.pad(h, (0, N))
    j_padded = np.pad(j, (0, N))
    corr_fft = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
    correlation = np.fft.ifft(corr_fft).real
    struct_c5 = np.max(correlation * dx)

    is_valid = (0.001 <= np.min(h) and np.max(h) <= 1.0 and abs(integral - 1.0) < 0.01)

    return {"pattern_name": pattern_name, "struct_c5_bound": float(struct_c5),
            "is_valid": is_valid, "integral": float(integral),
            "recommendation": "PROCEED" if struct_c5 < 0.375 else "SKIP"}
