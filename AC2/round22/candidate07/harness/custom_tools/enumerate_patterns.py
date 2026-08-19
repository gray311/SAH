def run(ctx, args):
    import random
    random.seed(42)
    import numpy as np
    
    def create_step(num_intervals, shape_type, base_style, n_peaks=2):
        f = np.zeros(num_intervals)
        n = num_intervals
        
        if base_style == 'flat_spike':
            base_start = int(n * 0.05)
            base_end = int(n * 0.85)
            spike_start = int(n * 0.30)
            spike_end = int(n * 0.45)
            f[base_start:base_end] = 0.9 + random.uniform(0.0, 0.2)
            f[spike_start:spike_end] = 2.0 + random.uniform(0.3, 0.7)
        
        elif base_style == 'flat_double_spike':
            base_start = int(n * 0.05)
            base_end = int(n * 0.95)
            spike1_start = int(n * 0.20)
            spike1_end = int(n * 0.28)
            spike2_start = int(n * 0.52)
            spike2_end = int(n * 0.60)
            f[base_start:base_end] = 1.1 + random.uniform(0.0, 0.15)
            f[spike1_start:spike1_end] = 2.5 + random.uniform(0.4, 0.9)
            f[spike2_start:spike2_end] = 2.5 + random.uniform(0.4, 0.9)
        
        elif shape_type == 'trapezoid':
            h1 = 1.3
            h2 = 2.2
            h3 = 1.3
            f[0:int(n*0.25)] = h1
            f[int(n*0.25):int(n*0.75)] = h2
            f[int(n*0.75):int(n*0.95)] = h3
        
        elif shape_type == 'two_peak':
            f[int(n*0.15):int(n*0.35)] = 1.6
            f[int(n*0.45):int(n*0.65)] = 2.4
        
        elif shape_type == 'Gaussian_like':
            center = n // 2
            width = int(n * 0.15)
            for i in range(max(0, center-width), min(n, center+width)):
                d = abs(i - center)
                f[i] = max(0.5, 2.0 * np.exp(-0.5 * (d/width)**2))
        
        return np.array(f)
    
    configs = [
        (600, 'single', 'flat_spike'),
        (600, 'trapezoid', 'flat_spike'),
        (600, 'Gaussian_like', 'flat_spike'),
        (400, 'flat_double_spike', 'flat_double_spike'),
        (800, 'two_peak', 'flat_double_spike'),
        (500, 'single', 'flat_double_spike'),
        (700, 'trapezoid', 'flat_double_spike'),
    ]
    
    candidates = []
    for config in configs:
        num_intervals, shape_type, base_style = config
        f = create_step(num_intervals, shape_type, base_style)
        candidates.append({'num_intervals': num_intervals, 'function': f.tolist()})
    
    return candidates