def run(ctx, args):
    prog = ctx.get_program()
    lines = prog.strip().split('\n')
    if len(lines) < 5:
        return {"error": "insufficient data"}
    try:
        import numpy as np
        w = np.array([list(map(float, l.split())) for l in lines])
        layer_means = w.mean(axis=1)
        layer_stds = w.std(axis=1)
        heavy_idx = np.where(layer_means > layer_means.mean() + layer_stds.std())[0]
        light_idx = np.where(layer_means < layer_means.mean() - layer_stds.std())[0]
        return {"shape": w.shape, "layer_means": layer_means.tolist(), 
                "layer_stds": layer_stds.tolist(), 
                "heavy_layers": heavy_idx.tolist(), 
                "light_layers": light_idx.tolist()}
    except:
        return {"note": "could not parse, assuming uniform distribution"}
