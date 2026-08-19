def run(ctx, args):
    import random
    import math

    num_steps = args.get("num_steps", 20)
    seed = args.get("seed", 42)
    num_intervals = ctx.hypers.get("num_intervals", 50) if hasattr(ctx, 'hypers') else 50
    
    rng = random.Random(seed)
    # Generate random breakpoints symmetric around 0
    half_steps = num_steps // 2
    endpoints_left = [-0.5 + i * 5.0 / half_steps for i in range(half_steps + 1)]
    endpoints_right = [-5.0 + i * 5.0 / half_steps for i in range(half_steps)]
    endpoints = endpoints_left + endpoints_right
    endpoints.sort()
    
    # Generate heights (must be non-negative)
    heights = [max(rng.uniform(0, 10), 1e-6) for _ in range(num_steps)]
    
    result = {
        "type": "step_function",
        "num_steps": num_steps,
        "breakpoints": endpoints,
        "heights": heights,
        "note": "Step function variant - tested with probe_solution to rank before full eval"
    }
    return result