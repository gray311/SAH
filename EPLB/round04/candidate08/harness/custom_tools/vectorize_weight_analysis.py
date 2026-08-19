def run(ctx, args):
    import math
    weight = ctx.get_program()
    lines = weight.strip().split('\n')
    if len(lines) < 2:
        return {"note": "insufficient data"}
    
    try:
        w_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts:
                w_lines.append([float(x) for x in parts])
        
        if not w_lines:
            return {"note": "no valid numeric data"}
        
        import numpy as np
        weight_matrix = np.array(w_lines, dtype=np.float32)
        num_layers, num_groups = weight_matrix.shape
        
        layer_means = weight_matrix.mean(axis=1)
        layer_stds = weight_matrix.std(axis=1)
        global_std = weight_matrix.std()
        global_mean = weight_matrix.mean()
        
        std_ratio = (layer_stds.max() / layer_stds.min()).item() if layer_stds.min() > 0 else 1.0
        
        if global_std < global_mean * 0.1:
            strategy = "uniform_weights: use simple round-robin (// and % ops)"
            recommended_op = "round_robin_vectorized"
        elif std_ratio > 5:
            strategy = "highly_skewed: sort descending, use argmax for heavy items"
            recommended_op = "sort_then_gather"
        else:
            strategy = "moderate_variance: use argsort + scatter"
            recommended_op = "argsort_scatter"
        
        return {
            "num_layers": int(num_layers),
            "num_groups": int(num_groups),
            "global_mean": float(global_mean),
            "global_std": float(global_std),
            "std_ratio": float(std_ratio),
            "strategy": strategy,
            "recommended_op": recommended_op
        }
    except Exception as e:
        return {"note": "analysis error: " + str(e)}