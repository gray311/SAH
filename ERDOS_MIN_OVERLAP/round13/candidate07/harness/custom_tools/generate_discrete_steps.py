def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    constructions = {}
    
    # Pattern 1: Two equal rectangles
    h = np.zeros(N)
    w = 1.0  # total width must be 1 for integral=1
    h[:int(N*w/2)] = 2.0
    h[int(N*w/2):int(N*w)] = 2.0
    constructions['two_rect'] = h
    
    # Pattern 2: Three equal rectangles
    h = np.zeros(N)
    w = 1.0
    for i in range(3):
        start = int(N * i / 3)
        end = int(N * (i+1) / 3)
        h[start:end] = 3.0
    constructions['three_rect'] = h
    
    # Pattern 3: Symmetric block (high in center)
    h = np.zeros(N)
    center_width = 0.6
    h[int(N*(1-center_width)/2):int(N*(1+center_width)/2)] = 1/center_width
    constructions['symmetric_center'] = h
    
    # Pattern 4: Asymmetric block (high on left)
    h = np.zeros(N)
    left_width = 0.4
    h[:int(N*left_width)] = 1/left_width
    constructions['asymmetric_left'] = h
    
    # Pattern 5: Two-level (high, medium, low regions)
    h = np.zeros(N)
    regions = [0.3, 0.5, 0.2]
    heights = [5/0.3, 2/0.5, 0.5/0.2]  # normalize to integral=1
    for i, (r, ht) in enumerate(zip(regions, heights)):
        start = int(N * sum(regions[:i]))
        end = int(N * sum(regions[:i+1]))
        h[start:end] = ht
    constructions['two_level'] = h
    
    # Pattern 6: Four equal segments
    h = np.zeros(N)
    for i in range(4):
        start = int(N * i / 4)
        end = int(N * (i+1) / 4)
        h[start:end] = 4.0
    constructions['four_rect'] = h
    
    return {"constructions": constructions, "num_constructions": 6}
