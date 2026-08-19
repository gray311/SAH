def run(ctx, args):
    import random
    import math
    import numpy as np
    
    N = args.get("num_intervals", 150)
    num_templates = args.get("num_templates", 100)
    template_classes = args.get("template_classes", ["single", "double", "symmetric", "shifted"])
    seed_val = args.get("seed", 42)
    dx = 2.0 / N
    
    random.seed(seed_val)
    
    templates = []
    
    for t_idx in range(num_templates):
        t_info = {
            "name": f"template_{t_idx:04d}",
            "type": random.choice(template_classes)
        }
        h = np.zeros(N)
        
        if t_info["type"] == "single":
            center = random.uniform(0.1, 0.9)
            width = random.uniform(0.5, 1.0)
            start = center - width/2
            end = center + width/2
            start_idx = max(0, int(start / dx))
            end_idx = min(N, int(end / dx))
            h[start_idx:end_idx] = 1.0
            mass = float(np.sum(h) * dx)
            if mass > 0.01:
                h = h / mass
            elif random.random() < 0.5:
                h = np.where(np.arange(N) < N//2, 2.0, 0.0)
            h = np.clip(h, 0.0, 1.0)
            
        elif t_info["type"] == "double":
            block1_center = random.uniform(0.1, 0.4)
            block2_center = random.uniform(1.6, 1.9)
            width = random.uniform(0.3, 0.6)
            
            start1 = max(0, block1_center - width/2)
            end1 = min(2.0, block1_center + width/2)
            start2 = max(0, block2_center - width/2)
            end2 = min(2.0, block2_center + width/2)
            
            h[max(0, int(start1/dx)):min(N, int(end1/dx))] = 1.0
            h[max(0, int(start2/dx)):min(N, int(end2/dx))] = 1.0
            
            mass = float(np.sum(h) * dx)
            if mass > 0.01:
                h = h / mass
            elif random.random() < 0.5:
                h = np.where((np.arange(N) < N//4) | (np.arange(N) >= N//2), 2.0, 0.0)
            h = np.clip(h, 0.0, 1.0)
            
        elif t_info["type"] == "symmetric":
            h = np.zeros(N)
            left_range = random.uniform(0.1, 0.45)
            left_width = random.uniform(0.2, 0.5)
            
            def set_block(start, width):
                s, e = start - width/2, start + width/2
                h[max(0, int(s/dx)):min(N, int(e/dx))] = 1.0
            
            set_block(left_range, left_width)
            set_block(2.0 - left_range, left_width)
            
            mass = float(np.sum(h) * dx)
            if mass > 0.01:
                h = h / mass
            elif random.random() < 0.5:
                h = np.where((np.arange(N) < N//4) | (np.arange(N) >= 3*N//4), 2.0, 0.0)
            h = np.clip(h, 0.0, 1.0)
            
        elif t_info["type"] == "shifted":
            start_frac = random.uniform(0.0, 1.0)
            width = random.uniform(0.4, 1.0)
            start = max(0.0, start_frac - width/2)
            end = min(2.0, start_frac + width/2)
            
            h = np.zeros(N)
            h[max(0, int(start/dx)):min(N, int(end/dx))] = 1.0
            
            mass = float(np.sum(h) * dx)
            if mass > 0.01:
                h = h / mass
            elif random.random() < 0.5:
                h = np.where(np.arange(N) < N//2, 2.0, 0.0)
            h = np.clip(h, 0.0, 1.0)
        
        h_list = h.tolist()
        templates.append((t_info, h_list))
    
    return {"templates": templates, "num_generated": len(templates)}