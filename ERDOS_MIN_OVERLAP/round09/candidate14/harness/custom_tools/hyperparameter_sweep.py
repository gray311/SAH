def run(ctx, args):
    import numpy as np
    configs = []
    lrs = [0.001, 0.005, 0.01, 0.02]
    penalties = [500, 1000, 2500, 5000, 10000]
    steps = [30000, 50000, 70000]
    restarts = [1, 2, 3, 5]
    intervals = [600, 800, 1000]
    
    for i, (lr, pen, steps, rest, ints) in enumerate(zip(
        lrs, penalties, steps, restarts, intervals)):
        cfg = {
            "num_intervals": ints,
            "base_learning_rate": lr,
            "num_steps": steps,
            "penalty_strength": pen,
            "num_restarts": rest,
            "config_seed": 42 + i,
            "description": f"Config {i+1}: lr={lr}, pen={pen}, steps={steps}, restarts={rest}, intervals={ints}"
        }
        configs.append(cfg)
    
    return {
        "configs": configs,
        "count": len(configs),
        "note": "Use probe_solution with each config to rank before full eval"
    }
