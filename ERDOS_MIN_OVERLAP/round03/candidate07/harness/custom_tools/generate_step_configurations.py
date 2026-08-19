def run(ctx, args):
    import numpy as np
    domain = 2.0
    num_intervals = 200
    dx = domain / num_intervals
    N = num_intervals
    
    def make_step(h_vals):
        h_vals = np.asarray(h_vals, dtype=float)
        # Normalize to maintain integral=1
        current_integral = np.sum(h_vals) * dx
        if current_integral != 1.0:
            scale = 1.0 / current_integral
            h_vals = h_vals * scale
        # Clamp to [0,1]
        h_vals = np.clip(h_vals, 0.0, 1.0)
        # Renormalize after clipping
        current_integral = np.sum(h_vals) * dx
        if current_integral > 0:
            h_vals = h_vals * (1.0 / current_integral)
        return np.clip(h_vals, 0.0, 1.0)
    
    configs = {}
    
    # Bimodal narrow: peaks at 0.25 and 0.75
    h_vals = np.zeros(N)
    h_vals[50:100] = 2.0  # 50 intervals per peak
    configs['bimodal_narrow'] = make_step(h_vals)
    
    # Bimodal wider: peaks at 0.25 and 0.75
    h_vals = np.zeros(N)
    h_vals[40:120] = 2.0
    configs['bimodal_wide'] = make_step(h_vals)
    
    # Triangular: high in middle, lower elsewhere
    h_vals = np.zeros(N)
    h_vals[80:120] = 1.5  # [0.4, 0.6]
    h_vals[40:60] = 0.8   # [0.2, 0.3]
    h_vals[140:160] = 0.8 # [0.7, 0.8]
    configs['triangular'] = make_step(h_vals)
    
    # Periodic: high on [0,0.5] and [1,1.5]
    h_vals = np.zeros(N)
    h_vals[:100] = 2.0    # [0, 0.5]
    h_vals[200:300] = 2.0 # [1.0, 1.5]
    configs['periodic_1'] = make_step(h_vals)
    
    # Uniform-ish: spread over most of domain
    h_vals = np.ones(N) / 2.0  # h=0.5 almost everywhere
    h_vals[:50] = 2.0  # boost at start
    h_vals[-50:] = 2.0 # boost at end
    configs['uniform_boost'] = make_step(h_vals)
    
    return {"configurations": configs}
