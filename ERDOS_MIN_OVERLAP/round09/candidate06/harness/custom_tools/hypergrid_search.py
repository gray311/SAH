def run(ctx, args):
    import numpy as np
    lrs = [0.001, 0.005, 0.01, 0.02, 0.05]
    penalties = [500, 1000, 2000, 5000, 10000]
    steps = [10000, 20000, 40000, 60000]
    num_restarts = [3, 5, 10]
    seeds = list(range(20))
    grid = []
    for lr in lrs:
        for penalty in penalties:
            for step in steps:
                for nr in num_restarts:
                    for seed in seeds[:10]:
                        grid.append({
                            "lr": lr,
                            "penalty": penalty,
                            "steps": step,
                            "num_restarts": nr,
                            "seed": seed
                        })
    return {"combinations": grid[:150], "total": len(grid)}