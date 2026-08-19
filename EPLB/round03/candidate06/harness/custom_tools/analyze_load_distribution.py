def run(ctx, args):
    weight = ctx.get_program()
    lines = weight.strip().split('\n')
    if len(lines) < 2:
        return {"analysis": "insufficient data"}
    # Parse the weight matrix (simplified - assumes numpy-like or csv format)
    try:
        import numpy as np
        w = np.array([list(map(float, line.split())) for line in lines])
        mean_load = w.mean(axis=1)
        std_load = w.std(axis=1)
        max_load = w.max(axis=1)
        return {
            "mean_load": float(np.mean(mean_load)),
            "std_load": float(np.std(std_load)),
            "max_load": float(max(max_load)),
            "load_variance": float(np.var(mean_load)),
            "heavy_experts": [i for i, load in enumerate(mean_load) if load > np.mean(mean_load) + np.std(mean_load)],
            "light_experts": [i for i, load in enumerate(mean_load) if load < np.mean(mean_load) - np.std(mean_load)]
        }
    except:
        return {"note": "could not parse weight, returning stats estimate"}
