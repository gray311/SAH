def run(ctx, args):
    import numpy as np
    N = 800
    num_breaks = args.get('num_breaks', 3)
    heights = args.get('heights', None)
    normalize = args.get('normalize', True)
    
    if heights is None:
        num_intervals = num_breaks + 1
        heights = np.ones(num_intervals) / num_intervals
    
    h = np.zeros(N)
    interval_size = N // num_intervals
    for i in range(num_intervals):
        start_idx = i * interval_size
        end_idx = min((i + 1) * interval_size, N)
        h[start_idx:end_idx] = heights[i]
    
    if normalize and np.sum(h) > 0:
        h = h / np.sum(h)
    
    return {"h": h, "integral": float(np.sum(h))}