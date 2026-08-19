def run(ctx, args):
    weight_str = ctx.get_program()
    lines = weight_str.strip().split('\n')
    if len(lines) < 2:
        return {"note": "insufficient data"}
    try:
        import numpy as np
        w = np.array([list(map(float, line.split())) for line in lines])
        num_layers, num_groups = w.shape
        groups_per_pack = num_groups // 3
        sorted_indices = np.argsort(-w, axis=1)
        pack_assignments = np.repeat(np.arange(groups_per_pack), num_groups).reshape(1, -1)
        expanded = np.tile(pack_assignments, (num_layers, 1))
        ranks = np.repeat(np.arange(groups_per_pack), groups_per_pack // 1)
        return {
            "shape": {"layers": num_layers, "groups": num_groups},
            "load_mean": float(w.mean()),
            "load_std": float(w.std()),
            "load_min": float(w.min()),
            "load_max": float(w.max()),
            "groups_per_pack": groups_per_pack,
            "vectorizable": True,
            "recommendation": "Rewrite balanced_packing to use torch.argsort and scatter operations"
        }
    except Exception as e:
        return {"error": str(e), "note": "could not parse weight"}
