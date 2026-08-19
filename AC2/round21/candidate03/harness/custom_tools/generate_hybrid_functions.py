def run(ctx, args):
    import re
    import numpy as np
    
    best_f = ctx.get_best_program()
    if not best_f:
        return {"note": "no best program"}
    
    # Extract num_intervals from code
    num_intervals = 600
    match = re.search(r'num_intervals:\s*(\d+)', best_f)
    if match:
        num_intervals = int(match.group(1))
    
    # Generate 5 hybrid variants using numpy array operations
    hybrids = []
    
    # Hybrid 1: Mix patterns 0,1,2 with varied heights
    h1 = np.zeros(num_intervals)
    h1[int(0.2*num_intervals):int(0.3*num_intervals)] = 1.5
    h1[int(0.3*num_intervals):int(0.7*num_intervals)] = 2.0
    h1[int(0.7*num_intervals):int(0.8*num_intervals)] = 1.2
    hybrids.append(("mix_123", h1.tolist()))
    
    # Hybrid 2: Single high peak with wider base
    h2 = np.zeros(num_intervals)
    h2[int(0.1*num_intervals):int(0.9*num_intervals)] = 1.2
    h2[int(0.35*num_intervals):int(0.65*num_intervals)] = 2.8
    hybrids.append(("wide_base", h2.tolist()))
    
    # Hybrid 3: Three distinct peaks
    h3 = np.zeros(num_intervals)
    h3[int(0.1*num_intervals):int(0.25*num_intervals)] = 1.8
    h3[int(0.25*num_intervals):int(0.35*num_intervals)] = 2.5
    h3[int(0.35*num_intervals):int(0.45*num_intervals)] = 1.8
    h3[int(0.45*num_intervals):int(0.55*num_intervals)] = 2.5
    h3[int(0.55*num_intervals):int(0.7*num_intervals)] = 1.5
    hybrids.append(("three_peaks", h3.tolist()))
    
    # Hybrid 4: Asymmetric multi-level
    h4 = np.zeros(num_intervals)
    h4[int(0.08*num_intervals):int(0.18*num_intervals)] = 1.0
    h4[int(0.18*num_intervals):int(0.28*num_intervals)] = 1.8
    h4[int(0.28*num_intervals):int(0.45*num_intervals)] = 2.2
    h4[int(0.45*num_intervals):int(0.65*num_intervals)] = 1.5
    h4[int(0.65*num_intervals):int(0.85*num_intervals)] = 1.1
    hybrids.append(("asymmetric", h4.tolist()))
    
    # Hybrid 5: Staircase with refinement
    h5 = np.zeros(num_intervals)
    h5[int(0.06*num_intervals):int(0.22*num_intervals)] = 0.7
    h5[int(0.22*num_intervals):int(0.38*num_intervals)] = 1.2
    h5[int(0.38*num_intervals):int(0.58*num_intervals)] = 1.8
    h5[int(0.58*num_intervals):int(0.78*num_intervals)] = 1.4
    h5[int(0.78*num_intervals):int(0.94*num_intervals)] = 1.0
    hybrids.append(("staircase", h5.tolist()))
    
    # Hybrid 6: Novel - wide base narrow high peak
    h6 = np.zeros(num_intervals)
    h6[int(0.1*num_intervals):int(0.9*num_intervals)] = 1.1
    h6[int(0.35*num_intervals):int(0.65*num_intervals)] = 3.0
    hybrids.append(("novel_wide", h6.tolist()))
    
    result = {"hybrids": hybrids}
    for name, hlist in hybrids:
        result[name] = hlist
    
    return result