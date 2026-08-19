def run(ctx, args):
    import numpy as np
    import math
    
    N = 800
    domain = 2.0
    dx = domain / N
    constructions = []
    
    def make_h_from_marks(marks, kernel_type='gaussian', widths=None):
        x = np.linspace(0, domain, N)
        h = np.zeros(N)
        if widths is None:
            widths = [0.15] * len(marks)
        if kernel_type == 'gaussian':
            for mark, width in zip(marks, widths):
                h += np.exp(-((x - mark) / width) ** 2 * 30)
        else:
            for mark, width in zip(marks, widths):
                h += np.clip((x - mark) / width + 0.5, 0, 1)
        
        integral = h.sum() * dx
        if integral > 0:
            h = h / integral
        return h
    
    def probe_c5(h):
        j = 1.0 - h
        N_local = 800
        h_pad = np.pad(h, (0, N_local))
        j_pad = np.pad(j, (0, N_local))
        corr_fft = np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))
        correlation = np.fft.ifft(corr_fft).real
        return float(np.max(correlation) * dx)
    
    def local_optimize_positions(marks, kernel_type, widths, steps=15):
        best_score = float('inf')
        best_marks = marks.copy()
        for _ in range(steps):
            perturbed = np.array(marks)
            perturbed = perturbed + np.random.uniform(-0.05, 0.05, len(marks))
            perturbed = np.clip(perturbed, 0, domain)
            h = make_h_from_marks(perturbed, kernel_type, widths)
            score = probe_c5(h)
            if score < best_score:
                best_score = score
                best_marks = perturbed.copy()
        return best_marks, best_score
    
    best_overall = None
    best_overall_score = float('inf')
    
    base_positions = {
        3: np.array([0.0, 1.0, 2.0]),
        4: np.array([0.0, 0.5, 1.5, 2.0]),
        5: np.array([0.0, 0.25, 0.75, 1.25, 2.0]),
        6: np.array([0.0, 0.2, 0.6, 1.0, 1.4, 2.0]),
        7: np.array([0.0, 0.15, 0.45, 0.75, 1.05, 1.35, 2.0]),
        8: np.array([0.0, 0.12, 0.35, 0.55, 0.8, 1.0, 1.3, 2.0]),
    }
    
    for num_marks in [3, 4, 5, 6, 7, 8]:
        base_marks = base_positions[num_marks]
        for width in [0.08, 0.12, 0.18]:
            widths = [width] * num_marks
            for ktype in ['gaussian', 'boxcar']:
                best_marks, score = local_optimize_positions(base_marks, ktype, widths, steps=12)
                h = make_h_from_marks(best_marks, ktype, widths)
                c5 = probe_c5(h)
                if c5 < best_overall_score:
                    best_overall_score = c5
                    best_overall = {'marks': best_marks.tolist(), 'kernel': ktype, 'width': width, 'c5_bound': c5, 'h': h}
        for widths_combo in [[0.1, 0.15], [0.08, 0.12, 0.16], [0.12, 0.14, 0.16]]:
            if len(widths_combo) != num_marks:
                continue
            for ktype in ['gaussian', 'boxcar']:
                best_marks, score = local_optimize_positions(base_marks, ktype, widths_combo, steps=8)
                h = make_h_from_marks(best_marks, ktype, widths_combo)
                c5 = probe_c5(h)
                if c5 < best_overall_score:
                    best_overall_score = c5
                    best_overall = {'marks': best_marks.tolist(), 'kernel': ktype, 'width': widths_combo, 'c5_bound': c5, 'h': h}
    
    if best_overall:
        return {'constructions': [best_overall], 'note': 'Best Golomb construction via internal search', 'c5_best': best_overall['c5_bound']}
    return {'constructions': [], 'note': 'No constructions found'}
