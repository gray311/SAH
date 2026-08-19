def run(ctx, args):
    prog = ctx.get_program()
    lines = prog.strip().split('\n')
    try:
        import numpy as np
        weight_data = np.array([
            [float(x) for x in line.split()] 
            for line in lines if line.strip() and not line.startswith('#')
        ])
        if weight_data.shape[1] < 2:
            return {"note": "insufficient data", "uniform": True}
        means = weight_data.mean(axis=1)
        stds = weight_data.std(axis=1)
        global_mean = means.mean()
        global_std = means.std()
        cv = global_std / global_mean if global_mean > 0 else 0
        skewed = cv > 0.5
        return {
            "shape": weight_data.shape,
            "global_mean": float(global_mean),
            "global_std": float(global_std),
            "cv": float(cv),
            "is_uniform": not skewed,
            "recommendation": "round_robin" if not skewed else "blocked_processing"
        }
    except:
        return {"note": "could not parse weights", "uniform": True, "recommendation": "round_robin"}
