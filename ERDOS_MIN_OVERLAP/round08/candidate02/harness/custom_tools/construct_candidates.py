def run(ctx, args):
    import random
    import numpy as np
    
    num_intervals = ctx.hypers.num_intervals if hasattr(ctx, 'hypers') else 800
    domain_width = ctx.hypers.domain_width if hasattr(ctx, 'hypers') else 2.0
    dx = domain_width / num_intervals
    
    candidates = []
    
    # Single block: h=1 on [0,1]
    def make_single_block():
        h = np.zeros(num_intervals)
        start = int(0 / dx)
        end = int(1.0 / dx) + 1
        h[start:end] = 1.0
        return h, 1.0
    
    # Double block: h=0.5 on [0,0.5] and [1.5,2]
    def make_double_block():
        h = np.zeros(num_intervals)
        h[:int(0.5/dx)+1] = 0.5
        h[int(1.5/dx):int(2.0/dx)+1] = 0.5
        return h, 1.0
    
    # Three block: h=1/3 on three intervals
    def make_three_block():
        h = np.zeros(num_intervals)
        for start, end in [(0, 2/3), (2/3, 4/3), (4/3, 2.0)]:
            h[int(start/dx):int(end/dx)+1] = 1/3
        return h, 1.0
    
    # Symmetric around x=1
    def make_symmetric():
        h = np.zeros(num_intervals)
        h[int(0.5/dx):int(1.5/dx)+1] = 0.5
        return h, 1.0
    
    # Asymmetric three blocks
    def make_asymmetric():
        h = np.zeros(num_intervals)
        h[int(0/dx):int(0.33/dx)+1] = 1/3
        h[int(0.66/dx):int(0.99/dx)+1] = 1/3
        h[int(1.33/dx):int(2.0/dx)+1] = 1/3
        return h, 1.0
    
    def make_random_piecewise():
        n_blocks = random.randint(5, 10)
        np.random.seed(random.randint(0, 2**31))
        breakpoints = np.sort(np.random.uniform(0.0, domain_width, n_blocks+1))
        heights = np.random.uniform(0.0, 2.0, n_blocks)
        
        block_lengths = breakpoints[1:] - breakpoints[:-1]
        block_lengths = block_lengths / np.sum(block_lengths)
        heights = heights / np.sum(heights * block_lengths)
        
        h = np.zeros(num_intervals)
        for i in range(n_blocks):
            start = int(breakpoints[i] / dx)
            end = int(breakpoints[i+1] / dx)
            h[start:end] = heights[i]
        return h, float(np.sum(h) * dx)
    
    strategy_map = {
        "single_block": make_single_block,
        "double_block": make_double_block,
        "three_block": make_three_block,
        "symmetric_two": make_symmetric,
        "asymmetric_three": make_asymmetric,
        "random_piecewise": make_random_piecewise
    }
    
    used_strategies = set(args.get("strategies", ["single_block", "double_block", 
               "three_block", "symmetric_two", "asymmetric_three"]))
    for strategy in used_strategies:
        if strategy in strategy_map:
            for _ in range(args.get("num_candidates", 5)):
                try:
                    h, integral = strategy_map[strategy]()
                    if abs(integral - 1.0) > 0.01:
                        h = h * (1.0 / integral)
                    h = np.clip(h, 0.0, 1.0)
                    candidates.append({
                        "strategy": strategy,
                        "h": h,
                        "integral": float(integral),
                        "n_nonzero": int(np.sum(h > 0))
                    })
                except Exception:
                    pass
    
    return {
        "num_candidates": len(candidates),
        "candidates": candidates,
        "num_intervals": num_intervals,
        "dx": float(dx)
    }