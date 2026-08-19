def run(ctx, args):
    import numpy as np
    N_choices = [100, 150, 200]
    constructions = {}
    for N in N_choices:
        domain = 2.0
        x = np.linspace(0, domain, N)
        dx = domain / N
        
        # Binary step pattern 1: bimodal tight
        h1 = np.zeros(N)
        h1[(x >= 0.2) & (x < 0.3)] = 4.0
        h1[(x >= 0.7) & (x < 0.8)] = 4.0
        h1 = np.clip(h1, 0, 10)
        
        # Binary step pattern 2: central peak
        h2 = np.zeros(N)
        h2[(x >= 0.35) & (x < 0.65)] = 4.0
        h2 = np.clip(h2, 0, 10)
        
        # Binary step pattern 3: three peaks
        h3 = np.zeros(N)
        h3[(x >= 0.15) & (x < 0.25)] = 4.0
        h3[(x >= 0.45) & (x < 0.55)] = 4.0
        h3[(x >= 0.75) & (x < 0.85)] = 4.0
        h3 = np.clip(h3, 0, 10)
        
        # Binary step pattern 4: half-half
        h4 = np.zeros(N)
        h4[(x >= 0.4) & (x < 0.6)] = 4.0
        h4 = np.clip(h4, 0, 10)
        
        # Binary step pattern 5: many small steps
        h5 = np.zeros(N)
        for i in range(0, N, 4):
            h5[i:i+2] = 4.0
        h5 = np.clip(h5, 0, 10)
        
        # Binary step pattern 6: golden ratio spacing
        h6 = np.zeros(N)
        ratios = [1/3, 2/3, 1/2, 1/5, 4/5, 1/4, 3/4, 2/5, 3/5]
        for r in ratios:
            h6[(x >= r) & (x < r + 0.02)] = 4.0
        h6 = np.clip(h6, 0, 10)
        
        constructions["N" + str(N)] = {
            "bimodal_tight": h1,
            "central_peak": h2,
            "three_peaks": h3,
            "half_half": h4,
            "many_small_steps": h5,
            "golden_spacing": h6
        }
    return {"constructions": constructions}