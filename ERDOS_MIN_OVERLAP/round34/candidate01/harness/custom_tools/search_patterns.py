def run(ctx, args):
    import numpy as np
    num = args.get('num_variants', 5)
    N = 800
    domain = 2.0
    dx = domain / N
    
    variants = []
    
    # Pattern 1: Bipartite (threshold at a)
    a = 0.3 + 0.4 * np.random.random()
    h = np.zeros(N)
    h[:int(N*a)] = 1.0/a
    h[int(N*a):] = 0.0
    variants.append((h, f"bipartite_{a:.2f}"))
    
    # Pattern 2: Two peaks
    c1, c2 = 0.4, 1.6
    h = np.zeros(N)
    h[:int(N*c1)] = 0.0
    h[int(N*c1):int(N*c1+(N-c1))] = 1.0/(2*(1-c1))
    h[int(N*c1+(N-c1)):int(N*(c1+c2))] = 0.0
    h[int(N*(c1+c2)):] = 1.0/(1-c2)
    variants.append((h, f"two_peaks_{c1}_{c2}"))
    
    # Pattern 3: Three peaks (Golomb-like)
    marks = [0.25, 0.75, 1.25, 1.75]
    h = np.zeros(N)
    for m in marks:
        start = int(N * m)
        width = int(N * 0.1)
        h[start:start+width] = 1.0 / (4 * 0.1)
    variants.append((h, f"golomb_{marks}"))
    
    # Pattern 4: Four peaks
    marks = [0.2, 0.6, 1.0, 1.4]
    h = np.zeros(N)
    for m in marks:
        start = int(N * m)
        width = int(N * 0.15)
        h[start:start+width] = 1.0 / (4 * 0.15)
    variants.append((h, f"four_peaks_{marks}"))
    
    # Pattern 5: Random thresholds
    h = np.zeros(N)
    thresholds = np.sort(np.random.uniform(0.1, 1.9, 6))
    for i, t in enumerate(thresholds):
        h[int(N*t):int(N*(t+0.1))] = 1.0 / 0.1
    variants.append((h, f"random_{thresholds}"))
    
    return {
        "note": f"Generated {len(variants)} diverse step functions",
        "variants": variants
    }