def run(ctx, args):
    import numpy as np
    N = int(args.get('num_intervals', 800))
    domain = 2.0
    dx = domain / N
    
    def normalize(h):
        integral = np.sum(h) * dx
        return h / integral  # Ensure integral = 1
    
    def clamp(h):
        return np.clip(h, 0.01, 1.0) / np.sum(np.clip(h, 0.01, 1.0)) * N
    
    candidates = []
    
    # Candidate 1: 4 uniform steps
    h = np.zeros(N)
    h[:int(N*0.2)] = 2.5
    h[int(N*0.2):int(N*0.6)] = 2.0
    h[int(N*0.6):int(N*1.4)] = 1.5
    h[int(N*1.4):] = 1.0
    h = normalize(h)
    h = clamp(h)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = np.max(corr * dx)
    candidates.append({'h': h.tolist(), 'c5_bound': float(c5), 'pattern': 'uniform_4'})
    
    # Candidate 2: Delta peaks
    h = np.zeros(N)
    for center in [0.4, 1.0, 1.6]:
        mask = np.abs(np.arange(N) / N - center) < 0.15
        h[mask] = 12.0
    h = normalize(h)
    h = clamp(h)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = np.max(corr * dx)
    candidates.append({'h': h.tolist(), 'c5_bound': float(c5), 'pattern': 'delta_3'})
    
    # Candidate 3: Bipartite
    h = np.zeros(N)
    h[:int(N*0.5)] = 3.0
    h[int(N*0.5):] = 0.3
    h = normalize(h)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = np.max(corr * dx)
    candidates.append({'h': h.tolist(), 'c5_bound': float(c5), 'pattern': 'bipartite'})
    
    # Candidate 4: Tri-bipartite (high-low-high)
    h = np.zeros(N)
    h[:int(N*0.3)] = 3.0
    h[int(N*0.3):int(N*0.7)] = 0.3
    h[int(N*0.7):] = 3.0
    h = normalize(h)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = np.max(corr * dx)
    candidates.append({'h': h.tolist(), 'c5_bound': float(c5), 'pattern': 'tri_bipartite'})
    
    # Candidate 5: Sinusoidal steps
    x = np.arange(N) / N
    h = np.abs(np.sin(np.pi * x / 0.8)) + np.abs(np.sin(2 * np.pi * x / 1.2))
    h = normalize(h)
    h = clamp(h)
    j = 1.0 - h
    h_pad = np.pad(h, (0, N))
    j_pad = np.pad(j, (0, N))
    corr = np.fft.ifft(np.fft.fft(h_pad) * np.conj(np.fft.fft(j_pad))).real
    c5 = np.max(corr * dx)
    candidates.append({'h': h.tolist(), 'c5_bound': float(c5), 'pattern': 'sinusoidal'})
    
    return {'candidates': candidates, 'num_candidates': len(candidates), 'patterns': [c['pattern'] for c in candidates]}