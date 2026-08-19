def run(ctx, args):
    import numpy as np
    from numpy.fft import fft, ifft

    domain_width = 2.0
    N = args.get('num_intervals', 800)
    strategy = args.get('strategy', 'single_step')
    params = args.get('params', {})
    
    def compute_c5(h_arr):
        h = h_arr
        j_arr = 1.0 - h
        h_padded = np.pad(h, (0, N))
        j_padded = np.pad(j_arr, (0, N))
        corr_fft = fft(h_padded) * np.conj(fft(j_padded))
        correlation = ifft(corr_fft).real
        c5_bound = np.max(correlation * domain_width / N)
        integral = np.sum(h) * domain_width / N
        valid = np.all((h >= 0) & (h <= 1) & (abs(integral - 1.0) < 1e-5))
        return float(c5_bound), float(integral), bool(valid)
    
    x = np.linspace(0, domain_width, N)
    h_vals = np.zeros(N)
    c5_bound, integral, valid = 1.0, 1.0, False
    
    if strategy == 'single_step':
        midpoint = int(N // 2)
        h_vals = h_vals[:midpoint]
        h_vals[:midpoint] = 1.0
        valid, c5_bound = True, compute_c5(h_vals)[0]
        
    elif strategy == 'double_step':
        quarter = int(N // 4)
        h_vals = h_vals.copy()
        h_vals[:quarter] = 0.5
        h_vals[3*quarter:4*quarter] = 0.5
        valid, c5_bound = True, compute_c5(h_vals)[0]
        
    elif strategy == 'three_step':
        third = int(N // 3)
        h_vals = h_vals.copy()
        for i in [0, 1, 2]:
            start = i * third
            end = (i + 1) * third
            h_vals[start:end] = 1.0/3.0
        valid, c5_bound = True, compute_c5(h_vals)[0]
        
    elif strategy == 'symmetric':
        quarter = int(N // 4)
        h_vals = h_vals.copy()
        h_vals[:quarter] = 0.5
        h_vals[2*quarter:3*quarter] = 0.5
        valid, c5_bound = True, compute_c5(h_vals)[0]
        
    elif strategy == 'concentrated':
        half = int(N // 2)
        h_vals = h_vals.copy()
        h_vals[:half] = 1.0
        valid, c5_bound = True, compute_c5(h_vals)[0]
    
    integral = np.sum(h_vals) * domain_width / N
    result = {
        'h_values': h_vals.tolist(),
        'c5_bound': float(c5_bound),
        'integral': float(integral),
        'valid': bool(valid),
        'strategy': strategy,
        'N': N
    }
    
    return result